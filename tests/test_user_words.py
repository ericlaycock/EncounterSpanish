from tests.conftest import register_user


def test_get_user_words_empty(client, seed_data):
    _, headers = register_user(client)
    resp = client.get("/v1/user/words", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_mark_typed_correct(client, seed_data):
    _, headers = register_user(client)
    # Start a situation first to create user_words
    client.post("/v1/situations/banking_1/start", headers=headers)
    resp = client.post("/v1/user/words/typed-correct", headers=headers, json={
        "word_ids": ["enc_1"],
    })
    assert resp.status_code == 200
    # Verify count incremented
    words_resp = client.get("/v1/user/words", headers=headers)
    enc_1 = next(w for w in words_resp.json() if w["word_id"] == "enc_1")
    assert enc_1["typed_correct_count"] == 1
