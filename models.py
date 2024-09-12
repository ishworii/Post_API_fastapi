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
    
