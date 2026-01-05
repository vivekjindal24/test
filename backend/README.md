# Backend (FastAPI)

## Run locally
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app/db/init_db.py
alembic upgrade head
python app/db/seed.py  # seeds default admin/hod/supervisor/student (password: ChangeMe!123)
uvicorn app.main:app --reload
```

## API surface (v1)
- `POST /api/v1/auth/token` — OAuth2 password, returns JWT
- `POST /api/v1/projects` — create project (Student)
- `GET /api/v1/projects` — list projects (scoped by role)
- `POST /api/v1/projects/{project_id}/milestones/{milestone_id}/complete` — mark done (Supervisor/HOD/Admin)
- `POST /api/v1/projects/{project_id}/meetings` — schedule meeting (Supervisor/HOD/Admin)
- `POST /api/v1/projects/{project_id}/meetings/{meeting_id}/minutes` — add MoM (Supervisor/HOD/Admin)
- `POST /api/v1/documents/{project_id}` — upload doc (all roles)
- `GET /api/v1/documents/{project_id}` — list docs
- `POST /api/v1/documents/{document_id}/annotations` — add annotation
- `GET /api/v1/notifications` — current user notifications

## Database schema (core tables)
- `users(id, email, full_name, role, hashed_password, is_active, created_at, updated_at)`
- `projects(id, title, description, owner_id, supervisor_id, hod_id, status, created_at, updated_at)`
- `milestones(id, project_id, title, due_date, status, notes, created_at)`
- `meetings(id, project_id, title, agenda, scheduled_for, created_at)`
- `meeting_minutes(id, meeting_id, summary, action_items, created_at)`
- `documents(id, project_id, title, path, mime_type, latest_version_id, created_at)`
- `document_versions(id, document_id, version, path, checksum, created_by, created_at)`
- `annotations(id, document_id, author_id, body, is_resolved, created_at)`
- `manuscripts(id, project_id, status, document_id, submitted_at, approved_by_supervisor, approved_by_hod)`
- `publications(id, project_id, title, journal, doi, published_at)`
- `notifications(id, user_id, channel, subject, body, is_read, created_at)`
- `audit_logs(id, user_id, action, resource, metadata, created_at)`

## Services
- `StorageService` — S3-compatible uploads with checksums
- `NotificationService` — email/SMS/calendar hooks
- `ManuscriptService` — submit and approve workflow
- `Audit` — persistent audit trail

## Security & compliance
- JWT auth with RBAC guards per route
- Structured logging; audit table
- CORS configured by env; HTTPS enforced at ALB/CloudFront
- Data at rest via RDS/S3 encryption; in transit via TLS
- GDPR: data subject export/delete hooks can extend services layer
