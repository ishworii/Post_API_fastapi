from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(String, nullable=True, default="admin")
    created_at = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey("users.id"))
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)

    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all,delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
