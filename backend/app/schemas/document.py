from datetime import datetime
from pydantic import BaseModel

class DocumentRead(BaseModel):
    id: int
    title: str
    path: str
    mime_type: str

    class Config:
        from_attributes = True

class DocumentVersionRead(BaseModel):
    id: int
    version: int
    path: str
    checksum: str
    created_at: datetime

    class Config:
        from_attributes = True

class AnnotationRead(BaseModel):
    id: int
    body: str
    is_resolved: bool

    class Config:
        from_attributes = True

class AnnotationCreate(BaseModel):
    body: str

class ManuscriptRead(BaseModel):
    id: int
    status: str
    submitted_at: datetime | None = None
    approved_by_supervisor: bool
    approved_by_hod: bool

    class Config:
        from_attributes = True

class PublicationRead(BaseModel):
    id: int
    title: str
    journal: str | None = None
    doi: str | None = None

    class Config:
        from_attributes = True
