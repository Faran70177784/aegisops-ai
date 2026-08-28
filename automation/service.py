from datetime import datetime, timezone
from backend.app.models.automation import AutomationJob
def create_job(db,name,job_type,payload):
    job=AutomationJob(name=name,job_type=job_type,status="running",payload_json=payload)
    db.add(job); db.commit(); db.refresh(job)
    try:
        if job_type=="health_check":
            result={"status":"ok","timestamp":datetime.now(timezone.utc).isoformat()}
        elif job_type=="echo":
            result={"echo":payload}
        else:
            result={"accepted":True,"job_type":job_type,"payload":payload}
        job.status="completed"; job.result_json=result; db.commit(); db.refresh(job)
    except Exception as exc:
        job.status="failed"; job.error=str(exc); db.commit()
    return job
