# AI Pipeline

## Current Flow
1. Lawyer uploads image or PDF.
2. OCR endpoint accepts upload at `POST /ocr`.
3. `backend/services/ocr_service.py`:
   - image uploads go through Tesseract
   - PDF uploads are rendered page-by-page via `pypdfium2`, then OCR’d
4. Extracted text is sent to `POST /ocr/extract`.
5. `backend/services/nlp_service.py` performs regex-style extraction.
6. Frontend fills extracted values into editable form fields.

## Current Strengths
- OCR health diagnostics exist via `GET /ocr/health`
- image OCR works once Tesseract is installed and visible in PATH
- PDF OCR support is implemented
- manual editing remains available after extraction

## Current Weaknesses
- handwritten OCR quality is limited
- current NLP extraction is brittle
- no field-level confidence breakdown
- no review queue for low-confidence extraction

## Recommended Future Direction
- keep Tesseract as fallback for typed scans
- add stronger document AI for handwriting and mixed layouts
- move from regex-only extraction to structured extraction
- store extraction confidence and provenance
- highlight uncertain fields in UI for human review

## Operational Checks
- `/ocr/health` should return `ok: true`
- backend process must see Tesseract in PATH
- uploaded PDFs should be tested with multi-page real-world court documents
