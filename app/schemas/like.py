from enum import Enum

from pydantic import BaseModel


class LikeAction(str, Enum):
    like = "like"
    dislike = "dislike"


class LikeResponse(BaseModel):
    post_id: int
    user_id: int
    is_like: bool

    class Config:
        orm_mode = True


class PostLikeCount(BaseModel):
    post_id: int
    like_count: int
    dislike_count: int

    class Config:
        orm_mode = True
