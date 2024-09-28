from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud import like, post
from app.models.like import Like
from app.models.user import User
from app.schemas.like import LikeAction
from app.schemas.post import PostCreate, PostRead
from app.models.post import Post

router = APIRouter()


@router.get("/", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db), author_id: int = Query(None, description="Filter by author id"),
                  min_likes: int = Query(None, description="Filter by minimum number of likes"),
                  title: str = Query(None, description="Filter by title")):
    query = db.query(Post)
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if min_likes:
        query = query.filter(Post.like_count >= min_likes)
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))
    posts = query.all()
    return posts


@router.get("/{id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    pst = post.get_post(db, id)
    return pst


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
        post_create: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return post.create_post(db, post_create, current_user.id)


@router.put("/{id}", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def update_post(
        id: int,
        post_read: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return post.update_post(db, post_read, id, current_user.id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    post.delete_post(db, id)


# like/dislike a post
@router.post("/{id}/{action}", status_code=status.HTTP_201_CREATED)
def like_dislike_post(
        id: int,
        action: LikeAction,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    get_post = post.get_post(db, id)
    if not get_post:
        raise HTTPException(status_code=404, detail="detail not found")
    if action == LikeAction.like:
        like.like_post(db, current_user, get_post)
    elif action == LikeAction.dislike:
        like.dislike_post(db, current_user, get_post)

    like_record = (
        db.query(Like)
        .filter(Like.user_id == current_user.id, Like.post_id == get_post.id)
        .first()
    )
    is_like = like_record.is_like if like_record else False

    return {"post_id": get_post.id, "user_id": current_user.id, "is_like": is_like}
