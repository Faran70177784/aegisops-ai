from backend.app.models.audit_log import AuditLog
from backend.app.services.audit_log_service import AuditLogService


def test_audit_log_service_records_log(db_session):
    service = AuditLogService(db_session)

    audit_log = service.record(
        user_id=None,
        action="CREATE",
        resource_type="organization",
        resource_id=1,
        description="Created organization.",
        ip_address="127.0.0.1",
        user_agent="pytest",
        metadata_json={"source": "test"},
    )

    db_session.commit()

    assert audit_log.id is not None
    assert audit_log.action == "CREATE"
    assert audit_log.resource_type == "organization"
    assert audit_log.resource_id == 1
    assert audit_log.description == "Created organization."
    assert audit_log.ip_address == "127.0.0.1"
    assert audit_log.user_agent == "pytest"
    assert audit_log.metadata_json == {"source": "test"}


def test_audit_log_service_gets_log(db_session):
    service = AuditLogService(db_session)

    created = service.record(
        user_id=None,
        action="LOGIN",
        resource_type="authentication",
        description="User login recorded.",
    )

    db_session.commit()

    fetched = service.get(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.action == "LOGIN"


def test_audit_log_service_lists_logs(db_session):
    service = AuditLogService(db_session)

    service.record(
        user_id=None,
        action="CREATE",
        resource_type="organization",
    )

    service.record(
        user_id=None,
        action="UPDATE",
        resource_type="organization",
    )

    db_session.commit()

    logs = service.list(
        resource_type="organization",
    )

    assert len(logs) == 2
    assert all(
        log.resource_type == "organization"
        for log in logs
    )


def test_audit_log_service_filters_by_action(db_session):
    service = AuditLogService(db_session)

    service.record(
        user_id=None,
        action="LOGIN",
        resource_type="authentication",
    )

    service.record(
        user_id=None,
        action="LOGOUT",
        resource_type="authentication",
    )

    db_session.commit()

    logs = service.list(
        action="LOGIN",
    )

    assert len(logs) == 1
    assert logs[0].action == "LOGIN"


def test_audit_log_service_missing_log_returns_none(db_session):
    service = AuditLogService(db_session)

    result = service.get(999999)

    assert result is None