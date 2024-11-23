from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.normal


class UserRead(UserBase):
    id: int
    role: UserRole = UserRole.normal

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None

    class Config:
        orm_mode = True

class FollowResponse(BaseModel):
    follower : UserBase
    following : UserBase