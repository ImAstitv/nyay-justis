# Deployment

## Current Local Development Commands

### Backend
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
$env:DATABASE_URL="sqlite:///./nyay.db"
$env:SECRET_KEY="dev-secret"
$env:CORS_ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'
$env:COOKIE_SECURE="false"
$env:COOKIE_SAMESITE="lax"
$env:ALLOW_LOCAL_BOOTSTRAP="true"
$env:OPENAI_API_KEY="your-openai-api-key"
$env:Path += ";C:\Program Files\Tesseract-OCR"
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

## Local Validation
```powershell
cd C:\Users\astit\Desktop\nyay-justis\backend
python -m pytest backend/tests -q
python -m compileall backend

cd C:\Users\astit\Desktop\nyay-justis\frontend
npm run build
```

## Production Direction
- Backend: FastAPI on a hosted environment with PostgreSQL
- Frontend: Vercel or equivalent CDN-hosted static deployment
- Secrets: environment variables, not checked-in `.env`
- Primary extraction: OpenAI API key configured on the backend host
- Cookies:
  - `COOKIE_SECURE=true`
  - `COOKIE_SAMESITE=none` for cross-site hosted frontend/backend if needed
- Fallback OCR host should still have:
  - Tesseract installed
  - PDF rendering dependency available

## Before Real Deployment
- switch to PostgreSQL
- create real account lifecycle
- verify OpenAI extraction with real sample documents
- finish frontend redesign
- finalize domain/CORS/cookie settings
