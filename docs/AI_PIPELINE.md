# AI Pipeline

## Current Flow
1. Lawyer uploads image or PDF.
2. `POST /ocr` sends the file to OpenAI Responses API for document extraction.
3. If OpenAI extraction is unavailable, local Tesseract OCR acts as fallback.
4. Extracted text is sent to `POST /ocr/extract`.
5. OpenAI performs structured field extraction for filing metadata.
6. If OpenAI extraction is unavailable, regex extraction remains as fallback.
7. Frontend fills extracted values into editable form fields for human review.

## Current Strengths
- OpenAI can handle PDFs, images, multilingual text, and better semantic extraction than regex-only parsing.
- OCR health diagnostics exist via `GET /ocr/health`.
- Tesseract fallback remains available for local/offline resilience.
- PDF OCR support is implemented.
- Manual editing remains available after extraction.

## Current Weaknesses
- Handwritten extraction quality still needs validation on real court documents.
- Current schema is still limited to the existing filing fields.
- No field-level confidence breakdown yet.
- No review queue for low-confidence extraction.
- Regex fallback is still prototype-grade.

## Recommended Future Direction
- Keep OpenAI as the primary document intelligence provider.
- Keep Tesseract only as a fallback while confidence and cost behavior are validated.
- Store extraction confidence, provenance, and raw model output for auditability.
- Highlight uncertain fields in UI for human review.
- Add multilingual prompt tuning and validation for Indian legal documents.
- Add human-review metrics so extraction quality can be measured, not guessed.

## Operational Checks
- `/ocr/health` should report OpenAI configuration under `document_extraction`.
- If fallback OCR is needed, the backend process must see Tesseract in PATH.
- Uploaded PDFs should be tested with multi-page real-world court documents.
- `OPENAI_API_KEY` must be configured in the backend environment.
