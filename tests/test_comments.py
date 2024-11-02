def test_add_comment(client, test_user_token, create_posts_for_user):
    # Add a comment to the first post
    comment_data = {"content": "This is a test comment"}
    response = client.post('/posts/1/comments', json=comment_data, headers=test_user_token)
    assert response.status_code == 201
    data = response.json()
    assert data['content'] == "This is a test comment"
    assert data['post_id'] == 1
    assert 'id' in data


def test_get_comment(client, test_user_token, create_posts_for_user):
    # first add a comment
    comment_data = {"content": "This is another test comment"}
    add_response = client.post('/posts/1/comments', json=comment_data, headers=test_user_token)
    assert add_response.status_code == 201
    added_comment = add_response.json()

    response = client.get(f'/comments/{added_comment["id"]}', headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data['content'] == "This is another test comment"
    assert data['post_id'] == 1
    assert data['id'] == added_comment["id"]


def test_get_all_comments_by_user(client, test_user_token, create_posts_for_user):
    # Add some test comments for the test user
    comment_data_1 = {"content": "User's first comment"}
    comment_data_2 = {"content": "User's second comment"}

    client.post('/posts/1/comments', json=comment_data_1, headers=test_user_token)
    client.post('/posts/1/comments', json=comment_data_2, headers=test_user_token)

    # Get all comments
    response = client.get('/comments/me', headers=test_user_token)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(comment['content'] == "User's first comment" for comment in data)
    assert any(comment['content'] == "User's second comment" for comment in data)


def test_get_all_comments_for_post(client, test_user_token, create_posts_for_user):
    comment_data_1 = {"content": "First comment on post"}
    comment_data_2 = {"content": "Second comment on post"}

    client.post('/posts/1/comments', json=comment_data_1, headers=test_user_token)
    client.post('/posts/1/comments', json=comment_data_2, headers=test_user_token)

    response = client.get('/posts/1/comments', headers=test_user_token)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(comment['content'] == "First comment on post" for comment in data)
    assert any(comment['content'] == "Second comment on post" for comment in data)
