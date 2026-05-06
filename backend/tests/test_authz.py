import pytest
from fastapi import HTTPException

from core.authz import ensure_case_not_disposed, require_case_owner, require_roles


class DummyCase:
    def __init__(self, citizen_username, status="Active"):
        self.citizen_username = citizen_username
        self.status = status


def test_require_roles_allows_matching_role():
    dependency = require_roles("judge", "lawyer")
    user = {"username": "judge1", "role": "judge"}

    result = dependency(user)

    assert result == user


def test_require_roles_rejects_non_matching_role():
    dependency = require_roles("judge")

    with pytest.raises(HTTPException) as exc_info:
        dependency({"username": "citizen1", "role": "citizen"})

    assert exc_info.value.status_code == 403


def test_require_case_owner_allows_owner():
    case = DummyCase(citizen_username="citizen1")
    user = {"username": "citizen1", "role": "citizen"}

    assert require_case_owner(case, user) is case


def test_require_case_owner_rejects_non_owner():
    case = DummyCase(citizen_username="citizen1")
    user = {"username": "citizen2", "role": "citizen"}

    with pytest.raises(HTTPException) as exc_info:
        require_case_owner(case, user)

    assert exc_info.value.status_code == 403


def test_ensure_case_not_disposed_rejects_disposed_case():
    case = DummyCase(citizen_username="citizen1", status="Disposed")

    with pytest.raises(HTTPException) as exc_info:
        ensure_case_not_disposed(case)

    assert exc_info.value.status_code == 409
