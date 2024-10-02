from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    normal = "normal"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False, unique=True)
    email = Column(String(50), index=True, nullable=False, unique=True)
    full_name = Column(String(100))
    hashed_password = Column(
        String(128),
        index=False,
    )
    role = Column(Enum(UserRole), default=UserRole.normal)
    posts = relationship("Post", back_populates="author", cascade="all,delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all,delete-orphan")
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
