from api import auth
from models.models import User


def _as_user(role: str):
    return {
        "id": 1,
        "username": f"{role}1",
        "role": role,
        "name": f"{role.title()} One",
    }


def test_admin_can_create_lawyer_account(client):
    client.app.dependency_overrides[auth.get_current_user] = lambda: _as_user("admin")

    response = client.post(
        "/auth/users",
        json={
            "username": "lawyer_new",
            "password": "password123",
            "role": "lawyer",
            "full_name": "Adv. New User",
        },
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["role"] == "lawyer"


def test_judge_cannot_create_accounts(client):
    client.app.dependency_overrides[auth.get_current_user] = lambda: _as_user("judge")

    response = client.post(
        "/auth/users",
        json={
            "username": "blocked_user",
            "password": "password123",
            "role": "lawyer",
            "full_name": "Blocked User",
        },
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 403


def test_citizen_role_is_not_accepted_for_new_accounts(client):
    client.app.dependency_overrides[auth.get_current_user] = lambda: _as_user("admin")

    response = client.post(
        "/auth/users",
        json={
            "username": "public_user",
            "password": "password123",
            "role": "citizen",
            "full_name": "Public User",
        },
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 400


def test_admin_can_list_users(client, db_session):
    db_session.add(
        User(
            username="judge_roster",
            password_hash="hashed",
            role="judge",
            full_name="Judge Roster",
        )
    )
    db_session.commit()
    client.app.dependency_overrides[auth.get_current_user] = lambda: _as_user("admin")

    response = client.get("/auth/users")

    client.app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()[0]["username"] == "judge_roster"
