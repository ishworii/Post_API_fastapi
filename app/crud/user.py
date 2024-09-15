from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.utils.hashing import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_users(db: Session, limit: int = 10):
    return db.query(User).limit(limit).all()


def get_user_by_username(db: Session, username: int) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
