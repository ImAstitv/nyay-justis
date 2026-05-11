# Staging Runbook

Last updated: 2026-05-11

This runbook is the fastest staging path for the current repo without redoing the already-verified Supabase migration and smoke work.

## Deployment Targets
- Backend host: Render
- Frontend host: Vercel
- Staging database: Supabase Postgres project `xjznnzrwescdkszhtprw`
- Git remote: `https://github.com/ImAstitv/nyay-justis.git`
- Deploy branch: `main`

## Exact Render Dashboard Values

Preferred staging path right now: manual Render Web Service creation from GitHub, using the existing Docker setup in `backend/`.

- Service type: `Web Service`
- Source: `Public Git repository`
- Repository: `https://github.com/ImAstitv/nyay-justis.git`
- Branch: `main`
- Root Directory: leave blank
- Runtime: `Docker`
- Name: `nyay-justis-api`
- Region: `Singapore` recommended for India-facing staging
- Plan: `Free` for staging
- Dockerfile Path: `backend/Dockerfile`
- Docker Build Context Directory: `backend`
- Health Check Path: `/`
- Auto-Deploy: `On`

Environment variables to enter in Render:

- `DATABASE_URL`: Supabase staging connection string
- `DB_POOL_SIZE`: `5`
- `DB_MAX_OVERFLOW`: `10`
- `DB_POOL_TIMEOUT_SECONDS`: `30`
- `DB_POOL_RECYCLE_SECONDS`: `1800`
- `SECRET_KEY`: generate a long random secret
- `OPENAI_API_KEY`: staging OpenAI key
- `OPENAI_EXTRACTION_MODEL`: `gpt-4.1`
- `OPENAI_TIMEOUT_SECONDS`: `90`
- `ENABLE_MULTILINGUAL_PIPELINE`: `true`
- `MULTILINGUAL_TARGET_LANGUAGE`: `English`
- `SUPPORTED_DOCUMENT_LANGUAGES`: `English,Hindi`
- `CORS_ALLOWED_ORIGINS`: exact Vercel frontend URL after Vercel creation
- `COOKIE_SECURE`: `true`
- `COOKIE_SAMESITE`: `none`
- `COOKIE_DOMAIN`: leave empty at first unless a custom cookie domain is deliberately chosen
- `ALLOW_LOCAL_BOOTSTRAP`: do not set in staging

Expected backend URLs after deploy:

- Health/root: `https://<render-backend-host>/`
- OCR health: `https://<render-backend-host>/ocr/health`
- Translate endpoint: `https://<render-backend-host>/ocr/translate`

## Exact Vercel Dashboard Values

Preferred staging path right now: manual Vercel Project import from GitHub, targeting the `frontend/` app only.

- Project type: `Vite`
- Repository: `https://github.com/ImAstitv/nyay-justis.git`
- Branch: `main`
- Root Directory: `frontend`
- Framework Preset: `Vite`
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`
- Development Command: `npm run dev`
- Node version: default current Vercel Node is fine; pin only if the first build disagrees

Environment variables to enter in Vercel:

- `VITE_API_URL`: `https://<render-backend-host>`

Expected frontend URLs after deploy:

- App root: `https://<vercel-frontend-host>/`
- Admin login: `https://<vercel-frontend-host>/login/admin`
- Judge login: `https://<vercel-frontend-host>/login/judge`
- Lawyer login: `https://<vercel-frontend-host>/login/lawyer`

## Click-By-Click Backend Deploy Checklist

### A. Create Render service
1. Open Render Dashboard.
2. Click `New +`.
3. Click `Web Service`.
4. Connect GitHub if prompted.
5. Select repo `ImAstitv/nyay-justis`.
6. Set branch to `main`.
7. Choose runtime `Docker`.
8. Enter service name `nyay-justis-api`.
9. Leave root directory blank.
10. Set Dockerfile path to `backend/Dockerfile`.
11. Set Docker build context directory to `backend`.
12. Choose region `Singapore`.
13. Choose plan `Free`.
14. Set health check path to `/`.
15. Turn auto-deploy on.
16. Enter all backend environment variables listed above except `CORS_ALLOWED_ORIGINS` if the frontend URL is not known yet.
17. Click `Create Web Service`.

### B. Finish backend configuration after first Vercel deploy
1. Copy the Vercel preview or production frontend URL.
2. Open the Render service.
3. Go to `Environment`.
4. Set `CORS_ALLOWED_ORIGINS` to that exact frontend origin only.
5. Keep `COOKIE_SECURE=true`.
6. Keep `COOKIE_SAMESITE=none`.
7. Leave `COOKIE_DOMAIN` empty unless you later move both apps under one deliberate parent domain.
8. Save changes and allow Render to redeploy.

### C. Seed the first admin
Fastest safe option:
1. Open the Render backend service.
2. Open `Shell`.
3. Run:

```bash
python scripts/seed_admin.py --username admin --password <strong-password> --full-name "Registry Admin"
```

Alternative option:
1. Run the same script locally from `backend/`.
2. Point local `DATABASE_URL` at the same Supabase staging database.

## Click-By-Click Frontend Deploy Checklist

1. Open Vercel Dashboard.
2. Click `Add New...`.
3. Click `Project`.
4. Import repo `ImAstitv/nyay-justis`.
5. Set framework preset to `Vite`.
6. Set root directory to `frontend`.
7. Confirm build command `npm run build`.
8. Confirm output directory `dist`.
9. Confirm install command `npm install`.
10. Add environment variable `VITE_API_URL=https://<render-backend-host>`.
11. Click `Deploy`.
12. After the site is live, copy the frontend URL.
13. Go back to Render and set `CORS_ALLOWED_ORIGINS` to that exact URL.
14. Trigger or wait for the backend redeploy.
15. Reload the frontend and test login again.

