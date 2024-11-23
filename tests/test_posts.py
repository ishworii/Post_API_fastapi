def test_create_post(client, test_user_token,create_posts_for_user):
    response = client.post(
        "/posts/",
        json={"title": "New Post", "content": "Content of the new post.","tags":[{"name" : "content"}]},
        headers=test_user_token,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "Content of the new post."
    
    assert data["tags"][0]['name'] == "content"


def create_admin_test_post(client, test_admin_token):
    post_data_1 = {
        "title": "Test Post 1 Admin",
        "content": "This is a test post by admin.",
        "tags" : [{"name" : "admin"}]
    }
    return client.post("/posts/", json=post_data_1, headers=test_admin_token).json()


def test_get_all_post(client, test_user_token,create_posts_for_user):
    response = client.get("/posts/", headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)
    assert data[0]["title"] == "Test Post 1"
    assert data[0]["content"] == "This is a test post."


def test_get_post_by_id(client, test_user_token,create_posts_for_user):
    response = client.get("/posts/1", headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_update_post(client, test_user_token):
    response = client.put(
        "/posts/1",
        json={"title": "Updated Title", "content": "Updated content.","tags" : [{"name" : "update"}]},
        headers=test_user_token,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content."
    assert data["tags"][0]['name'] == "update"


def test_delete_post(client, test_user_token):
    response = client.delete("/posts/1", headers=test_user_token)
    assert response.status_code == 204


def test_normal_user_cannot_edit_others_post(client, test_user_token, test_admin_token):
    # Normal user tries to edit the admin's post
    admin_post = create_admin_test_post(client, test_admin_token)
    edit_data = {"title": "Normal User's Edit", "content": "Normal User tries to edit","tags":[{"name":"update"}]}
    response = client.put(
        f"/posts/{admin_post['id']}",
        json=edit_data,
        headers=test_user_token,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_normal_user_cannot_delete_others_post(
    client, test_user_token, test_admin_token
):
    # Normal user tries to delete the admin's post
    admin_post = create_admin_test_post(client, test_admin_token)
    response = client.delete(
        f"/posts/{admin_post['id']}",
        headers=test_user_token,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_admin_user_can_edit_any_post(client, test_admin_token):
    # Admin tries to edit any post
    edit_data = {"title": "Admin User's Edit", "content": "Admin User tries to edit","tags":[{"name":"admin"}]}
    response = client.put(
        "/posts/2",
        json=edit_data,
        headers=test_admin_token,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Admin User's Edit"
    assert data["content"] == "Admin User tries to edit"


def test_admin_user_can_delete_others_post(client, test_admin_token):
    # admin user tries to delete any post
    response = client.delete(
        "/posts/2",
        headers=test_admin_token,
    )
    assert response.status_code == 204
