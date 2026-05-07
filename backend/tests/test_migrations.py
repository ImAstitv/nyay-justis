from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect

from core.config import settings

command = pytest.importorskip("alembic.command")
Config = pytest.importorskip("alembic.config").Config


def test_alembic_upgrade_creates_expected_schema(tmp_path):
    db_file = tmp_path / "migration_test.db"
    database_url = f"sqlite:///{db_file.as_posix()}"
    old_database_url = settings.DATABASE_URL
    backend_dir = Path(__file__).resolve().parents[1]
    settings.DATABASE_URL = database_url

    try:
        config = Config(str(backend_dir / "alembic.ini"))
        config.set_main_option("script_location", str(backend_dir / "migrations"))
        command.upgrade(config, "head")

        engine = create_engine(database_url)
        inspector = inspect(engine)
        tables = set(inspector.get_table_names())
        case_columns = {column["name"] for column in inspector.get_columns("cases")}

        assert {"users", "cases", "hearings", "audit_log"}.issubset(tables)
        assert {"status", "citizen_username", "filed_by_user_id"}.issubset(case_columns)
    finally:
        settings.DATABASE_URL = old_database_url
