# NYAY-JUSTIS Context

This file is the short starting point for any future engineer or LLM.

## Source Of Truth
- Active repo: `C:\Users\astit\Desktop\nyay-justis`
- GitHub remote: `https://github.com/ImAstitv/nyay-justis.git`

## Read These First
1. `docs/STATUS.md`
2. `docs/HANDOFF.md`
3. `docs/ROADMAP.md`
4. `docs/ARCHITECTURE.md`
5. `docs/STAGING_RUNBOOK.md`

## Current Reality
- This is a working production-baseline prototype, not a fully production-ready platform.
- Backend auth, migrations, tests, OCR health, PDF OCR support, and OpenAI-first extraction wiring are in place.
- Frontend builds and local role-based flows run.
- SQLite works locally.
- Tesseract is now fallback OCR, not the primary strategy.
- OpenAI is the intended primary provider for OCR, field extraction, and future language workflows.
- The filing form now supports stronger AI-assisted human review with attention states and source-text reference.
- Admin role and admin panel are now part of the product direction.
- Account creation has moved from judge-managed to admin-managed.
- Citizen-facing backend and frontend modules have been removed from active product flows.
- PostgreSQL is now the intended standard environment and the backend config normalizes hosted Postgres URLs.
- Local PostgreSQL 18 service is installed/running on this workstation, and local provisioning has been verified against `nyay_justis` after supplying a valid Postgres password.
- Hosted Supabase PostgreSQL migration and smoke verification now pass against project `xjznnzrwescdkszhtprw`.
- A staging-safe admin seed script now exists at `backend/scripts/seed_admin.py`.
- A minimal court-data import script now exists at `backend/scripts/ingest_court_data.py`.
- A minimal multilingual backend translation endpoint now exists at `POST /ocr/translate`.
- A current staging deployment runbook now exists at `docs/STAGING_RUNBOOK.md`.
- A follow-up migration now exists at `backend/migrations/versions/20260511_0002_allow_admin_role.py` to align staging DB role constraints with the admin-first product direction.
- As of 2026-05-11, the deployed Render backend was confirmed stale relative to repo state and needs redeploy before hosted staging smoke can pass.
- Handwritten extraction quality still needs serious improvement.
- UI/UX still needs a full redesign.
- Full multilingual UX and real court-data ingestion workflows are still future work.

## Quick Commands

### Backend
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
 $env:DATABASE_URL="postgresql+psycopg2://postgres:[YOUR-LOCAL-PASSWORD]@localhost:5432/nyay_justis"
 $env:SECRET_KEY="dev-secret"
 $env:CORS_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'
 $env:COOKIE_SECURE="false"
 $env:COOKIE_SAMESITE="lax"
 $env:ALLOW_LOCAL_BOOTSTRAP="true"
 $env:OPENAI_API_KEY="your-openai-api-key"
 $env:ENABLE_MULTILINGUAL_PIPELINE="true"
 $env:MULTILINGUAL_TARGET_LANGUAGE="English"
 $env:SUPPORTED_DOCUMENT_LANGUAGES="English,Hindi"
 $env:DB_POOL_SIZE="5"
 $env:DB_MAX_OVERFLOW="10"
 $env:DB_POOL_TIMEOUT_SECONDS="30"
 $env:DB_POOL_RECYCLE_SECONDS="1800"
 $env:Path += ";C:\Program Files\Tesseract-OCR"
 python -m alembic upgrade head
 python .\scripts\postgres_smoke.py
 python -m uvicorn main:app --reload --host localhost --port 8000
 ```

### Frontend
```powershell
cd C:\Users\astit\Desktop\nyay-justis\frontend
$env:VITE_API_URL="http://localhost:8000"
npm run dev
```

### Tests
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
python -m pytest tests -q
python -m compileall api core migrations models services tests scripts bootstrap_local_users.py main.py
```

## Most Important Next Work
- validate OpenAI extraction on real documents
- improve handwritten extraction quality
- redesign the filing and review UX
- execute the hosted Render + Vercel staging deployment using the now-verified Supabase database
- expand admin account lifecycle beyond create/list
- expand multilingual support from backend translation to full frontend/workflow coverage
- ingest real cause-list and case-history data through the new import scaffolding
