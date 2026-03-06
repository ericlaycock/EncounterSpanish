from tests.conftest import register_user


def test_register_success(client):
    resp = client.post("/v1/auth/register", json={
        "email": "new@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "user_id" in data


def test_register_duplicate_email(client):
    register_user(client, email="dup@example.com")
    resp = client.post("/v1/auth/register", json={
        "email": "dup@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
    })
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"].lower()


def test_login_success(client):
    register_user(client, email="login@example.com")
    resp = client.post("/v1/auth/login", json={
        "email": "login@example.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    register_user(client, email="wrong@example.com")
    resp = client.post("/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword123",
    })
    assert resp.status_code == 401
