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

## Current Reality
- This is a working production-baseline prototype, not a fully production-ready platform.
- Backend auth, migrations, tests, OCR health, PDF OCR support, and OpenAI-first extraction wiring are in place.
- Frontend builds and local role-based flows run.
- SQLite works locally.
- Tesseract is now fallback OCR, not the primary strategy.
- OpenAI is the intended primary provider for OCR, field extraction, and future language workflows.
- The filing form now supports stronger AI-assisted human review with attention states and source-text reference.
- Judge-managed account creation UI is now part of the frontend and linked from sign-in and the judge dashboard.
- PostgreSQL is now the intended standard environment and the backend config normalizes hosted Postgres URLs.
- Handwritten extraction quality still needs serious improvement.
- UI/UX still needs a full redesign.
- Multilingual support and real court-data ingestion are still future work.

## Quick Commands

### Backend
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
 $env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/nyay_justis"
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
cd C:\Users\astit\Desktop\nyay-justis
python -m pytest backend/tests -q
```

## Most Important Next Work
- validate OpenAI extraction on real documents
- improve handwritten extraction quality
- redesign the filing and review UX
- add proper signup/create-account UI and account lifecycle
- move to PostgreSQL for real staging/production
- add multilingual architecture using OpenAI language workflows
- ingest real cause-list and case-history data
