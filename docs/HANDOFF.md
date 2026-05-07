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
- OpenAI-based future multilingual workflows for Indian languages
- Tesseract retained only as fallback OCR for resilience

## Backend Commands
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
python -m pytest backend/tests -q
python -m compileall backend
python -m alembic upgrade head
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
```

## Real Product Gaps Still Open
- handwritten OCR quality
- stronger NLP field extraction
- create-account frontend flow
- production database posture with PostgreSQL
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
