from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    resource_type: str
    resource_id: int | None
    description: str | None
    ip_address: str | None
    user_agent: str | None
    metadata_json: dict | None
    created_at: datetime


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    count: int = Field(ge=0)
