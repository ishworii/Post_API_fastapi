from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from .utility import verify_password
from .crud import get_user_by_username
from .models import User
from sqlalchemy.orm import Session


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
