# Roadmap

## Phase 1: Stable Baseline
- Remove runtime seeding
- Add cookie-based auth
- Add migrations
- Add backend tests
- Add OCR health and PDF OCR
- Status: largely complete

## Phase 2: Real Product Work
- OpenAI-first document intelligence
  - document extraction from PDFs/images
  - structured case field extraction
  - human review and correction workflow
  - confidence/provenance tracking
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
  - better handwritten extraction quality
  - multilingual legal document extraction
  - confidence scoring and fallback review
- Real UX
  - redesign to court-grade look and feel
  - mobile responsiveness
  - dark/light theme switch
  - editable extraction results
- Real multilingual support
  - i18n framework
  - OpenAI language workflows
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
1. Validate OpenAI extraction on real documents
2. PostgreSQL + staging
3. Frontend redesign and create-account flow
4. Multilingual support
5. Real court data ingestion
6. Production deployment
