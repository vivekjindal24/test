from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.api.deps import get_current_user, require_role
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.ProjectRead)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(models.Role.STUDENT))):
    project = models.Project(title=payload.title, description=payload.description, owner_id=current_user.id, supervisor_id=payload.supervisor_id, hod_id=payload.hod_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=List[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    q = db.query(models.Project)
    if current_user.role == models.Role.STUDENT:
        q = q.filter(models.Project.owner_id == current_user.id)
    return q.all()

@router.post("/{project_id}/milestones/{milestone_id}/complete")
def complete_milestone(project_id: int, milestone_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(models.Role.SUPERVISOR, models.Role.HOD, models.Role.ADMIN))):
    milestone = db.get(models.Milestone, milestone_id)
    if not milestone or milestone.project_id != project_id:
        raise HTTPException(status_code=404, detail="Milestone not found")
    milestone.status = "done"
    db.commit()
    return {"status": "ok"}

@router.post("/{project_id}/meetings", response_model=schemas.MeetingRead)
def schedule_meeting(project_id: int, meeting: schemas.MeetingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(models.Role.SUPERVISOR, models.Role.HOD, models.Role.ADMIN))):
    entity = models.Meeting(project_id=project_id, title=meeting.title, agenda=meeting.agenda, scheduled_for=meeting.scheduled_for)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

@router.post("/{project_id}/meetings/{meeting_id}/minutes", response_model=schemas.MeetingMinutesRead)
def add_minutes(project_id: int, meeting_id: int, body: schemas.MeetingMinutesCreate, db: Session = Depends(get_db), current_user: models.User = Depends(require_role(models.Role.SUPERVISOR, models.Role.HOD, models.Role.ADMIN))):
    meeting = db.get(models.Meeting, meeting_id)
    if not meeting or meeting.project_id != project_id:
        raise HTTPException(status_code=404, detail="Meeting not found")
    minutes = models.MeetingMinutes(meeting_id=meeting_id, summary=body.summary, action_items=body.action_items)
    db.add(minutes)
    db.commit()
    db.refresh(minutes)
    return minutes
