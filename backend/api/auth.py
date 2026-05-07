from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from models.models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SESSION_COOKIE_NAME = "nyay_session"


def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm="HS256")


def _set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_HOURS * 3600,
        domain=settings.COOKIE_DOMAIN,
        path="/",
    )


def _clear_session_cookie(response: Response):
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/",
    )


def _read_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()

    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        return token

    raise HTTPException(status_code=401, detail="Authentication required")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = _read_token(request)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        role = payload.get("role")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "id": user.id,
            "username": username,
            "role": role,
            "name": user.full_name,
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class UserCreatePayload(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: str
    full_name: str = Field(min_length=1, max_length=200)


class PasswordChangePayload(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


ALLOWED_ROLES = {"judge", "lawyer", "citizen"}


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/login")
def login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not pwd_context.verify(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username, "role": user.role, "name": user.full_name})
    _set_session_cookie(response, token)
    return {"role": user.role, "name": user.full_name, "username": user.username}


@router.post("/users")
def create_user(payload: UserCreatePayload, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "judge":
        raise HTTPException(status_code=403, detail="Only judges can create user accounts")
    if payload.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {', '.join(sorted(ALLOWED_ROLES))}")

    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = User(
        username=payload.username,
        password_hash=_hash_password(payload.password),
        role=payload.role,
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role, "full_name": user.full_name}


@router.post("/change-password")
def change_password(payload: PasswordChangePayload, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(payload.current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    if payload.current_password == payload.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the current password")

    user.password_hash = _hash_password(payload.new_password)
    db.commit()
    return {"status": "password_updated"}


@router.post("/logout")
def logout(response: Response):
    _clear_session_cookie(response)
    return {"status": "logged_out"}


@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user
