from api import auth


def test_lawyer_can_create_case_without_public_party_account(client):
    client.app.dependency_overrides[auth.get_current_user] = lambda: {
        "id": 10,
        "username": "lawyer1",
        "role": "lawyer",
        "name": "Lawyer One",
    }

    response = client.post(
        "/cases",
        json={
            "case_id_number": "CRM/2026/1001",
            "primary_case_nature": "Criminal",
            "procedural_stage": "Pre-Trial",
            "petitioner": "State",
            "respondent": "Accused A",
        },
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["cnr"] == "CRM/2026/1001"


def test_public_case_status_route_is_removed(client):
    response = client.get("/citizen/search", params={"q": "CRM/2026/1001"})

    assert response.status_code == 404
