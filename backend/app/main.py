"""Initial FastAPI backend scaffold."""

from fastapi import FastAPI

# Initial scaffold: this app only provides a basic health-check endpoint.
# No database, upload, or AI logic is included at this stage.
app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Initial scaffold health endpoint."""
    return {"status": "ok"}
