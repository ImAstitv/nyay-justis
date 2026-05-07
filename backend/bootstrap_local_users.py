from passlib.context import CryptContext

from core.config import settings
from core.database import SessionLocal
from models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_USERS = [
    {
        "username": "judge",
        "password": "judge123",
        "role": "judge",
        "full_name": "Hon. Justice R.K. Sharma",
    },
    {
        "username": "lawyer",
        "password": "lawyer123",
        "role": "lawyer",
        "full_name": "Adv. Priya Mishra",
    },
    {
        "username": "citizen",
        "password": "citizen123",
        "role": "citizen",
        "full_name": "Rajesh Kumar",
    },
]


def upsert_local_users():
    if not settings.ALLOW_LOCAL_BOOTSTRAP:
        raise SystemExit("Local bootstrap is disabled. Set ALLOW_LOCAL_BOOTSTRAP=true to use this script.")
    if not settings.DATABASE_URL.startswith("sqlite"):
        raise SystemExit("Local bootstrap is only allowed for SQLite development databases.")

    db = SessionLocal()
    created = 0
    updated = 0

    try:
        for entry in DEFAULT_USERS:
            user = db.query(User).filter(User.username == entry["username"]).first()
            password_hash = pwd_context.hash(entry["password"])

            if user is None:
                db.add(
                    User(
                        username=entry["username"],
                        password_hash=password_hash,
                        role=entry["role"],
                        full_name=entry["full_name"],
                    )
                )
                created += 1
            else:
                user.password_hash = password_hash
                user.role = entry["role"]
                user.full_name = entry["full_name"]
                updated += 1

        db.commit()
    finally:
        db.close()

    print(f"Local users ready. Created: {created}, Updated: {updated}")
    print("Credentials:")
    for entry in DEFAULT_USERS:
        print(f"  {entry['role']}: {entry['username']} / {entry['password']}")


if __name__ == "__main__":
    upsert_local_users()
