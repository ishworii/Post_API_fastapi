from pydantic import BaseModel
from app.schemas.tag import TagRead, TagCreate


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    tags: list[TagCreate]


class PostRead(PostBase):
    id: int
    like_count: int | None = 0
    dislike_count: int | None = 0
    author_id: int
    tags: list[TagRead]

    class Config:
        orm_mode = True
