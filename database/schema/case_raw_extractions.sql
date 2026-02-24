CREATE TABLE case_raw_extractions (
    raw_id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES file_uploads(upload_id),
    extracted_type TEXT NOT NULL, -- pdf | csv | xlsx
    raw_text TEXT,
    raw_rows JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);