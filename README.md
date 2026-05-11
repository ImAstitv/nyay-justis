# NYAY-JUSTIS

Nyay-Justis is a court workflow prototype for:
- case filing support
- OCR/NLP-assisted document extraction
- priority-based scheduling support
- admin, judge, and lawyer role-based workflows

## Current State
- Backend and frontend run locally
- Backend tests pass
- PDF OCR support exists
- Local SQLite development works
- Local and hosted PostgreSQL migration/smoke verification now pass
- This repo is still in active product-hardening and redesign

## Key Docs
- [CONTEXT.md](CONTEXT.md)
- [docs/STATUS.md](docs/STATUS.md)
- [docs/HANDOFF.md](docs/HANDOFF.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)

## Local Run

### Backend
```powershell
cd backend
python -m pip install -r requirements.txt
python -m alembic upgrade head
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Notes
- Tesseract must be installed locally for OCR.
- Local bootstrap users are development-only.
- Hosted staging needs a one-time admin seed via `backend/scripts/seed_admin.py` after migrations.
- Minimal multilingual backend translation is available at `POST /ocr/translate`.
- Minimal CSV/JSON court-data import is available via `backend/scripts/ingest_court_data.py`.
- For full current engineering context, start with `CONTEXT.md`.
