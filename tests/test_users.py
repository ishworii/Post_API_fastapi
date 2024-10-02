def test_current_user(client, normal_user_token):
    response = client.get("/users/me", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "normaluser"
    assert data["email"] == "normaluser@example.com"
    assert data["id"] == 1


def test_signup(client):
    response = client.post(
        "/users/register",
        json={
            "username": "newuser",
            "password": "password",
            "email": "newuser@test.com",
            "role": "normal",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@test.com"
    assert "id" in data


def test_login(client):
    response = client.post(
        "/users/login", data={"username": "normaluser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_all_users(client, normal_user_token):
    response = client.get("/users/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["username"] == "testuser" for user in data)


def test_get_user_by_id(client, normal_user_token):
    response = client.get("/users/1", headers=normal_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@test.com"
    assert data["id"] == 1


def test_get_posts_by_user(client, normal_user_token, create_posts_for_user):
    response = client.get("/posts?author_id=1", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for post in data:
        assert post["author_id"] == 1


def create_test_user(client, sign_up=False):
    user_data = {
        "username": "new_test_user",
        "email": "new_test_user@example.com",
        "password": "password123",
        "full_name": "Test User",
    }
    # signup
    if sign_up:
        client.post("/users/register", json=user_data)
    login_data = {"username": "new_test_user", "password": "password123"}
    login_response = client.post("/users/login", data=login_data)
    data = login_response.json()
    return data['access_token']


def test_update_user(client):
    access_token = create_test_user(client, sign_up=True)
    new_user_data = {
        "username": "new_username",
        "email": "newemail@example.com",
        "full_name": "New Full Name",
    }

    response = client.put("/users/", json=new_user_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    updated_user = response.json()
    assert updated_user["username"] == "new_username"
    assert updated_user["email"] == "newemail@example.com"
    assert updated_user["full_name"] == "New Full Name"


def test_update_user_password(client):
    access_token = create_test_user(client)

    new_password_data = {"password": "newpassword123"}
    response = client.put("/users/", json=new_password_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    login_data = {"username": "testuser", "password": "newpassword123"}
    login_response = client.post("/users/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_update_user_partial(client):
    # access_token = create_test_user(client)

    partial_update_data = {
        "username": "new_username",
        "email": "partialupdate@example.com",
    }

    response = client.put("/users/", json=partial_update_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    updated_user = response.json()
    assert updated_user["email"] == "partialupdate@example.com"


def test_delete_user(client):
    access_token = create_test_user(client)

    response = client.delete("/users/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204

    user_response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert user_response.status_code == 401
