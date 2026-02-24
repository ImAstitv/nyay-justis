"""File upload route for accepted document types."""

from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/upload", tags=["upload"])

_ALLOWED_EXTENSIONS = {"csv", "xlsx", "pdf"}

# Temporary in-memory metadata store.
# TODO: Persist upload metadata in a proper database model.
uploaded_files_metadata: list[dict[str, str]] = []


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """Accept a supported file upload and store basic metadata only."""
    filename = file.filename or ""
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed types: CSV, XLSX, PDF.",
        )

    metadata = {
        "filename": filename,
        "file_type": extension,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    uploaded_files_metadata.append(metadata)

    # TODO: Add file parsing logic (CSV/XLSX/PDF content extraction).
    # TODO: Add AI interpretation pipeline after parsing is implemented.

    return metadata
