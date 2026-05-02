from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
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


@router.post("/login")
def login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not pwd_context.verify(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username, "role": user.role, "name": user.full_name})
    _set_session_cookie(response, token)
    return {"role": user.role, "name": user.full_name, "username": user.username}


@router.post("/logout")
def logout(response: Response):
    _clear_session_cookie(response)
    return {"status": "logged_out"}


@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return user
