
def test_follow_user(client, test_user_token,test_admin_token):
    response = client.post("/follow/2", headers=test_user_token)
    assert response.status_code == 200
    assert response.json()["follower"]["username"] == "testuser"
    assert response.json()["following"]["username"] == "admin"


def test_cannot_follow_self(client, test_user_token):
    response = client.post("/follow/1", headers=test_user_token) 
    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot follow yourself."


def test_follow_user_not_found(client, test_user_token):
    response = client.post("/follow/999", headers=test_user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_unfollow_user(client, test_user_token, test_admin_token):
    client.post("/follow/2", headers=test_user_token) 

    response = client.delete("/unfollow/2", headers=test_user_token)
    assert response.status_code == 200
    assert response.json()["follower"]["username"] == "testuser"
    assert response.json()["following"]["username"] == "admin"


def test_unfollow_not_following(client, test_user_token, test_admin_token):
    response = client.delete("/unfollow/1", headers=test_user_token)  
    assert response.status_code == 400
    assert response.json()["detail"] == "You are not following this user."


def test_list_followers(client, test_user_token, test_admin_token):
    client.post("/follow/1", headers=test_admin_token)  

    response = client.get("/1/followers", headers=test_user_token)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "admin"


def test_list_following(client, test_user_token, test_admin_token):
    client.post("/follow/2", headers=test_user_token) 

    response = client.get("/1/following", headers=test_user_token)  
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "admin"
