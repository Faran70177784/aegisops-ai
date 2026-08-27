from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.rbac import require_role
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.schemas.audit_log import AuditLogListResponse, AuditLogResponse
from backend.app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/admin", tags=["Administration"])


@router.get("/dashboard", summary="Administrator dashboard")
def admin_dashboard(user: User = Depends(require_role("admin"))) -> dict[str, str]:
    return {
        "message": "Welcome to the administrator dashboard.",
        "user": user.email,
        "role": user.role.name,
    }


@router.get("/audit-logs", response_model=AuditLogListResponse, summary="List audit logs")
def list_audit_logs(
    user_id: int | None = Query(default=None, ge=1),
    action: str | None = Query(default=None, min_length=1, max_length=100),
    resource_type: str | None = Query(default=None, min_length=1, max_length=100),
    resource_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> AuditLogListResponse:
    items = AuditLogService(db).list(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        limit=limit,
    )
    return AuditLogListResponse(
        items=[AuditLogResponse.model_validate(item) for item in items],
        count=len(items),
    )


@router.get("/audit-logs/{audit_log_id}", response_model=AuditLogResponse, summary="Get an audit log")
def get_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
) -> AuditLogResponse:
    item = AuditLogService(db).get(audit_log_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found.",
        )
    return AuditLogResponse.model_validate(item)
