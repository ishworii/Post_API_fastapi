def test_subscribe_to_post(
    client, test_user_token, test_admin_token, create_posts_for_user
):
    # Get a list of posts to find a post ID
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    posts = response.json()
    post_id = posts[0]["id"]

    # Subscribe to the post
    response = client.post(f"/posts/{post_id}/subscribe", headers=test_admin_token)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "subscribed successfully"
    assert data["post_id"] == post_id


def test_duplicate_subscription(
    client, test_user_token, test_admin_token, create_posts_for_user
):
    # Get a list of posts to find a post ID
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    posts = response.json()
    post_id = posts[0]["id"]

    # Subscribe to the post
    response = client.post(f"/posts/{post_id}/subscribe", headers=test_admin_token)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Already subscribed"


def test_unsubscribe_to_post(
    client, test_user_token, test_admin_token, create_posts_for_user
):
    # Get a list of posts to find a post ID
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    posts = response.json()
    post_id = posts[0]["id"]

    # Subscribe to the post
    response = client.post(f"/posts/{post_id}/unsubscribe", headers=test_admin_token)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Unsubscribed successfully"
    assert data["post_id"] == post_id


def test_duplicate_unsubscription(
    client, test_user_token, test_admin_token, create_posts_for_user
):
    # Get a list of posts to find a post ID
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    posts = response.json()
    post_id = posts[0]["id"]

    # Subscribe to the post
    response = client.post(f"/posts/{post_id}/unsubscribe", headers=test_admin_token)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Not subscribed"


def test_cannot_subscribe_unsubscribe_to_own_post(
    client, test_user_token, create_posts_for_user
):
    # Get a list of posts to find a post ID
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    posts = response.json()
    post_id = posts[0]["id"]

    # Subscribe to the post
    response = client.post(f"/posts/{post_id}/subscribe", headers=test_user_token)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Can not subscribe your own post"

    response = client.post(f"/posts/{post_id}/unsubscribe", headers=test_user_token)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Can not unsubscribe your own post"
