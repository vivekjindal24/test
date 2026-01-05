from app import models
from sqlalchemy.orm import Session

async def audit_action(db: Session, user: models.User | None, action: str, resource: str, metadata: dict | None = None) -> None:
    entry = models.AuditLog(user_id=user.id if user else None, action=action, resource=resource, metadata=metadata or {})
    db.add(entry)
    db.commit()
