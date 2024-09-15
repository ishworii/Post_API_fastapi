from fastapi import FastAPI
from dotenv import load_dotenv
from app.db.session import engine
from app.db.base import Base
from app.api import posts, users, auth

load_dotenv(".env")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Auth"])


@app.get("/")
def root():
    return {"data": "Hello, world!"}
