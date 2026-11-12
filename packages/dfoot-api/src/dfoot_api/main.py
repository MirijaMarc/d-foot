"""FastAPI application. Run with: uvicorn dfoot_api.main:app"""

from fastapi import FastAPI

app = FastAPI(title="D-Foot API")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: answers as long as the process is up."""
    return {"status": "ok"}
