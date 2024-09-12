from fastapi import FastAPI, Depends, HTTPException, status
from . import crud, schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found"
        )
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
