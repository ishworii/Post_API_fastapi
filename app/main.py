import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from app.api import auth, comment, posts, users
from app.db.base import Base
from app.db.session import engine
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post, Subscription
from app.models.user import User

load_dotenv(".env")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis_url= os.getenv("REDIS_URL")
    redis_client = Redis.from_url(redis_url if redis_url else "") 

    try:
        # Test the connection
        await redis_client.ping()
        # Store the client in app state
        app.state.redis_client = redis_client
        print("Connected to Redis")
        yield
    finally:
        # Cleanup: Close the Redis connection when the server stops
        await redis_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(comment.router, tags=["Comment"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Auth"])
