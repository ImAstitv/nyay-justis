from typing import Iterable

from fastapi import Depends, HTTPException

from api.auth import get_current_user


def _role_list(roles: Iterable[str]) -> str:
    return ", ".join(sorted(roles))


def require_roles(*roles: str):
    allowed_roles = set(roles)

    def dependency(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Requires one of roles: {_role_list(allowed_roles)}",
            )
        return user

    return dependency


def require_case_owner(case, user):
    if case.citizen_username != user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this case")
    return case


def ensure_case_not_disposed(case):
    if case.status == "Disposed":
        raise HTTPException(status_code=409, detail="Disposed cases cannot be modified")
    return case
