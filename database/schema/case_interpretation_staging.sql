CREATE TABLE case_interpretation_staging (
    staging_id SERIAL PRIMARY KEY,
    raw_id INTEGER REFERENCES case_raw_extractions(raw_id),

    inferred_case_nature TEXT,
    case_nature_confidence FLOAT,

    inferred_procedural_stage TEXT,
    procedural_stage_confidence FLOAT,

    inferred_custody_status TEXT,
    custody_confidence FLOAT,

    inferred_property_livelihood_risk BOOLEAN,
    risk_confidence FLOAT,

    inferred_severity_band TEXT,
    severity_confidence FLOAT,

    inferred_petitioner_age_band TEXT,
    age_confidence FLOAT,

    inferred_case_complexity TEXT,
    complexity_confidence FLOAT,

    model_version TEXT,
    interpreted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);