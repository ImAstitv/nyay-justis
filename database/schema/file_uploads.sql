CREATE TABLE file_uploads (
    upload_id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    ingestion_mode TEXT NOT NULL, -- manual | ai_assisted
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);