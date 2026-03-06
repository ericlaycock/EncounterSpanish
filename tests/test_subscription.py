from tests.conftest import register_user


def test_get_subscription_status(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/subscription/status", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["active"] is False
    assert data["free_situations_limit"] == 25
    assert data["free_situations_remaining"] == 25
