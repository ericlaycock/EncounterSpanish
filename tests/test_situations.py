from tests.conftest import register_user


def test_list_situations(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/situations", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]["id"] == "banking_1"


def test_get_situation_detail(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/situations/banking_1", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "banking_1"
    assert data["free"] is True
    assert len(data["words"]) > 0


def test_start_situation(client, seed_data):
    _, headers = register_user(client)
    resp = client.post("/v1/situations/banking_1/start", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "words" in data
    assert len(data["words"]) > 0


def test_complete_situation(client, seed_data):
    _, headers = register_user(client)
    # Must start before completing
    client.post("/v1/situations/banking_1/start", headers=headers)
    resp = client.post("/v1/situations/banking_1/complete", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    # Should suggest next situation in banking series
    assert "next_situation_id" in data
