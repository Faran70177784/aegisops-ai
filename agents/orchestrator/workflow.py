from datetime import datetime, timezone
def run_workflow(name:str, payload:dict)->dict:
    n=name.lower().replace(" ","_")
    if n in {"summarize","summarization"}:
        text=str(payload.get("text",""))
        return {"summary": text[:800] + ("..." if len(text)>800 else ""), "generated_at":datetime.now(timezone.utc).isoformat()}
    if n in {"health_check","system_health"}:
        return {"status":"operational","checks":["api","database","knowledge","automation"]}
    if n in {"incident_triage","operations_triage"}:
        return {"priority":payload.get("priority","medium"),"classification":payload.get("category","general"),"next_action":"Assign to operations queue"}
    return {"message":"Workflow accepted","workflow":name,"input":payload}
