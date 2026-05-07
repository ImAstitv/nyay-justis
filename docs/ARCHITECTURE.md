# Architecture

## Repositories And Working Copies
- Active engineering copy during this session: `C:\Users\astit\.codex\worktrees\9655\nyay-justis`
- User-facing repo to update before deployment: `C:\Users\astit\Desktop\nyay-justis`
- GitHub remote: `https://github.com/ImAstitv/nyay-justis.git`

## System Overview
- `frontend/`: React + Vite application for judge, lawyer, and citizen flows.
- `backend/`: FastAPI application with auth, case management, OCR/NLP, and citizen search.
- `backend/migrations/`: Alembic migration scaffolding and schema revisions.
- `docs/`: project memory and handoff documents.

## Backend Modules
- `backend/main.py`
  - FastAPI app entrypoint
  - CORS wiring from environment
- `backend/api/auth.py`
  - login/logout/me
  - create user endpoint
  - change password endpoint
  - cookie-based session auth
- `backend/api/cases.py`
  - create case
  - list cases
  - analytics
  - adjourn and dispose actions
- `backend/api/citizen.py`
  - exact-match, ownership-gated citizen search
- `backend/api/ocr.py`
  - OCR upload endpoint
  - OCR health endpoint
  - NLP extraction endpoint
- `backend/core/authz.py`
  - role checks
  - case owner checks
  - disposed-case guard
- `backend/core/config.py`
  - environment-backed settings
- `backend/models/models.py`
  - `User`, `Case`, `Hearing`, `AuditLog`
- `backend/services/ocr_service.py`
  - image OCR via Tesseract
  - PDF rendering via `pypdfium2`
  - OCR health diagnostics
- `backend/services/nlp_service.py`
  - current regex-style field extraction
- `backend/services/priority_engine.py`
  - current priority scoring logic

## Frontend Modules
- `frontend/src/App.jsx`
  - route registration and role gates
- `frontend/src/services/api.js`
  - API client with cookie credentials
- `frontend/src/pages/Login.jsx`
  - username/password login
- `frontend/src/pages/LawyerFiling.jsx`
  - OCR/NLP/manual-review flow
- `frontend/src/pages/JudgeDashboard.jsx`
  - analytics and case actions
- `frontend/src/pages/CitizenPortal.jsx`
  - exact-match citizen search

## Current Runtime Model
- Development database: SQLite via `DATABASE_URL=sqlite:///./nyay.db`
- Production target database: PostgreSQL
- Auth transport: HTTP-only cookie
- OCR engine: local Tesseract
- PDF OCR renderer: `pypdfium2`

## Key Constraints
- Current NLP extraction is still prototype-grade.
- Current handwritten OCR quality is not state of the art.
- Current UI is functional but not production-quality.
- Current local bootstrap users are for dev only and are gated by `ALLOW_LOCAL_BOOTSTRAP=true`.
