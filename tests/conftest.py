import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db, get_post_cache
from app.core.security import create_access_token
from app.crud.user import create_user
from app.db.base import Base
from app.main import app
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.user import User, UserRole
from app.schemas.user import UserCreate

load_dotenv(".env")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_TEST_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL or "")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
class MockRedis:
    async def set(*args,**kwargs):
        pass
    async def get(*args,**kwargs):
        pass
    async def delete(*args,**kwargs):
        pass
        


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_post_cache] = lambda : MockRedis()



@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(setup_db):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user_token(client):
    db = TestingSessionLocal()
    user_data = UserCreate(
        username="testuser", password="password", email="test@test.com", role=UserRole.normal
    )
    user = create_user(db, user_data)
    token = create_access_token({"sub": user.username})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def test_admin_token(client):
    db = TestingSessionLocal()
    user_data = UserCreate(
        username="admin", password="password", email="admin@admin.com", role=UserRole.admin
    )
    user = create_user(db, user_data)
    token = create_access_token({"sub": user.username})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def create_posts_for_user(client, test_user_token):
    post_data_1 = {"title": "Test Post 1", "content": "This is a test post.","tags" : [{"name" : "test"}]}
    post_data_2 = {"title": "Test Post 2", "content": "This is another test post.","tags" : [{"name" : "qa"}]}

    client.post("/posts/", json=post_data_1, headers=test_user_token)
    client.post("/posts/", json=post_data_2, headers=test_user_token)
