# NYAY-JUSTIS Context

This file is the short entry point for any future engineer or LLM.

## Source Of Truth
- Active working copy during this session:
  - `C:\Users\astit\.codex\worktrees\9655\nyay-justis`
- Desktop repo to sync before deployment:
  - `C:\Users\astit\Desktop\nyay-justis`
- GitHub remote:
  - `https://github.com/ImAstitv/nyay-justis.git`

## Read These First
1. `docs/STATUS.md`
2. `docs/HANDOFF.md`
3. `docs/ROADMAP.md`
4. `docs/ARCHITECTURE.md`

## Current Reality
- This is a working production-baseline prototype, not a fully production-ready platform.
- Backend auth, migrations, tests, OCR health, and PDF OCR support are in place.
- Frontend builds and local role-based flows run.
- SQLite works locally.
- Tesseract-backed OCR is locally operational when the backend process has Tesseract in PATH.
- Handwritten OCR quality and NLP extraction quality are still below target.
- UI/UX still needs a full redesign.
- Multilingual support and real court-data ingestion are still future work.

## Quick Commands

### Backend
```powershell
cd C:\Users\astit\.codex\worktrees\9655\nyay-justis\backend
$env:DATABASE_URL="sqlite:///./nyay.db"
$env:SECRET_KEY="dev-secret"
$env:CORS_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'
$env:COOKIE_SECURE="false"
$env:COOKIE_SAMESITE="lax"
$env:ALLOW_LOCAL_BOOTSTRAP="true"
$env:Path += ";C:\Program Files\Tesseract-OCR"
python -m uvicorn main:app --reload --host localhost --port 8000
```

### Frontend
```powershell
cd C:\Users\astit\.codex\worktrees\9655\nyay-justis\frontend
$env:VITE_API_URL="http://localhost:8000"
npm run dev
```

### Tests
```powershell
cd C:\Users\astit\.codex\worktrees\9655\nyay-justis
python -m pytest backend/tests -q
```

## Most Important Next Work
- improve handwriting/document extraction quality
- replace weak regex NLP extraction
- redesign UI to official Indian court-grade experience
- add proper signup/create-account UI and account lifecycle
- move to PostgreSQL for real staging/production
- add multilingual architecture and Sarvam integration
- ingest real cause-list and case-history data
