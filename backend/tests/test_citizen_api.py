from datetime import datetime

from api import auth
from models.models import Case, Hearing, User


def _seed_case_data(db_session):
    citizen = User(
        username="citizen1",
        password_hash="hashed",
        role="citizen",
        full_name="Citizen One",
    )
    other_citizen = User(
        username="citizen2",
        password_hash="hashed",
        role="citizen",
        full_name="Citizen Two",
    )
    db_session.add_all([citizen, other_citizen])
    db_session.flush()

    owned_case = Case(
        cnr_number="CRM/2026/0001",
        citizen_username="citizen1",
        filed_by_user_id=citizen.id,
        primary_case_nature="Criminal",
        current_stage="Pre-Trial",
        filing_date=datetime.utcnow(),
        under_sections="302",
        petitioner="State",
        respondent="Accused A",
    )
    foreign_case = Case(
        cnr_number="CRM/2026/0002",
        citizen_username="citizen2",
        filed_by_user_id=other_citizen.id,
        primary_case_nature="Criminal",
        current_stage="Evidence",
        filing_date=datetime.utcnow(),
        under_sections="420",
        petitioner="State",
        respondent="Accused B",
    )
    db_session.add_all([owned_case, foreign_case])
    db_session.flush()

    db_session.add(
        Hearing(
            case_id=owned_case.id,
            purpose_of_hearing="Adjourned",
            adjournment_reason="Documents pending",
            business_on_date=datetime.utcnow(),
        )
    )
    db_session.commit()


def test_citizen_can_fetch_owned_case(client, db_session):
    _seed_case_data(db_session)
    client.app.dependency_overrides[auth.get_current_user] = lambda: {
        "id": 1,
        "username": "citizen1",
        "role": "citizen",
        "name": "Citizen One",
    }

    response = client.get("/citizen/search", params={"q": "CRM/2026/0001"})

    client.app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["case_id_number"] == "CRM/2026/0001"
    assert data[0]["timeline"][0]["event"] == "Adjourned"


def test_citizen_cannot_fetch_other_users_case(client, db_session):
    _seed_case_data(db_session)
    client.app.dependency_overrides[auth.get_current_user] = lambda: {
        "id": 1,
        "username": "citizen1",
        "role": "citizen",
        "name": "Citizen One",
    }

    response = client.get("/citizen/search", params={"q": "CRM/2026/0002"})

    client.app.dependency_overrides.clear()
    assert response.status_code == 403


def test_non_citizen_cannot_use_citizen_search(client, db_session):
    _seed_case_data(db_session)
    client.app.dependency_overrides[auth.get_current_user] = lambda: {
        "id": 10,
        "username": "judge1",
        "role": "judge",
        "name": "Judge One",
    }

    response = client.get("/citizen/search", params={"q": "CRM/2026/0001"})

    client.app.dependency_overrides.clear()
    assert response.status_code == 403
