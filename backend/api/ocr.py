from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from services.nlp_service import extract_fields
from services.ocr_service import OCRExtractionError, extract_text
from api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class TextPayload(BaseModel):
    text: str

@router.post("")
async def run_ocr(file: UploadFile = File(...), user=Depends(get_current_user)):
    contents = await file.read()
    try:
        return extract_text(contents)
    except OCRExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@router.post("/extract")
def run_nlp(payload: TextPayload, user=Depends(get_current_user)):
    return extract_fields(payload.text)
