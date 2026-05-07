import numpy as np


class OCRExtractionError(Exception):
    pass


PDF_SIGNATURE = b"%PDF"
MAX_PDF_PAGES = 5


def _is_pdf(file_bytes: bytes, content_type: str | None) -> bool:
    return content_type == "application/pdf" or file_bytes.startswith(PDF_SIGNATURE)


def _ocr_image_bytes(image_bytes: bytes) -> str:
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
        return text.strip()
    raise OCRExtractionError("OCR completed but no readable text was detected")


def _ocr_pdf_bytes(file_bytes: bytes) -> dict:
    import io

    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(io.BytesIO(file_bytes))
    total_pages = len(pdf)
    if total_pages == 0:
        raise OCRExtractionError("The uploaded PDF has no pages")

    pages_to_process = min(total_pages, MAX_PDF_PAGES)
    extracted_pages = []

    for page_index in range(pages_to_process):
        page = pdf.get_page(page_index)
        try:
            bitmap = page.render(scale=2.0)
            pil_image = bitmap.to_pil()
            with io.BytesIO() as buffer:
                pil_image.save(buffer, format="PNG")
                page_text = _ocr_image_bytes(buffer.getvalue())
            extracted_pages.append(page_text)
        finally:
            page.close()

    combined_text = "\n\n".join(text for text in extracted_pages if text.strip())
    if not combined_text.strip():
        raise OCRExtractionError("OCR completed but no readable text was detected in the PDF")

    return {
        "text": combined_text,
        "source": "tesseract_pdf",
        "pages_processed": pages_to_process,
        "total_pages": total_pages,
    }


def get_ocr_health() -> dict:
    try:
        import pytesseract
        import pypdfium2

        version = str(pytesseract.get_tesseract_version())
        executable = getattr(pytesseract.pytesseract, "tesseract_cmd", "tesseract")
        return {
            "ok": True,
            "engine": "tesseract",
            "version": version,
            "executable": executable,
            "pdf_renderer": "pypdfium2",
            "pdf_renderer_version": getattr(pypdfium2, "__version__", "unknown"),
        }
    except Exception as exc:
        return {
            "ok": False,
            "engine": "tesseract",
            "error": str(exc),
        }


def extract_text(file_bytes: bytes, content_type: str | None = None) -> dict:
    try:
        if _is_pdf(file_bytes, content_type):
            return _ocr_pdf_bytes(file_bytes)

        return {"text": _ocr_image_bytes(file_bytes), "source": "tesseract"}
    except Exception as exc:
        if isinstance(exc, OCRExtractionError):
            raise
        raise OCRExtractionError(f"OCR failed: {exc}")
