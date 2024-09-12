from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str | None = "ishwor"

    class Config:
        orm_mode = True
