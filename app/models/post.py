from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey("users.id"))
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)

    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all,delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    subscriptions = relationship(
        "Subscription", back_populates="post", cascade="all, delete-orphan"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="user_post_subscriber_unique"),
    )

    user = relationship("User", back_populates="subscriptions")
    post = relationship("Post", back_populates="subscriptions")
