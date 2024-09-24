def test_create_post(client, test_user_token):
    response = client.post(
        "/posts/",
        json={"title": "New Post", "content": "Content of the new post."},
        headers=test_user_token,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "Content of the new post."

def test_get_all_post(client,test_user_token):
    response = client.get("/posts/",headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)
    assert data[0]["title"] == "New Post"
    assert data[0]["content"] == "Content of the new post."


def test_get_post_by_id(client, test_user_token):
    response = client.get("/posts/1", headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "New Post"


def test_get_all_posts(client, test_user_token):
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_post(client, test_user_token):
    response = client.put(
        "/posts/1",
        json={"title": "Updated Title", "content": "Updated content."},
        headers=test_user_token,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content."


def test_delete_post(client, test_user_token):
    response = client.delete("/posts/1", headers=test_user_token)
    assert response.status_code == 204
