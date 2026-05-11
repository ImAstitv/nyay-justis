from api import auth, ocr


def _as_user():
    return {
        "id": 1,
        "username": "admin1",
        "role": "admin",
        "name": "Admin One",
    }


def test_translation_endpoint_returns_fallback_when_pipeline_disabled(client, monkeypatch):
    client.app.dependency_overrides[auth.get_current_user] = _as_user
    monkeypatch.setattr(ocr.settings, "ENABLE_MULTILINGUAL_PIPELINE", False)

    response = client.post(
        "/ocr/translate",
        json={"text": "नमस्ते", "target_language": "English"},
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["translated_text"] == "नमस्ते"
    assert response.json()["provider"] == "disabled"
