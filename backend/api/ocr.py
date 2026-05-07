from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from services.nlp_service import extract_fields
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
        return extract_text(contents, file.content_type)
    except OCRExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/health")
def ocr_health(user=Depends(get_current_user)):
    return get_ocr_health()

@router.post("/extract")
def run_nlp(payload: TextPayload, user=Depends(get_current_user)):
    return extract_fields(payload.text)
