from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.automation import AutomationJob
from backend.app.schemas.automation import AutomationCreate
from automation.service import create_job
router=APIRouter(prefix="/automation",tags=["Automation"])
@router.post("/jobs")
def create(data:AutomationCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    j=create_job(db,data.name,data.job_type,data.payload)
    return {"id":j.id,"name":j.name,"job_type":j.job_type,"status":j.status,"result":j.result_json,"error":j.error}
@router.get("/jobs")
def list_jobs(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    jobs=db.scalars(select(AutomationJob).order_by(AutomationJob.created_at.desc()).limit(100)).all()
    return [{"id":j.id,"name":j.name,"job_type":j.job_type,"status":j.status,"result":j.result_json,"error":j.error} for j in jobs]
