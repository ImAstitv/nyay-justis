import os

from core.config import Settings


def test_normalizes_render_style_postgres_url():
    settings = Settings(
        DATABASE_URL="postgres://user:pass@localhost:5432/nyay_justis",
        SECRET_KEY="secret",
    )

    assert settings.DATABASE_URL == "postgresql+psycopg2://user:pass@localhost:5432/nyay_justis"


def test_keeps_sqlite_url_unchanged():
    settings = Settings(
        DATABASE_URL="sqlite:///./nyay.db",
        SECRET_KEY="secret",
    )

    assert settings.DATABASE_URL == "sqlite:///./nyay.db"
