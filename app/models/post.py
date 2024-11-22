from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Table,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship

from app.db.base import Base

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


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
    search_vector = Column(TSVECTOR, index=True)
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")


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
