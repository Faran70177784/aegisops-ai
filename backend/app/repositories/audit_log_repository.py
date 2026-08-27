from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
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
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_json=metadata_json,
        )

        self.db.add(audit_log)
        self.db.flush()

        return audit_log

    def get_by_id(
        self,
        audit_log_id: int,
    ) -> AuditLog | None:
        return self.db.scalar(
            select(AuditLog).where(
                AuditLog.id == audit_log_id,
            )
        )

    def list_all(
        self,
        *,
        user_id: int | None = None,
        action: str | None = None,
        resource_type: str | None = None,
        resource_id: int | None = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        query = select(AuditLog)

        if user_id is not None:
            query = query.where(
                AuditLog.user_id == user_id,
            )

        if action is not None:
            query = query.where(
                AuditLog.action == action,
            )

        if resource_type is not None:
            query = query.where(
                AuditLog.resource_type == resource_type,
            )

        if resource_id is not None:
            query = query.where(
                AuditLog.resource_id == resource_id,
            )

        query = query.order_by(
            AuditLog.created_at.desc(),
        ).limit(limit)

        return list(self.db.scalars(query).all())