## Hosted Flow To Verify First

Run these in order. Do not expand scope before this list passes.

1. Admin seed
   - Confirm `python scripts/seed_admin.py ...` succeeds once against staging.
   - Success signal: admin record exists and login works.
2. Admin login
   - Visit `/login/admin`.
   - Log in with the seeded admin credentials.
   - Success signal: lands on `/admin`, account roster loads, no 401 loop.
3. Account creation
   - From `/admin`, create one `lawyer` account and one `judge` account.
   - Success signal: both accounts appear in the roster and can log in.
4. Lawyer filing
   - Visit `/login/lawyer`.
   - Log in with the created lawyer account.
   - Upload a JPG, PNG, or PDF in `/lawyer`.
   - Run OCR.
   - Run field extraction.
   - Submit a case with at least `Case ID`.
   - Success signal: case creation completes and the confirmation view appears.
5. Judge flow
   - Visit `/login/judge`.
   - Log in with the created judge account.
   - Confirm the new case appears.
   - Test `Adjourn` once.
   - Test `Dispose` once.
   - Success signal: analytics load, case state changes persist, no role/auth errors.
6. OCR health
   - While logged in, call `GET /ocr/health`.
   - Success signal: response shows `primary_provider: openai` and fallback OCR health details.
7. Translation endpoint
   - While logged in, call `POST /ocr/translate` with JSON body:

```json
{
  "text": "नमस्ते",
  "target_language": "English"
}
```

   - Success signal: `200 OK` and a structured JSON response with `translated_text`.

## Remaining Deploy Blockers

These are the blockers still worth caring about before calling staging "live":

1. `backend/render.yaml` is not at repo root.
   - Impact: Render Blueprint import is not ready as-is.
   - Fastest path: use the manual Render Web Service flow above.
2. `CORS_ALLOWED_ORIGINS` depends on the final frontend URL.
   - Impact: cookie-based login will fail until Render knows the exact Vercel origin.
3. Render and Vercel project auth are operator-side.
   - Impact: repo is ready enough for staging, but actual deploy clicks still require dashboard access.
4. Staging admin bootstrap is still manual.
   - Impact: login verification cannot start until the first admin is seeded.
5. Real OCR quality on court documents is not yet validated.
   - Impact: staging can go live for workflow verification, but extraction quality should still be treated as provisional MVP quality.

## Verification Snapshot

Checked on 2026-05-11 against:
- Backend URL: `https://nyay-justis.onrender.com`
- Frontend URL: `https://nyay-justis.vercel.app`

What is verified now:
- Supabase staging DB is reachable and migrations are present.
- Alembic `head` on staging is now `20260511_0002`.
- Admin seed now exists in staging DB as `admin`.
- Direct staging DB court-data ingestion verification passed.
- Current repo code, when pointed at staging DB, can:
  - create admin-managed lawyer and judge accounts
  - create a lawyer-filed case
  - list and analyze cases for a judge
  - adjourn and dispose a case

What is still broken on the currently hosted Render backend:
- `POST /auth/login` returns `500` for all tested users.
- CORS preflight for frontend origin `https://nyay-justis.vercel.app` returns `400`.
- Hosted OpenAPI is stale relative to repo direction:
  - still exposes `/citizen/search`
  - does not expose `POST /ocr/translate`
- Hosted backend therefore needs a fresh redeploy from current repo state before browser-based staging smoke can pass.

OpenAI/OCR note from 2026-05-11 verification:
- OpenAI extraction config is present in current code, but direct Responses API calls returned HTTP `429`.
- As a result:
  - translation falls back to original text
  - field extraction falls back to regex
  - document OCR falls through to Tesseract when OpenAI fails
- On the local verification machine, Tesseract was not installed in PATH, so local fallback OCR returned `422`.
- On hosted Render, ensure Tesseract remains installed in the Docker image and resolve the OpenAI `429` condition before treating OCR/translation as staging-ready.

## Fastest UI Polish Path After Staging

Recommendation: do a narrow visual pass on the existing pages instead of a redesign or new feature wave.

### Option A: fastest and safest
- Keep routes, components, and API behavior unchanged.
- Introduce a shared visual system only:
  - one typography stack
  - one color system
  - one spacing scale
  - one button/input/card pattern
- Restyle only:
  - `frontend/src/pages/Landing.jsx`
  - `frontend/src/pages/Login.jsx`
  - `frontend/src/pages/AdminPanel.jsx`
  - `frontend/src/pages/LawyerFiling.jsx`
  - `frontend/src/pages/JudgeDashboard.jsx`
- Why this wins: highest cosmetic gain, lowest regression risk.

### Option B: moderate polish
- Do Option A.
- Also split repeated inline styles into shared UI primitives and page sections.
- Why not first: better code quality, but slower than needed for the next 2 days.

### Option C: full redesign
- Rework IA, page layout, and interaction model.
- Why not now: too much risk for the current staging-first goal.

### Recommended polish sequence
1. Create a shared `theme` file and a small set of reusable layout primitives.
2. Make the landing page feel intentional and premium first.
3. Refresh login and admin pages next for trust and clarity.
4. Polish lawyer filing third because it is the strongest demo path.
5. Polish judge dashboard last, focusing on hierarchy and status chips rather than new analytics.

### UI polish guardrails
- Do not add new roles or reopen the citizen flow.
- Do not change backend contracts.
- Do not redesign the filing workflow steps yet.
- Do not add broad multilingual UI until the backend language path is verified on real usage.
