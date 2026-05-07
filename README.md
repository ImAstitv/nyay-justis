# NYAY-JUSTIS

Nyay-Justis is a court workflow prototype for:
- case filing support
- OCR/NLP-assisted document extraction
- priority-based scheduling support
- judge, lawyer, and citizen role-based workflows

## Current State
- Backend and frontend run locally
- Backend tests pass
- PDF OCR support exists
- Local SQLite development works
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
- For full current engineering context, start with `CONTEXT.md`.
