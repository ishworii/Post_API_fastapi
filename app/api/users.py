from fastapi import Depends, HTTPException, status, APIRouter
from app.api.deps import get_db, get_current_user
from app.crud.user import get_user_by_username, create_user
from app.schemas.user import UserRead, UserCreate
from app.models.user import User
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/register", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return create_user(db, user)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
