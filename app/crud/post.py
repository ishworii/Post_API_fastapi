from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate


def get_posts(db: Session, limit: int = 10):
    return db.query(Post).limit(limit).all()


def get_post(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found"
        )

    return post


def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.author_id == user_id).all()


def create_post(db: Session, post: PostCreate, user_id: int):
    new_post = Post(**post.model_dump(), author_id=user_id)
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(db: Session, post: PostCreate, id: int, author_id: int):
    existing_post = db.query(Post).filter(Post.id == id).first()
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


def delete_post(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.delete(post)
    db.commit()
