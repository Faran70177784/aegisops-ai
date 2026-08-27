from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from sqlalchemy.exc import IntegrityError

from backend.app.api.v1 import api_router
from backend.app.core.config import settings
from backend.app.core.exceptions import integrity_exception_handler, unhandled_exception_handler, validation_exception_handler
from backend.app.core.logging import configure_logging
from backend.app.middleware.security import SecurityHeadersMiddleware

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AegisOps AI - Enterprise Operations Command Center. "
        "An enterprise AI platform combining RAG, hybrid search, "
        "multi-agent workflows, business intelligence, automation, "
        "enterprise knowledge management, RBAC, and auditability."
    ),
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

if settings.environment.lower() == "production" and settings.allowed_host_list:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_host_list)

if settings.cors_origin_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["System"], summary="Application information")
async def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "online",
    }


@app.get("/health", tags=["System"], summary="Health check")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
