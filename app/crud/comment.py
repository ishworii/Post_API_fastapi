from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


def create_comment(
    db: Session, comment: CommentCreate, post_id: int, user_id: int
) -> Comment:
    db_comment = Comment(content=comment.content, post_id=post_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).all()


def get_comments_by_user(db: Session, user_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.user_id == user_id).all()


def get_comment(db: Session, comment_id: int) -> Comment:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def update_comment(db: Session, comment_id: int, content: str) -> Comment:
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment.content = content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()

def get_commenters_for_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
