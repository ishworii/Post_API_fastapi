def test_current_user(client,test_user_token):
    response = client.get('/users/me',headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == "testuser"
    assert data['email'] == "test@test.com"
    assert data['id'] == 1

def test_signup(client):
    response = client.post(
        '/users/register',
        json={"username": "newuser", "password": "password", "email": "newuser@test.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == "newuser"
    assert data['email'] == "newuser@test.com"
    assert 'id' in data

def test_login(client):
    response = client.post(
        '/users/login',
        data={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == "bearer"

def test_get_all_users(client, test_user_token):
    response = client.get(
        '/users/', headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user['username'] == 'testuser' for user in data)

def test_get_user_by_id(client, test_user_token):
    response = client.get(
        '/users/1', headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == "testuser"
    assert data['email'] == "test@test.com"
    assert data['id'] == 1

def test_get_posts_by_user(client, test_user_token,create_posts_for_user):
    response = client.get(
        '/users/1/posts', headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for post in data:
        assert post['author_id'] == 1
