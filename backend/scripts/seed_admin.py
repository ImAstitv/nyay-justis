from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from passlib.context import CryptContext

from core.database import SessionLocal
from models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_admin(username: str, password: str, full_name: str) -> str:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        password_hash = pwd_context.hash(password)
        if existing:
            existing.password_hash = password_hash
            existing.role = "admin"
            existing.full_name = full_name
            action = "updated"
        else:
            db.add(
                User(
                    username=username,
                    password_hash=password_hash,
                    role="admin",
                    full_name=full_name,
                )
            )
            action = "created"
        db.commit()
        return action
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Create or update the initial hosted admin account.")
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--full-name", required=True)
    args = parser.parse_args()

    action = seed_admin(args.username.strip(), args.password, args.full_name.strip())
    print(f"Admin account {action}: {args.username}")


if __name__ == "__main__":
    main()
