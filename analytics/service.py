from sqlalchemy import func, select
from backend.app.models.user import User
from backend.app.models.organization import Organization
from backend.app.models.audit_log import AuditLog
from backend.app.models.knowledge import KnowledgeDocument
from backend.app.models.automation import AutomationJob
def dashboard_metrics(db):
    return {
        "users": db.scalar(select(func.count(User.id))) or 0,
        "organizations": db.scalar(select(func.count(Organization.id))) or 0,
        "audit_events": db.scalar(select(func.count(AuditLog.id))) or 0,
        "knowledge_documents": db.scalar(select(func.count(KnowledgeDocument.id))) or 0,
        "automation_jobs": db.scalar(select(func.count(AutomationJob.id))) or 0,
    }
