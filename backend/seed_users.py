from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_users():
    db: Session = SessionLocal()

    users = [
        ("judge", "judge123", "judge", "Hon. Justice R.K. Sharma"),
        ("lawyer", "lawyer123", "lawyer", "Adv. Priya Mishra"),
        ("citizen", "citizen123", "citizen", "Rajesh Kumar"),
    ]

    for username, password, role, name in users:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            db.add(User(
                username=username,
                password_hash=pwd_context.hash(password),
                role=role,
                name=name
            ))

    db.commit()
    db.close()
    print("✅ Users seeded")