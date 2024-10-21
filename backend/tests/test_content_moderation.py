def test_non_toxic_content(client, test_user_token):
    post_data = {
        "title": "Friendly Post",
        "content": "This is a positive and non-toxic post.",
    }

    response = client.post("/posts/", json=post_data, headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]


def test_toxic_content(client, test_user_token):
    post_data = {"title": "Toxic Post", "content": "I hate you! You're the worst!"}

    response = client.post("/posts/", json=post_data, headers=test_user_token)
    assert response.status_code == 400
    assert response.json()["detail"] == "Toxicity detected in the post"


def test_moderate_content(client, test_user_token):
    post_data = {
        "title": "Moderate Post",
        "content": "You're not great",
    }

    response = client.post("/posts/", json=post_data, headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
