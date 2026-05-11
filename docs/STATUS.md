# Status

## Current State
- Backend production-hardening baseline is implemented.
- Frontend builds successfully.
- Backend tests are passing.
- SQLite local development flow is working.
- OpenAI-first document extraction wiring is in place.
- Tesseract fallback OCR health is working after local installation.
- PDF OCR support has been added in code.
- Filing review UX now shows AI metadata, attention fields, manual edit tracking, and source text beside the form.
- Admin role and admin panel now exist in the frontend.
- Account creation is now admin-only in backend and frontend.
- Citizen-facing backend/frontend module has been removed from active flows.
- PostgreSQL-ready backend config, env template, and URL normalization are now in place.
- PostgreSQL smoke script exists at `backend/scripts/postgres_smoke.py`.
- Local PostgreSQL 18 provisioning has been verified end-to-end with Alembic on `nyay_justis`.
- Hosted Supabase PostgreSQL migration and smoke verification now pass.
- Minimal multilingual backend translation support now exists via `POST /ocr/translate`.
- Minimal hosted admin bootstrap and court-data import scripts now exist.
- A current staging deployment runbook now exists at `docs/STAGING_RUNBOOK.md`.
- A follow-up migration now exists at `backend/migrations/versions/20260511_0002_allow_admin_role.py` to admit `admin` in the staging `users_role_check` constraint while tolerating the legacy `citizen` row.

## Verified
- backend tests from `backend/`: `python -m pytest tests -q` (`14 passed`)
- backend compile from `backend/`: `python -m compileall api core migrations models services tests scripts bootstrap_local_users.py main.py`
- frontend build from `frontend/`: `npm run build`
- route and role surfaces now target `admin`, `judge`, and `lawyer`
- `/ocr/health` can report OpenAI extraction configuration plus Tesseract fallback health
- local PostgreSQL 18 service is running, authenticates with the operator-supplied password, and targets `nyay_justis`
- Supabase staging `DATABASE_URL` accepts `python -m alembic upgrade head`
- Supabase staging `DATABASE_URL` passes `python .\scripts\postgres_smoke.py`
- staging DB Alembic head now verifies as `20260511_0002`
- staging DB direct admin seed now succeeds after the role-constraint migration
- staging DB direct court-data ingestion verification now succeeds for a unique imported case

## Not Yet Production Ready
- No real deployment pipeline has been completed in this session.
- OpenAI extraction quality has not yet been validated on a real corpus of court documents.
- Handwritten extraction quality is still below the desired standard until that validation is done.
- Regex fallback extraction is still weak.
- Overall UI is still prototype quality outside the improved filing review flow.
- No public self-service signup or identity verification flow exists yet.
- Render and Vercel deployment execution has not been completed from this session because the CLIs/project auth were unavailable locally.
- No scheduled or automated real court data ingestion pipeline exists yet beyond the new manual import script.
- No fully implemented multilingual product architecture exists yet beyond backend translation support.
- The checked-in Render config is not yet in repo-root Blueprint position; immediate staging should use the manual Render dashboard path in `docs/STAGING_RUNBOOK.md`.
- The currently hosted Render backend is not aligned with the repo state as of 2026-05-11:
  - `/auth/login` returns `500`
  - hosted CORS does not admit `https://nyay-justis.vercel.app`
  - hosted OpenAPI still includes `/citizen/search`
  - hosted OpenAPI does not yet include `POST /ocr/translate`
- Current OpenAI-backed OCR/translation verification against repo code is degraded by upstream HTTP `429` responses, causing fallback behavior.

## Current High-Priority Next Steps
1. Validate OpenAI extraction on real legal documents and tune schema/prompts.
2. Execute the Render backend deploy and Vercel frontend deploy using the verified staging database.
3. Seed the first hosted admin account and verify login, admin account creation, and case flows end to end.
4. Expand admin lifecycle and multilingual support beyond the current backend MVP.
5. Build real court-data ingestion automation and deployment observability.
