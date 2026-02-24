"""Initial FastAPI backend scaffold."""

from fastapi import FastAPI

from app.api.routes.upload import router as upload_router

# Initial scaffold: this app only provides a basic health-check endpoint.
# No database, upload parsing, or AI interpretation logic is included at this stage.
app = FastAPI()
app.include_router(upload_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Initial scaffold health endpoint."""
    return {"status": "ok"}
