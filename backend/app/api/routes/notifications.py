from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.api.deps import get_current_user
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.NotificationRead])
def list_notifications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()
