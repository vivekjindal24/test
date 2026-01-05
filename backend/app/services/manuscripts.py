from sqlalchemy.orm import Session
from app import models

class ManuscriptService:
    def submit(self, db: Session, project_id: int, document_id: int) -> models.Manuscript:
        manuscript = models.Manuscript(project_id=project_id, document_id=document_id, status="submitted")
        db.add(manuscript)
        db.commit()
        db.refresh(manuscript)
        return manuscript

    def approve(self, db: Session, manuscript_id: int, role: models.Role) -> models.Manuscript:
        manuscript = db.get(models.Manuscript, manuscript_id)
        if not manuscript:
            raise ValueError("Manuscript not found")
        if role == models.Role.SUPERVISOR:
            manuscript.approved_by_supervisor = True
        if role == models.Role.HOD:
            manuscript.approved_by_hod = True
        if manuscript.approved_by_supervisor and manuscript.approved_by_hod:
            manuscript.status = "approved"
        db.commit()
        db.refresh(manuscript)
        return manuscript
