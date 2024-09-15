from pydantic import BaseModel, EmailStr
from app.schemas.post import PostRead


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    posts: list[PostRead] = []

    class Config:
        orm_mode = True
