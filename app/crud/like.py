from sqlalchemy.orm import Session

from app.models.like import Like
from app.models.post import Post
from app.models.user import User


def like_post(db: Session, user: User, post: Post):
    like_record = (
        db.query(Like).filter(Like.user_id == user.id, Like.post_id == post.id).first()
    )

    if like_record:
        if like_record.is_like:
            db.delete(like_record)
            post.like_count -= 1
        else:
            like_record.is_like = True
            post.like_count += 1
            post.dislike_count -= 1
    else:
        new_like = Like(user_id=user.id, post_id=post.id, is_like=True)
        db.add(new_like)
        post.like_count += 1
    db.commit()
    db.refresh(post)


def dislike_post(db: Session, user: User, post: Post):
    like_record = (
        db.query(Like).filter(Like.user_id == user.id, Like.post_id == post.id).first()
    )

    if like_record:
        if not like_record.is_like:
            db.delete(like_record)
            post.dislike_count -= 1
        else:
            like_record.is_like = False
            post.dislike_count += 1
            post.like_count -= 1
    else:
        new_dislike = Like(user_id=user.id, post_id=post.id, is_like=False)
        db.add(new_dislike)
        post.dislike_count += 1
    db.commit()
    db.refresh(post)
