from datetime import date, datetime
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    supervisor_id: int | None = None
    hod_id: int | None = None

class ProjectRead(ProjectCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

class MilestoneRead(BaseModel):
    id: int
    title: str
    due_date: date | None = None
    status: str

    class Config:
        from_attributes = True

class MeetingRead(BaseModel):
    id: int
    title: str
    agenda: str | None = None
    scheduled_for: datetime

    class Config:
        from_attributes = True

class MeetingCreate(BaseModel):
    title: str
    agenda: str | None = None
    scheduled_for: datetime

class MeetingMinutesRead(BaseModel):
    id: int
    summary: str
    action_items: str | None = None

    class Config:
        from_attributes = True

class MeetingMinutesCreate(BaseModel):
    summary: str
    action_items: str | None = None
