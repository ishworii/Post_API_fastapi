from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str

    class Config:
        orm_mode = True


class CommentRead(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        orm_mode = True
