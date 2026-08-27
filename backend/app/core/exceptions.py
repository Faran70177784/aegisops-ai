from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def _error_response(
    status_code: int,
    message: str,
    *,
    details: Any = None,
) -> JSONResponse:
    content = {
        "success": False,
        "error": {
            "code": status_code,
            "message": message,
        },
    }

    if details is not None:
        content["error"]["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Request validation failed.",
        details=exc.errors(),
    )


async def integrity_exception_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return _error_response(
        status.HTTP_409_CONFLICT,
        "The requested operation violates a database constraint.",
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "An unexpected internal server error occurred.",
    )
