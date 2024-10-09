from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import auth, comment, posts, users
from app.db.base import Base
from app.db.session import engine
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post, Subscription
from app.models.user import User

load_dotenv(".env")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(comment.router, tags=["Comment"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Auth"])
