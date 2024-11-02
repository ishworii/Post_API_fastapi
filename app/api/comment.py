from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import verify_jwt_token
from app.crud import comment as crud_comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
from app.websockets import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_comment = crud_comment.create_comment(
        db, comment=comment, post_id=post_id, user_id=current_user.id
    )
    await manager.broadcast(
        f"New comment by {current_user.username}: {new_comment.content}"
    )

    return new_comment


@router.get("/posts/{post_id}/comments", response_model=list[CommentRead])
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return crud_comment.get_comments_by_post(db, post_id=post_id)


@router.get("/comments/me", response_model=list[CommentRead])
def get_all_comments_by_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud_comment.get_comments_by_user(db, current_user.id)


@router.get("/comments/{comment_id}", response_model=CommentRead)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = crud_comment.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/comments/{comment_id}", response_model=CommentRead)
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = crud_comment.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this comment"
        )
    return crud_comment.update_comment(
        db, comment_id=comment_id, content=comment.content
    )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = crud_comment.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )
    crud_comment.delete_comment(db, comment_id=comment_id)


@router.websocket("/ws/comments")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        username = verify_jwt_token(token)
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
