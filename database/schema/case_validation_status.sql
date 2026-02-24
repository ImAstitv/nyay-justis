CREATE TABLE case_validation_status (
    staging_id INTEGER PRIMARY KEY REFERENCES case_interpretation_staging(staging_id),
    status TEXT NOT NULL, -- auto_approved | needs_review
    reviewed_by TEXT,
    review_notes TEXT,
    reviewed_at TIMESTAMP
);