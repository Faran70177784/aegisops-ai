from datetime import datetime

from backend.app.models.audit_log import AuditLog


def test_audit_log_model_has_expected_columns():
    columns = {column.name for column in AuditLog.__table__.columns}

    assert columns == {
        "id",
        "user_id",
        "action",
        "resource_type",
        "resource_id",
        "description",
        "ip_address",
        "user_agent",
        "metadata_json",
        "created_at",
    }


def test_audit_log_timestamp_is_generated(db_session):
    item = AuditLog(action="LOGIN", resource_type="authentication")
    db_session.add(item)
    db_session.commit()
    assert isinstance(item.created_at, datetime)
