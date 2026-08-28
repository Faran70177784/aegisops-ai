from pydantic import BaseModel, Field
class DocumentCreate(BaseModel):
    title: str = Field(min_length=2,max_length=255)
    source: str = Field(min_length=1,max_length=500)
    content: str = Field(min_length=1)
    metadata: dict | None = None
class DocumentResponse(BaseModel):
    id:int; title:str; source:str; chunk_count:int; created_at:str
class SearchRequest(BaseModel):
    query:str=Field(min_length=2,max_length=1000)
    top_k:int=Field(default=5,ge=1,le=20)
class SearchResult(BaseModel):
    document_id:int; document_title:str; chunk_id:int; score:float; content:str
class SearchResponse(BaseModel):
    query:str; results:list[SearchResult]
