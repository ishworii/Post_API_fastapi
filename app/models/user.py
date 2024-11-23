from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(PyEnum):
    normal = "normal"
    admin = "admin"
    
    
user_follow_table = Table(
    "user_follow",
    Base.metadata,
    Column("follower_id",Integer,ForeignKey("users.id"),primary_key=True),
    Column("following_id",Integer,ForeignKey("users.id"),primary_key=True),
)


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
    subscriptions = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
    )

    followers = relationship(
        "User",
        secondary=user_follow_table,
        primaryjoin= id == user_follow_table.c.following_id,
        secondaryjoin= id == user_follow_table.c.follower_id,
        backref = "following"
    )