import numpy as np


class OCRExtractionError(Exception):
    pass


def extract_text(image_bytes: bytes) -> dict:
    try:
        import cv2
        import pytesseract
        from PIL import Image

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise OCRExtractionError("The uploaded file could not be decoded as an image")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        pil_img = Image.fromarray(thresh)
        text = pytesseract.image_to_string(pil_img, lang="eng", config="--oem 3 --psm 6")
        if text.strip():
            return {"text": text.strip(), "source": "tesseract"}
        raise OCRExtractionError("OCR completed but no readable text was detected")
    except Exception as exc:
        if isinstance(exc, OCRExtractionError):
            raise
        raise OCRExtractionError(f"OCR failed: {exc}")
