import logging

from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.services.audit_log_service import AuditLogService

logger = logging.getLogger(__name__)


def request_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def request_user_agent(request: Request) -> str | None:
    value = request.headers.get("user-agent")
    return value[:500] if value else None


def record_audit(
    db: Session,
    request: Request,
    *,
    user_id: int | None,
    action: str,
    resource_type: str,
    resource_id: int | None = None,
    description: str | None = None,
    metadata_json: dict | None = None,
) -> None:
    try:
        AuditLogService(db).record(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            ip_address=request_ip(request),
            user_agent=request_user_agent(request),
            metadata_json=metadata_json,
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to persist audit log for action=%s", action)
