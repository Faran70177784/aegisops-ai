from fastapi import APIRouter, Depends
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.agents import WorkflowRequest,WorkflowResponse
from agents.orchestrator.workflow import run_workflow
router=APIRouter(prefix="/workflows",tags=["Agents / Workflows"])
@router.post("/run",response_model=WorkflowResponse)
def run(data:WorkflowRequest,user:User=Depends(get_current_user)):
    return {"workflow":data.workflow,"status":"completed","result":run_workflow(data.workflow,data.input)}
@router.get("")
def list_workflows(user:User=Depends(get_current_user)):
    return {"workflows":["health_check","incident_triage","summarize","operations_triage"]}
