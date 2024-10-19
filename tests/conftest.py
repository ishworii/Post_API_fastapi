import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.security import create_access_token
from app.crud.user import create_user
from app.db.base import Base
from app.main import app
from app.models.post import Post
from app.models.user import User
from app.schemas.user import UserCreate

SQLALCHEMY_DATABASE_URL = "postgresql://ishwor:password@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


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
        username="testuser", password="password", email="test@test.com", role="normal"
    )
    user = create_user(db, user_data)
    token = create_access_token({"sub": user.username})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def test_admin_token(client):
    db = TestingSessionLocal()
    user_data = UserCreate(
        username="admin", password="password", email="admin@admin.com", role="admin"
    )
    user = create_user(db, user_data)
    token = create_access_token({"sub": user.username})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def create_posts_for_user(client, test_user_token):
    post_data_1 = {"title": "Test Post 1", "content": "This is a test post."}
    post_data_2 = {"title": "Test Post 2", "content": "This is another test post."}

    client.post("/posts/", json=post_data_1, headers=test_user_token)
    client.post("/posts/", json=post_data_2, headers=test_user_token)
