from agents.orchestrator.workflow import run_workflow
def test_health_workflow():
    result=run_workflow("health_check",{})
    assert result["status"]=="operational"
def test_triage_workflow():
    result=run_workflow("incident_triage",{"category":"database","priority":"high"})
    assert result["priority"]=="high"
