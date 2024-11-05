def test_like_post_twice(client, test_user_token, create_posts_for_user):
    # Like the first post
    response = client.post("/posts/1/like", headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is True

    # Try to like the same post again,will nullify the first like
    response = client.post("/posts/1/like", headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is False

    # Verify the like count is 0
    response = client.get("/posts/1", headers=test_user_token)
    post = response.json()
    assert post["like_count"] == 0
    assert post["dislike_count"] == 0


def test_dislike_post_twice(client, test_user_token, create_posts_for_user):
    # Dislike the first post
    response = client.post("/posts/1/dislike", headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is False

    # Try to dislike the same post again
    response = client.post("/posts/1/dislike", headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is False

    # Verify the dislike count at 0
    response = client.get("/posts/1", headers=test_user_token)
    post = response.json()
    assert post["dislike_count"] == 0
    assert post["like_count"] == 0


def test_like_post_once(client, test_admin_token, create_posts_for_user):
    response = client.post("/posts/1/like", headers=test_admin_token)
    print(client.get("/posts/1", headers=test_admin_token).json())
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is True

    response = client.get(f"/posts/{data['post_id']}", headers=test_admin_token)
    post = response.json()
    print(response.json())
    assert post["like_count"] == 1
    assert post["dislike_count"] == 0


def test_dislike_post_once(client, test_admin_token, create_posts_for_user):
    response = client.post("/posts/1/dislike", headers=test_admin_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is False

    response = client.get("/posts/1", headers=test_admin_token)
    post = response.json()
    assert post["dislike_count"] == 1
    assert post["like_count"] == 0


def test_like_then_dislike(client, test_admin_token, create_posts_for_user):
    # Like the first post
    response = client.post("/posts/1/like", headers=test_admin_token)
    assert response.status_code == 201

    # Now dislike the same post
    response = client.post("/posts/1/dislike", headers=test_admin_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is False

    # Verify the like and dislike count
    response = client.get("/posts/1", headers=test_admin_token)
    post = response.json()
    assert post["like_count"] == 0
    assert post["dislike_count"] == 1


def test_dislike_then_like(client, test_admin_token, create_posts_for_user):
    # Dislike the first post
    response = client.post("/posts/1/dislike", headers=test_admin_token)
    assert response.status_code == 201

    # Now like the same post
    response = client.post("/posts/1/like", headers=test_admin_token)
    assert response.status_code == 201
    data = response.json()
    assert data["is_like"] is True

    # Verify the like and dislike count
    response = client.get("/posts/1", headers=test_admin_token)
    post = response.json()
    assert post["like_count"] == 1
    assert post["dislike_count"] == 0
