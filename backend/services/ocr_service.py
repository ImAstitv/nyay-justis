import io
import numpy as np

MOCK_TEXT = """DISTRICT COURT, DANAPUR — CIVIL DIVISION

Case No: CRM/2026/147
Nature of Case: Criminal
Under Section: 302/34 IPC
Petitioner: State of Bihar
Respondent: Ramesh Kumar Singh
Procedural Stage: Pre-Trial
The accused is currently in judicial custody (Remand).
Bail application denied by Sessions Court.
Immediate risk: Threat to Life — witness intimidation reported.
Estimated Severity: High
Financial / Property Stake: Disputed agricultural land Rs. 45 Lakhs"""

def extract_text(image_bytes: bytes) -> dict:
    try:
        import pytesseract
        import cv2
        from PIL import Image

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        pil_img = Image.fromarray(thresh)
        text = pytesseract.image_to_string(pil_img, lang='eng', config='--oem 3 --psm 6')
        if text.strip():
            return {"text": text.strip(), "source": "tesseract"}
        raise ValueError("Empty OCR output")
    except Exception as e:
        return {"text": MOCK_TEXT, "source": "mock_ocr", "note": str(e)}