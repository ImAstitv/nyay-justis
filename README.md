# NYAY – Judicial Case Prioritization Initiative

NYAY is a judicial decision-support initiative designed to assist courts in
prioritizing cases for scheduling based on the potential irreversible harm
caused by procedural delays.

NYAY does not adjudicate cases, assess merits, or replace judicial discretion.
All outputs are advisory in nature.

This project is powered by **JUSTIS** 
(Judicial Unified Scheduling & Triage Information System).

---

## Purpose

Courts often follow a first-in-first-out approach to scheduling hearings.
While simple, this method does not account for situations where delay itself
causes irreversible harm, such as prolonged custody, risk of eviction, or
severe livelihood disruption.

NYAY aims to support judicial scheduling by highlighting cases where delay
sensitivity is higher, while ensuring that final authority always rests with
the Hon’ble Court.

---

## Core Principles

- Advisory-only decision support
- No prediction of case outcomes
- No assessment of guilt, innocence, or truth
- Explainable and overrideable recommendations
- Clear separation between data ingestion, analysis, and judicial control

---

## System Overview

The NYAY initiative is implemented through JUSTIS, a full-stack web system
built with a modular architecture:

- Frontend: React-based judicial and clerical interface
- Backend: FastAPI orchestration layer
- AI Services: Interpretation and delay-impact analysis (bounded and explainable)
- Database: PostgreSQL with strict relational integrity and auditability

---

## Intake Modes

The system supports two case intake workflows:

1. **Manual Intake**  
   Structured data entry for clerks or authorized users using controlled
   fields and validations.

2. **AI-Assisted File Upload**  
   Drag-and-drop ingestion of structured case data files (CSV, XLSX, PDF),
   followed by AI-assisted extraction and interpretation with confidence
   scoring and human review.

Both workflows converge into the same validated case schema.

---

## Ethical & Legal Safeguards

- AI interpretation is confidence-scored and reviewable
- AI influence on scheduling is capped and explainable
- Judicial override is always permitted and logged
- All critical actions are auditable

---

## Project Status

This repository is under active development.

Current focus:
- Core project scaffolding
- AI-assisted intake and interpretation (Module 0)
- Backend and frontend foundations

Subsequent modules will add scheduling logic, explainability, and judicial
dashboards incrementally.

---

## Disclaimer

NYAY assists judicial scheduling by highlighting delay-sensitive cases.
Final authority always rests with the Hon’ble Court.
