# Handoff

## Active Repo
- Source of truth repo:
  - `C:\Users\astit\Desktop\nyay-justis`

## Remote
- `origin`: `https://github.com/ImAstitv/nyay-justis.git`

## Important Commits Already Created
- `19ed362` `Harden app baseline and add migrations/authz scaffolding`
- `8ec10c9` `Add backend pytest coverage for authz and migrations`
- `9244648` `Add repo handoff docs and real-user/OCR improvements`

## Current Focus
- OpenAI-first document extraction and structured field extraction
- Human-review filing workflow with AI-prefilled fields
- Improved filing review UX with attention states and source-text-assisted correction
- Admin-managed account creation and admin panel
- Citizen-facing backend/frontend module removed from active product flows
- PostgreSQL-ready backend config with normalized hosted DB URLs and pool settings
- PostgreSQL smoke script added at `backend/scripts/postgres_smoke.py`
- Hosted admin seed script added at `backend/scripts/seed_admin.py`
- Minimal court-data import script added at `backend/scripts/ingest_court_data.py`
- Minimal multilingual translation endpoint added at `POST /ocr/translate`
- OpenAI-based future multilingual workflows for Indian languages
- Tesseract retained only as fallback OCR for resilience

## Backend Commands
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
python -m pytest tests -q
python -m compileall api core migrations models services tests scripts bootstrap_local_users.py main.py
python -m alembic upgrade head
python .\scripts\postgres_smoke.py
python .\scripts\seed_admin.py --username admin --password change-me-now --full-name "Registry Admin"
```

## Frontend Commands
```powershell
cd C:\Users\astit\Desktop\nyay-justis\frontend
npm install
npm run build
```

## Local OCR Requirements
- `OPENAI_API_KEY` configured for primary extraction
- Tesseract installed for fallback OCR
- backend process PATH includes `C:\Program Files\Tesseract-OCR` if fallback is needed
- `/ocr/health` should show OpenAI document extraction config and fallback OCR health

## Local Dev Environment Used
```powershell
$env:DATABASE_URL="sqlite:///./nyay.db"
$env:SECRET_KEY="dev-secret"
$env:CORS_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'
$env:COOKIE_SECURE="false"
$env:COOKIE_SAMESITE="lax"
$env:ALLOW_LOCAL_BOOTSTRAP="true"
$env:OPENAI_API_KEY="your-openai-api-key"
$env:DB_POOL_SIZE="5"
$env:DB_MAX_OVERFLOW="10"
$env:DB_POOL_TIMEOUT_SECONDS="30"
$env:DB_POOL_RECYCLE_SECONDS="1800"
```

## Real Product Gaps Still Open
- handwritten OCR quality
- stronger NLP field extraction
- account disable/lock/password-reset lifecycle
- Render and Vercel authentication plus deploy execution from this workstation
- real court data ingestion
- multilingual infrastructure using OpenAI language workflows
- full frontend redesign
- public deployment and operations

## If Another LLM Takes Over
Start here:
1. read `docs/STATUS.md`
2. read `docs/ROADMAP.md`
3. read `docs/ARCHITECTURE.md`
4. inspect `git status`
5. inspect latest commits
6. keep OpenAI as primary extraction and treat Tesseract as fallback unless there is a deliberate architectural decision to remove it
7. use admin credentials for account creation; judge accounts no longer create users

## PostgreSQL Note
- A local `postgresql-x64-18` Windows service is running on this workstation.
- `psql.exe` exists at `C:\Program Files\PostgreSQL\18\bin\psql.exe`, but it is not on PATH.
- Local provisioning is now verified on `localhost:5432` for database `nyay_justis` using an operator-supplied `postgres` password.
- `python -m alembic upgrade head` passes from `backend/` when `DATABASE_URL=postgresql+psycopg2://postgres:[YOUR-LOCAL-PASSWORD]@localhost:5432/nyay_justis`.
- `python .\scripts\postgres_smoke.py` now runs from `backend/` with that same `DATABASE_URL`.
- Keep the real password out of tracked files; use environment overrides or ignored local `.env` values.
- Hosted Supabase migration and smoke verification now also pass with the provided staging `DATABASE_URL`.
- For hosted staging, use `backend/scripts/seed_admin.py` once after migration to create the first admin login.

## Deployment Note
- `backend/render.yaml` and `frontend/vercel.json` are present and aligned with the current staging direction.
- `backend/Dockerfile` now respects `${PORT}` for Render.
- Render CLI and Vercel CLI were not installed/authenticated in this session, so actual hosted deploy execution is still pending operator/project access.
- `docs/STAGING_RUNBOOK.md` now contains the exact dashboard values, click-by-click deploy order, hosted verification flow, and current blockers for the immediate staging push.
- For immediate staging, use the manual Render Web Service flow from `docs/STAGING_RUNBOOK.md`; `backend/render.yaml` is useful as config reference but is not yet sitting at repo-root Blueprint location.
- On 2026-05-11, staging DB verification was advanced further:
  - `python .\scripts\postgres_smoke.py` passed against Supabase staging
  - Alembic staging head was moved to `20260511_0002`
  - direct admin seed for `admin` succeeded after the role-constraint migration
  - direct court-data ingestion verification succeeded
- On 2026-05-11, the hosted Render backend at `https://nyay-justis.onrender.com` was confirmed stale versus repo state:
  - `/auth/login` returned `500` for all tested users
  - CORS preflight from `https://nyay-justis.vercel.app` returned `400`
  - hosted OpenAPI still exposed `/citizen/search`
  - hosted OpenAPI did not include `POST /ocr/translate`
- The immediate next operator action is a fresh backend redeploy from current repo state plus Render env confirmation for:
  - `CORS_ALLOWED_ORIGINS=https://nyay-justis.vercel.app`
  - `SECRET_KEY`
  - `DATABASE_URL`
  - `OPENAI_API_KEY`
- Current OpenAI verification against repo code hit HTTP `429` on the Responses API, so OCR/translation stayed in fallback mode during verification.
