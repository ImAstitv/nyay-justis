from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import create_engine, inspect, text

from core.config import settings


def main():
    if not settings.DATABASE_URL.startswith("postgresql+psycopg2://"):
        raise SystemExit("DATABASE_URL must be a postgresql+psycopg2:// URL")

    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            database_name = conn.execute(text("select current_database()")).scalar_one()
            user_name = conn.execute(text("select current_user")).scalar_one()
            inspector = inspect(conn)
            tables = set(inspector.get_table_names())
    finally:
        engine.dispose()

    expected_tables = {"users", "cases", "hearings", "audit_log"}
    missing_tables = expected_tables - tables
    if missing_tables:
        raise SystemExit(f"PostgreSQL is reachable, but migrations are missing tables: {sorted(missing_tables)}")

    print(f"PostgreSQL smoke OK: database={database_name}, user={user_name}, tables={sorted(expected_tables)}")


if __name__ == "__main__":
    main()
