from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status
from .utility import hash_password


def get_posts(db: Session, limit: int = 10):
    return db.query(models.Post).limit(limit).all()


def get_users(db: Session, limit: int = 10):
    return db.query(models.User).limit(limit).all()


def get_post(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found"
        )
    return post


def get_user_by_username(db: Session, username: int) -> models.User | None:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


def create_post(db: Session, post: schemas.PostCreate):

    new_post = models.Post(title=post.title, content=post.content, author=post.author)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        email=user.email,
        fullname=user.fullname,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
