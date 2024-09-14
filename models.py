from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(String, nullable=True, default="admin")
    created_at = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False, unique=True)
    email = Column(String(50), index=True, nullable=False, unique=True)
    fullname = Column(String(100))
    hashed_password = Column(
        String(128),
        index=False,
    )
