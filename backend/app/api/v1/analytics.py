from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from analytics.service import dashboard_metrics
router=APIRouter(prefix="/analytics",tags=["Business Intelligence"])
@router.get("/dashboard")
def dashboard(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return dashboard_metrics(db)
@router.get("/overview")
def overview(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    m=dashboard_metrics(db)
    return {"metrics":m,"insights":[
        {"name":"Knowledge Coverage","value":m["knowledge_documents"],"description":"Indexed enterprise documents"},
        {"name":"Automation Activity","value":m["automation_jobs"],"description":"Automation jobs recorded"},
        {"name":"Audit Activity","value":m["audit_events"],"description":"Auditable system events"},
    ]}
