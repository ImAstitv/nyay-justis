# Deployment

## Current Local Development Commands

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
$env:DB_POOL_SIZE="5"
$env:DB_MAX_OVERFLOW="10"
$env:DB_POOL_TIMEOUT_SECONDS="30"
$env:DB_POOL_RECYCLE_SECONDS="1800"
$env:Path += ";C:\Program Files\Tesseract-OCR"
python -m alembic upgrade head
python .\scripts\postgres_smoke.py
python -m uvicorn main:app --reload --host localhost --port 8000
```

### SQLite Fallback For Local-Only Work
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
$env:DATABASE_URL="sqlite:///./nyay.db"
python -m alembic upgrade head
python -m uvicorn main:app --reload --host localhost --port 8000
```

### Frontend
```powershell
cd C:\Users\astit\Desktop\nyay-justis\frontend
$env:VITE_API_URL="http://localhost:8000"
npm run dev
```

## Local Bootstrap Users
Use only for local development:
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
$env:ALLOW_LOCAL_BOOTSTRAP="true"
python .\bootstrap_local_users.py
```
Current local bootstrap roles are `admin`, `judge`, and `lawyer`.

## Local Validation
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
python -m pytest tests -q
python -m compileall api core migrations models services tests scripts bootstrap_local_users.py main.py

cd C:\Users\astit\Desktop\nyay-justis\frontend
npm run build
```

## PostgreSQL Smoke Test
After valid Postgres credentials are configured:
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
$env:DATABASE_URL="postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/nyay_justis"
python -m alembic upgrade head
python .\scripts\postgres_smoke.py
```

Local note from May 9, 2026: local PostgreSQL provisioning is now verified on `nyay_justis` after supplying a valid local `postgres` password. `python -m alembic upgrade head` and `python .\scripts\postgres_smoke.py` both pass from `backend/`.

## Production Direction
- Backend: FastAPI on Render using `backend/render.yaml`
- Frontend: Vite static site on Vercel using `frontend/vercel.json`
- Secrets: environment variables, not checked-in `.env`
- Primary extraction: OpenAI API key configured on the backend host
- Use `backend/.env.example` as the environment starting template
- Prefer `postgresql+psycopg2://...` URLs; Render-style `postgres://...` is normalized in config
- Cookies:
  - `COOKIE_SECURE=true`
  - `COOKIE_SAMESITE=none` for cross-site hosted frontend/backend if needed
- Fallback OCR host should still have:
  - Tesseract installed
  - PDF rendering dependency available

## Hosted Staging Prerequisites
- GitHub repository pushed and available to Render and Vercel
- Hosted PostgreSQL connection string for staging
- Backend secrets configured on the host:
  - `DATABASE_URL`
  - `SECRET_KEY`
  - `OPENAI_API_KEY`
  - `CORS_ALLOWED_ORIGINS`
  - `COOKIE_SECURE=true`
  - `COOKIE_SAMESITE=none`
  - optional `COOKIE_DOMAIN` once the frontend domain is fixed
- Frontend environment configured on Vercel:
  - `VITE_API_URL=https://<your-backend-host>`
- Real domain decisions made for:
  - backend origin
  - frontend origin
  - cookie domain and cross-site cookie policy
- Render and Vercel project access, or authenticated CLIs, to execute the actual deploys from this workstation

## Staging Runbook
- Use `docs/STAGING_RUNBOOK.md` as the current source of truth for:
  - exact Render dashboard values
  - exact Vercel dashboard values
  - click-by-click deploy steps
  - hosted verification order
  - current deploy blockers
- Important nuance: `backend/render.yaml` reflects the intended Render config, but because it is not at repo root it is not yet a ready-to-import Render Blueprint. For immediate staging, prefer the manual Render Web Service flow documented in `docs/STAGING_RUNBOOK.md`.

## Staging Deployment Order
1. Provision hosted PostgreSQL and set the backend `DATABASE_URL`.
2. Deploy the backend on Render using `backend/Dockerfile` and the manual dashboard values in `docs/STAGING_RUNBOOK.md`.
3. Run Alembic against the hosted database.
4. Run `python .\scripts\seed_admin.py --username <admin> --password <password> --full-name "<name>"` once against the hosted database.
5. Verify backend health at `/` and OCR health at `/ocr/health`.
6. Deploy the frontend with `VITE_API_URL` pointing at the staged backend.
7. Verify login, admin account creation, case filing, judge actions, and `/ocr/translate` end to end.
8. Verify OpenAI extraction on real staging documents before any production cutover.

## Current Known Blockers For Real Staging
- OpenAI extraction has not been validated on a real court-document corpus.
- Admin lifecycle is only partially complete today: create/list exists, but reset/disable/lock flows do not.
- UI quality is still prototype-level outside the improved filing review flow.
- Render CLI and Vercel CLI were not installed/authenticated in this session, so the deploy execution itself is still pending.
- `backend/render.yaml` is not at repo root, so Blueprint-style Render import is not ready without an additional file move/copy or manual dashboard setup.
- As of 2026-05-11, the currently hosted Render backend is stale versus repo state:
  - `POST /auth/login` returns `500`
  - frontend-origin CORS preflight from `https://nyay-justis.vercel.app` returns `400`
  - hosted OpenAPI still exposes `/citizen/search`
  - hosted OpenAPI does not expose `POST /ocr/translate`
- As of 2026-05-11, direct OpenAI Responses API calls from current code returned `429`, so OCR/translation currently fall back when exercised from the verified code path.

## Before Real Deployment
- complete hosted/staging PostgreSQL provisioning and run the same migration/smoke flow there
- expand admin account lifecycle beyond create/list
- verify OpenAI extraction with real sample documents
- finish frontend redesign
- finalize domain/CORS/cookie settings
