from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.user import create_user, get_user_by_id, get_user_by_username, get_users
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.utils.hashing import hash_password, verify_password

router = APIRouter()


@router.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


@router.put("/", response_model=UserRead)
def update_user(
    new_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if new_user.username:
        current_user.username = new_user.username
    if new_user.email:
        current_user.email = new_user.email
    if new_user.full_name:
        current_user.full_name = new_user.full_name
    if new_user.password:
        if verify_password(new_user.password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password can not be the old password",
            )
        current_user.hashed_password = hash_password(new_user.password)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted"}


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    check_email = db.query(User).filter(User.email == user.email).first()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use",
        )

    return create_user(db, user)
