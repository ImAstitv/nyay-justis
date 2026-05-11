# Architecture

## Repositories And Working Copies
- Active repo: `C:\Users\astit\Desktop\nyay-justis`
- GitHub remote: `https://github.com/ImAstitv/nyay-justis.git`

## System Overview
- `frontend/`: React + Vite application for admin, judge, and lawyer flows.
- `backend/`: FastAPI application with auth, admin account management, case management, and OCR/NLP.
- `backend/migrations/`: Alembic migration scaffolding and schema revisions.
- `docs/`: project memory and handoff documents.

## Backend Modules
- `backend/main.py`
  - FastAPI app entrypoint
  - CORS wiring from environment
- `backend/api/auth.py`
  - login/logout/me
  - admin-only create/list user endpoints
  - change password endpoint
  - cookie-based session auth
- `backend/api/cases.py`
  - create case
  - list cases
  - analytics
  - adjourn and dispose actions
- `backend/api/ocr.py`
  - OpenAI-first document extraction endpoint
  - OCR health endpoint
  - structured field extraction endpoint
  - multilingual translation endpoint
- `backend/core/authz.py`
  - role checks
  - case owner checks
  - disposed-case guard
- `backend/core/config.py`
  - environment-backed settings
- `backend/services/openai_extraction_service.py`
  - OpenAI Responses API integration
  - document text extraction
  - structured case field extraction
  - legal text translation helper
- `backend/models/models.py`
  - `User`, `Case`, `Hearing`, `AuditLog`
- `backend/services/ocr_service.py`
  - local fallback OCR via Tesseract
  - PDF rendering via `pypdfium2`
  - OCR health diagnostics
- `backend/services/nlp_service.py`
  - current regex fallback extraction
- `backend/services/priority_engine.py`
  - current priority scoring logic
- `backend/scripts/seed_admin.py`
  - one-time hosted admin bootstrap
- `backend/scripts/ingest_court_data.py`
  - manual CSV/JSON case import for staged court data

## Frontend Modules
- `frontend/src/App.jsx`
  - route registration and role gates
- `frontend/src/services/api.js`
  - API client with cookie credentials
- `frontend/src/pages/Login.jsx`
  - username/password login
- `frontend/src/pages/AdminPanel.jsx`
  - admin-only account creation and account roster
- `frontend/src/pages/LawyerFiling.jsx`
  - upload, extraction, prefill, and manual-review flow
- `frontend/src/pages/JudgeDashboard.jsx`
  - analytics and case actions

## Current Runtime Model
- Development database: SQLite via `DATABASE_URL=sqlite:///./nyay.db`
- Production target database: PostgreSQL
- Auth transport: HTTP-only cookie
- Primary document extraction: OpenAI Responses API
- Minimal multilingual backend flow: OpenAI-powered translation endpoint
- Fallback OCR engine: local Tesseract
- PDF renderer for fallback OCR: `pypdfium2`

## Key Constraints
- OpenAI is now the primary extraction path, but handwritten extraction quality still needs validation.
- Regex fallback extraction is still prototype-grade.
- Current UI is functional but not production-quality.
- Current local bootstrap users are for dev only and are gated by `ALLOW_LOCAL_BOOTSTRAP=true`.
- User roles are currently `admin`, `judge`, and `lawyer`; account creation is admin-only.
- Hosted staging currently depends on a one-time admin seed after migrations.
