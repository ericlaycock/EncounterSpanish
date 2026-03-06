from tests.conftest import register_user


def test_get_onboarding_status_initial(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/onboarding/status", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["onboarding_completed"] is False


def test_save_onboarding_selections(client, seed_data):
    _, headers = register_user(client)
    resp = client.post("/v1/onboarding/save-selections", headers=headers, json={
        "selected_category": "banking",
        "dialect": "mexico",
    })
    assert resp.status_code == 200
    # Verify status updated
    status_resp = client.get("/v1/onboarding/status", headers=headers)
    assert status_resp.json()["onboarding_completed"] is True


def test_get_available_categories(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/onboarding/available-categories", headers=headers)
    assert resp.status_code == 200
    categories = resp.json()["categories"]
    category_ids = [c["id"] for c in categories]
    assert "banking" in category_ids
    assert "restaurant" in category_ids
