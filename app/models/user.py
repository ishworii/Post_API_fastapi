from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


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
    posts = relationship("Post", back_populates="author", cascade="all,delete-orphan")
