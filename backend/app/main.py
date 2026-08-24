from fastapi import FastAPI

from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AegisOps AI — Enterprise Operations Command Center. "
        "An enterprise AI platform combining RAG, hybrid search, "
        "multi-agent workflows, business intelligence, automation, "
        "and enterprise knowledge management."
    ),
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "online",
    }


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }