# Roadmap

## Phase 1: Stable Baseline
- Remove runtime seeding
- Add cookie-based auth
- Add migrations
- Add backend tests
- Add OCR health and PDF OCR
- Status: largely complete

## Phase 2: Real Product Work
- Real account lifecycle
  - signup or invite flow
  - create-account UI
  - password reset
  - account disable/lock
- Real database posture
  - PostgreSQL
  - migration discipline
  - staging/prod environments
- Real document intelligence
  - better OCR for handwriting
  - stronger NLP extraction
  - confidence scoring and fallback review
- Real UX
  - redesign to court-grade look and feel
  - mobile responsiveness
  - dark/light theme switch
  - editable extraction results
- Real multilingual support
  - i18n framework
  - Sarvam AI integration
  - Hindi and Indian language switching
- Real deployment
  - domain, HTTPS, CI/CD, observability

## Phase 3: Court Data Platform
- Cause list ingestion
- Case history ingestion
- provenance and auditability
- schedule refresh/update jobs
- case search and reconciliation

## Recommended Order
1. Sync repo and push clean baseline
2. PostgreSQL + staging
3. Better OCR/NLP
4. Frontend redesign
5. Multilingual support
6. Real court data ingestion
7. Production deployment
