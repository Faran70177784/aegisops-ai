from pydantic import BaseModel, Field
class WorkflowRequest(BaseModel):
    workflow:str=Field(min_length=2,max_length=100)
    input:dict={}
class WorkflowResponse(BaseModel):
    workflow:str; status:str; result:dict
