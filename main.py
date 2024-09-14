from fastapi import FastAPI, Depends, HTTPException, status
from . import crud, schemas, models, auth
from .database import SessionLocal, engine
from .dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv(".env")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"data": "Hello,world!"}


@app.get("/posts", response_model=list[schemas.Post], status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts


@app.get("/posts/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, id)
    return post


@app.post("/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    return crud.create_post(db, post)


@app.put(
    "/posts/{id}", response_model=schemas.Post, status_code=status.HTTP_201_CREATED
)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    return crud.update_post(db, post, id)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    crud.delete_post(db, id)


@app.post("/signup",response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return crud.create_user(db, user)


@app.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))),
    )
    return {"access_token":access_token,"token_type":"bearer","expires_in" : f"{os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")} minutes"}
