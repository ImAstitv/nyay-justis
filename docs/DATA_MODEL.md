# Data Model

## User
Defined in `backend/models/models.py`

Fields:
- `id`
- `username`
- `password_hash`
- `role`
- `full_name`
- `created_at`

Roles currently supported:
- `admin`
- `judge`
- `lawyer`

## Case
Fields:
- `id`
- `cnr_number`
- `status`
- `case_type`
- `petitioner`
- `respondent`
- `filed_by_user_id`
- `under_acts`
- `under_sections`
- `filing_date`
- `first_hearing_date`
- `current_stage`
- `establishment_code`
- `primary_case_nature`
- `custody_status`
- `immediate_risk`
- `financial_stake`
- `estimated_severity`
- `is_undertrial`
- `days_in_custody`
- `priority_score`
- `aging_factor`
- `friction_index`
- `vulnerability`
- `stage_coeff`
- `omega_flag`
- `created_at`
- `updated_at`

Current notable statuses:
- `Active`
- `Disposed`

## Hearing
Fields:
- `id`
- `case_id`
- `judge_id`
- `business_on_date`
- `next_hearing_date`
- `purpose_of_hearing`
- `adjournment_reason`
- `adjourned_by`
- `created_at`

## AuditLog
Fields:
- `id`
- `case_id`
- `action`
- `performed_by_role`
- `old_value`
- `new_value`
- `detail`
- `timestamp`

## Needed Future Data Work
- normalized court metadata
- court complexes/benches/jurisdictions
- case history import tables
- cause list import tables
- ingestion provenance
- multilingual content storage
