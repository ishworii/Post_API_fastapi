from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud import post
from app.models.user import User
from app.schemas.post import PostCreate, PostRead

router = APIRouter()


@router.get("/", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db)):
    posts = post.get_posts(db)
    return posts


@router.get("/{id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    pst = post.get_post(db, id)
    return pst


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post_create: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post.create_post(db, post_create, current_user.id)


@router.put("/{id}", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def update_post(
    id: int,
    post_read: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return post.update_post(db, post_read, id, current_user.id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post.delete_post(db, id)
