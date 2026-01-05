from app.db.session import SessionLocal
from app import models
from app.core.security import get_password_hash

SEED_USERS = [
    {"email": "admin@example.com", "full_name": "Admin", "role": models.Role.ADMIN},
    {"email": "hod@example.com", "full_name": "Head of Dept", "role": models.Role.HOD},
    {"email": "supervisor@example.com", "full_name": "Supervisor", "role": models.Role.SUPERVISOR},
    {"email": "student@example.com", "full_name": "Student", "role": models.Role.STUDENT},
]

PASSWORD = "ChangeMe!123"


def seed() -> None:
    db = SessionLocal()
    try:
        for user in SEED_USERS:
            existing = db.query(models.User).filter(models.User.email == user["email"]).first()
            if existing:
                continue
            entity = models.User(
                email=user["email"],
                full_name=user["full_name"],
                role=user["role"],
                hashed_password=get_password_hash(PASSWORD),
            )
            db.add(entity)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
