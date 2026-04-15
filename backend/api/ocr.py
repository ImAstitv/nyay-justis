from fastapi import APIRouter, File, UploadFile, Depends
from services.ocr_service import extract_text
from services.nlp_service import extract_fields
from api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class TextPayload(BaseModel):
    text: str

@router.post("")
async def run_ocr(file: UploadFile = File(...), user=Depends(get_current_user)):
    contents = await file.read()
    return extract_text(contents)

@router.post("/extract")
def run_nlp(payload: TextPayload, user=Depends(get_current_user)):
    return extract_fields(payload.text)