from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.services.storage import StorageService
from app.services.audit import audit_action

router = APIRouter()
storage = StorageService()

@router.post("/{project_id}", response_model=schemas.DocumentRead)
async def upload_document(project_id: int, title: str, mime_type: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(require_role(models.Role.STUDENT, models.Role.SUPERVISOR, models.Role.HOD, models.Role.ADMIN))):
    project = db.get(models.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    object_path = await storage.save(file=file, project_id=project_id, user_id=current_user.id)
    document = models.Document(project_id=project_id, title=title, path=object_path, mime_type=mime_type)
    db.add(document)
    db.commit()
    db.refresh(document)
    await audit_action(db=db, user=current_user, action="upload", resource="document", metadata={"document_id": document.id})
    return document

@router.get("/{project_id}", response_model=List[schemas.DocumentRead])
def list_documents(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Document).filter(models.Document.project_id == project_id).all()

@router.post("/{document_id}/annotations", response_model=schemas.AnnotationRead)
def add_annotation(document_id: int, payload: schemas.AnnotationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    annotation = models.Annotation(document_id=document_id, author_id=current_user.id, body=payload.body, is_resolved=False)
    db.add(annotation)
    db.commit()
    db.refresh(annotation)
    return annotation
