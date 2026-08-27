from sqlalchemy.orm import Session

from backend.app.models.audit_log import AuditLog
from backend.app.repositories.audit_log_repository import (
    AuditLogRepository,
)


class AuditLogService:
    def __init__(self, db: Session):
        self.repository = AuditLogRepository(db)

    def record(
        self,
        *,
        user_id: int | None,
        action: str,
        resource_type: str,
        resource_id: int | None = None,
        description: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata_json: dict | None = None,
    ) -> AuditLog:
        return self.repository.create(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_json=metadata_json,
        )

    def get(
        self,
        audit_log_id: int,
    ) -> AuditLog | None:
        return self.repository.get_by_id(
            audit_log_id,
        )

    def list(
        self,
        *,
        user_id: int | None = None,
        action: str | None = None,
        resource_type: str | None = None,
        resource_id: int | None = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        return self.repository.list_all(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            limit=limit,
        )