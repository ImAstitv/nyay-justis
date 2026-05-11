# Staging MVP Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a deployable staging MVP on Supabase Postgres + Render + Vercel, with the smallest viable multilingual and court-data-ingestion scaffolding that supports the current product direction.

**Architecture:** Keep the existing FastAPI + React/Vite structure intact, harden deployment/runtime configuration for hosted environments, and extend the OpenAI-first backend with narrowly scoped multilingual and ingestion helpers. Prioritize staging readiness, verification, and handoff clarity over broad new feature surface.

**Tech Stack:** FastAPI, SQLAlchemy, Alembic, PostgreSQL (Supabase), React, Vite, Render Docker deploy, Vercel static deploy, OpenAI Responses API

---

### Task 1: Harden Hosted Runtime Configuration

**Files:**
- Modify: `backend/Dockerfile`
- Modify: `backend/render.yaml`
- Modify: `docs/DEPLOYMENT.md`

- [ ] Ensure the backend container respects hosted runtime port expectations.
- [ ] Add any missing Render env/config notes required for staging deploy.
- [ ] Document the exact staging environment contract for backend and frontend.

### Task 2: Add Minimal Multilingual Pipeline Support

**Files:**
- Modify: `backend/core/config.py`
- Modify: `backend/services/openai_extraction_service.py`
- Modify: `backend/api/ocr.py`
- Modify: `docs/ROADMAP.md`

- [ ] Add a small configuration surface for multilingual processing that does not break the current OCR flow.
- [ ] Extend the OpenAI extraction pipeline to expose language-aware outputs useful for staging verification.
- [ ] Keep the scope backend-first so multilingual document handling can be tested without a full frontend i18n rollout.

### Task 3: Add Minimal Court-Data Ingestion Scaffolding

**Files:**
- Create: `backend/scripts/ingest_court_data.py`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/STATUS.md`

- [ ] Add a simple ingestion entrypoint for staged CSV/JSON court data imports.
- [ ] Keep the first version file-driven and operator-run, not a full scheduled pipeline.
- [ ] Document what format is supported and what remains future work.

### Task 4: Verify Staging Readiness

**Files:**
- Modify: `docs/HANDOFF.md`
- Modify: `CONTEXT.md`

- [ ] Run hosted DB migration and smoke verification against Supabase.
- [ ] Run backend tests/build checks and frontend build checks after code changes.
- [ ] Record the exact verified commands, outcomes, and remaining external blockers.

