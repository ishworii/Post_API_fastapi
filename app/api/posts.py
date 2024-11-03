from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_post_cache
from app.crud import like, post
from app.models.like import Like
from app.models.post import Post, Subscription
from app.models.user import User, UserRole
from app.schemas.like import Action
from app.schemas.post import PostCreate, PostRead
from app.api.deps import PostCache


router = APIRouter()


@router.get("/", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_all_posts(
    db: Session = Depends(get_db),
    author_id: int = Query(None, description="Filter by author id"),
    min_likes: int = Query(None, description="Filter by minimum number of likes"),
    title: str = Query(None, description="Filter by title"),
):
    query = db.query(Post)
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if min_likes:
        query = query.filter(Post.like_count >= min_likes)
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))
    posts = query.all()
    return posts


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post_create: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return post.create_post(db, post_create, current_user.id)


@router.get("/search")
async def search_posts(query: str, db: Session = Depends(get_db)):
    sql_query = """
        SELECT * 
        FROM post 
        WHERE search_vector @@ plainto_tsquery('english', :query)
        ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query)) DESC;
    """
    result = db.execute(text(sql_query), {"query": query}).fetchall()

    posts = [
        {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3].isoformat(),
            "author_id": row[4],
            "like_count": row[5],
            "dislike_count": row[6],
        }
        for row in result
    ]

    return posts


@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Session = Depends(get_db),cache:PostCache=Depends(get_post_cache)):
    cache_key = str(post_id)
    if cached_data := await cache.get(cache_key):
        return PostRead(**cached_data)
    pst = post.get_post(db, post_id)
    await cache.set(cache_key,pst)
    return pst


@router.put("/{post_id}", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def update_post(
    post_id: int,
    post_read: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cache : PostCache = Depends(get_post_cache)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.author_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    db_post.title = post_read.title
    db_post.content = post_read.content
    db_post.author_id = current_user.id
    db.commit()
    db.refresh(db_post)
    await cache.delete(str(post_id))
    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cache : PostCache = Depends(get_post_cache),
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.author_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    db.delete(db_post)
    db.commit()
    await cache.delete(str(post.id))
    return {"detail": "Post deleted"}


# like/dislike/subscribe/unsubscribe a post
@router.post("/{id}/{action}", status_code=status.HTTP_201_CREATED)
def like_dislike_post(
    id: int,
    action: Action,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_a_post = post.get_post(db, id)
    if not get_a_post:
        raise HTTPException(status_code=404, detail="detail not found")
    if action == Action.like:
        like.like_post(db, current_user, get_a_post)
    elif action == Action.dislike:
        like.dislike_post(db, current_user, get_a_post)
    elif action == Action.subscribe:
        if current_user.id == get_a_post.author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not subscribe your own post",
            )
        subscription = (
            db.query(Subscription)
            .filter_by(post_id=get_a_post.id, user_id=current_user.id)
            .first()
        )
        if subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Already subscribed"
            )
        new_subscription = Subscription(user_id=current_user.id, post_id=get_a_post.id)
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return {
            "message": "subscribed successfully",
            "user_id": current_user.id,
            "post_id": get_a_post.id,
        }
    elif action == Action.unsubscribe:
        if current_user.id == get_a_post.author_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not unsubscribe your own post",
            )
        subscription = (
            db.query(Subscription)
            .filter_by(post_id=get_a_post.id, user_id=current_user.id)
            .first()
        )
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not subscribed"
            )
        db.delete(subscription)
        db.commit()
        return {
            "message": "Unsubscribed successfully",
            "post_id": get_a_post.id,
            "user_id": current_user.id,
        }

    like_record = (
        db.query(Like)
        .filter(Like.user_id == current_user.id, Like.post_id == get_a_post.id)
        .first()
    )
    is_like = like_record.is_like if like_record else False

    return {"post_id": get_a_post.id, "user_id": current_user.id, "is_like": is_like}
