from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.post import Post, Subscription
from app.schemas.post import PostCreate


def get_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{post_id} not found",
        )
    return post


def create_post(db: Session, post: PostCreate, user_id: int):
    new_post = Post(**post.model_dump(), author_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(db: Session, post: PostCreate, post_id: int, author_id: int):
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.author_id = author_id
    db.commit()
    db.refresh(existing_post)
    return existing_post


def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.delete(post)
    db.commit()


def get_subscribers_for_a_post(db: Session, post_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(post_id).all()
