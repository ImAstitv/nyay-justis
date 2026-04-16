from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_users():
    db: Session = SessionLocal()

    print("🧹 Deleting old users...")
    db.query(User).delete()   # 🔥 wipes all old bad users

    users = [
        ("judge", "judge123", "judge", "Hon. Justice R.K. Sharma"),
        ("lawyer", "lawyer123", "lawyer", "Adv. Priya Mishra"),
        ("citizen", "citizen123", "citizen", "Rajesh Kumar"),
    ]

    print("🌱 Seeding fresh users...")
    for username, password, role, name in users:
        db.add(User(
            username=username,
            password_hash=pwd_context.hash(password),  # ✅ proper hash
            role=role,
            full_name=name   # ⚠️ IMPORTANT: match your model field
        ))

    db.commit()
    db.close()

    print("✅ Users reset and seeded properly")