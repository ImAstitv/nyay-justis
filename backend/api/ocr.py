from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from core.config import settings
from services.nlp_service import extract_fields
from services.openai_extraction_service import (
    OpenAIExtractionError,
    extract_case_fields_with_openai,
    extract_document_text,
    get_openai_extraction_health,
    translate_legal_text,
)
from services.ocr_service import OCRExtractionError, extract_text, get_ocr_health
from api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

ALLOWED_OCR_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "application/pdf",
}

class TextPayload(BaseModel):
    text: str


class TranslatePayload(BaseModel):
    text: str
    target_language: str | None = None

@router.post("")
async def run_ocr(file: UploadFile = File(...), user=Depends(get_current_user)):
    if file.content_type not in ALLOWED_OCR_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Supported types: JPEG, PNG, WEBP, PDF.",
        )
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    try:
        return extract_document_text(contents, file.content_type, file.filename)
    except OpenAIExtractionError:
        try:
            fallback = extract_text(contents, file.content_type)
            fallback["fallback_used"] = True
            fallback["fallback_provider"] = "tesseract"
            return fallback
        except OCRExtractionError as exc:
            raise HTTPException(status_code=422, detail=str(exc))


@router.get("/health")
def ocr_health(user=Depends(get_current_user)):
    return {
        "primary_provider": "openai",
        "document_extraction": get_openai_extraction_health(),
        "fallback_ocr": get_ocr_health(),
    }

@router.post("/extract")
def run_nlp(payload: TextPayload, user=Depends(get_current_user)):
    try:
        return extract_case_fields_with_openai(payload.text)
    except OpenAIExtractionError:
        fallback = extract_fields(payload.text)
        fallback["provider"] = "regex_fallback"
        fallback["warnings"] = ["OpenAI extraction unavailable; regex fallback used."]
        fallback["missing_fields"] = []
        fallback["language"] = "unknown"
        fallback["summary"] = "Fallback extraction was used because OpenAI extraction was unavailable."
        return fallback


@router.post("/translate")
def run_translation(payload: TranslatePayload, user=Depends(get_current_user)):
    target_language = payload.target_language or settings.MULTILINGUAL_TARGET_LANGUAGE
    if not settings.ENABLE_MULTILINGUAL_PIPELINE:
        return {
            "source_language": "unknown",
            "target_language": target_language,
            "translated_text": payload.text,
            "notes": ["Multilingual pipeline disabled; returning original text."],
            "provider": "disabled",
        }
    try:
        return translate_legal_text(payload.text, target_language)
    except OpenAIExtractionError:
        return {
            "source_language": "unknown",
            "target_language": target_language,
            "translated_text": payload.text,
            "notes": ["OpenAI translation unavailable; returning original text."],
            "provider": "fallback_original",
        }
