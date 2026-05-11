import pytest
from fastapi import HTTPException

from core.authz import ensure_case_not_disposed, require_roles


class DummyCase:
    def __init__(self, status="Active"):
        self.status = status


def test_require_roles_allows_matching_role():
    dependency = require_roles("judge", "lawyer")
    user = {"username": "judge1", "role": "judge"}

    result = dependency(user)

    assert result == user


def test_require_roles_rejects_non_matching_role():
    dependency = require_roles("judge")

    with pytest.raises(HTTPException) as exc_info:
        dependency({"username": "lawyer1", "role": "lawyer"})

    assert exc_info.value.status_code == 403


def test_ensure_case_not_disposed_rejects_disposed_case():
    case = DummyCase(status="Disposed")

    with pytest.raises(HTTPException) as exc_info:
        ensure_case_not_disposed(case)

    assert exc_info.value.status_code == 409
