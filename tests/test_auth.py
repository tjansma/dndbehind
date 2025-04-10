def test_login_success(client, test_user):
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_invalid_credentials(client, test_user):
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get('/auth/whoami')
    assert response.status_code == 401


def test_protected_route_with_token(client, test_user):
    # First login to get token
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.json['access_token']

    # Test protected route with token
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/auth/whoami', headers=headers)
    assert response.status_code == 200
