from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    like_count: int | None = 0
    dislike_count: int | None = 0

    class Config:
        orm_mode = True
