from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status


def get_posts(db: Session, limit: int = 10):
    return db.query(models.Post).limit(limit).all()


def get_post(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()


def create_post(db: Session, post: schemas.Post):

    new_post = models.Post(title=post.title, content=post.content, author=post.author)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update_post(db: Session, post: schemas.Post, id: int):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.author = post.author
    db.commit()
    db.refresh(existing_post)
    return existing_post


def delete_post(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.delete(post)
    db.commit()
