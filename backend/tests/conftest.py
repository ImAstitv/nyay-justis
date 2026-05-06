import os
from pathlib import Path

import pytest


TEST_DATABASE_URL = "sqlite:///./test_backend.db"
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)

from core.database import Base, SessionLocal, engine  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def cleanup_sqlite_file():
    yield
    engine.dispose()
    db_path = Path("test_backend.db")
    if db_path.exists():
        db_path.unlink()
