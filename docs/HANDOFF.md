# Handoff

## Active Repo
- Worktree copy used during implementation:
  - `C:\Users\astit\.codex\worktrees\9655\nyay-justis`
- Desktop repo to sync before deployment:
  - `C:\Users\astit\Desktop\nyay-justis`

## Remote
- `origin`: `https://github.com/ImAstitv/nyay-justis.git`

## Important Commits Already Created In Worktree
- `19ed362` `Harden app baseline and add migrations/authz scaffolding`
- `8ec10c9` `Add backend pytest coverage for authz and migrations`

## Current Uncommitted Worktree Changes At Time Of Writing
- real DB-backed user creation and password change endpoints
- OCR diagnostics
- PDF OCR support
- local bootstrap guard
- NumPy compatibility pin
- migration smoke test path fix
- `frontend/package-lock.json`

## Backend Commands
```powershell
cd C:\Users\astit\.codex\worktrees\9655\nyay-justis\backend
python -m pytest backend/tests -q
python -m compileall backend
python -m alembic upgrade head
```

## Frontend Commands
```powershell
cd C:\Users\astit\.codex\worktrees\9655\nyay-justis\frontend
npm install
npm run build
```

## Local OCR Requirements
- Tesseract installed
- backend process PATH includes `C:\Program Files\Tesseract-OCR`
- `/ocr/health` should return `ok: true`

## Local Dev Environment Used
```powershell
$env:DATABASE_URL="sqlite:///./nyay.db"
$env:SECRET_KEY="dev-secret"
$env:CORS_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'
$env:COOKIE_SECURE="false"
$env:COOKIE_SAMESITE="lax"
$env:ALLOW_LOCAL_BOOTSTRAP="true"
```

## Real Product Gaps Still Open
- handwritten OCR quality
- stronger NLP field extraction
- create-account frontend flow
- production database posture with PostgreSQL
- real court data ingestion
- multilingual infrastructure
- full frontend redesign
- public deployment and operations

## If Another LLM Takes Over
Start here:
1. read `docs/STATUS.md`
2. read `docs/ROADMAP.md`
3. read `docs/ARCHITECTURE.md`
4. inspect `git status`
5. inspect latest commits
6. continue from worktree until Desktop repo sync is explicitly done
