from pydantic import BaseModel, Field
class AutomationCreate(BaseModel):
    name:str=Field(min_length=2,max_length=150)
    job_type:str=Field(min_length=2,max_length=80)
    payload:dict={}
class AutomationResponse(BaseModel):
    id:int; name:str; job_type:str; status:str; result:dict|None=None; error:str|None=None
