from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.comment import get_commenters_for_post
from app.crud.post import get_subscribers_for_a_post
from app.models.post import Post
from app.models.user import User
from app.websockets import ConnectionManager

manager = ConnectionManager()


async def websocket_endpoint(
    websocket: WebSocket,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    await manager.connect(websocket, user.id)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)


async def notify_on_new_comment(
    post_id, comment_content: str, db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    author_id = post.author.id

    commenters = get_commenters_for_post(db, post_id)
    subscribed_users = get_subscribers_for_a_post(db, post_id)
    if author_id in manager.active_connections:
        await manager.send_personal_messages(
            f"New comment on your post:{comment_content}", author_id
        )
    for each_commenter in commenters:
        if (
            each_commenter.user_id in manager.active_connections
            and each_commenter.user_id != author_id
        ):
            await manager.send_personal_messages(
                f"New comment on a post you commented on: {comment_content}",
                each_commenter.user_id,
            )

    for subscriber in subscribed_users:
        if (
            subscriber.user_id in manager.active_connections
            and subscriber.user_id != author_id
            and subscriber.user_id not in [c.user_id for c in commenters]
        ):
            await manager.send_personal_messages(
                f"New comment on a post you are subscribed to: {comment_content}",
                subscriber.user_id,
            )
