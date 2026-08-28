from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.models.knowledge import KnowledgeDocument, KnowledgeChunk
from backend.app.schemas.knowledge import DocumentCreate, DocumentResponse, SearchRequest, SearchResponse
from rag.ingestion import extract_text, content_hash, chunk_text
from search.engine import search_chunks

router=APIRouter(prefix="/knowledge",tags=["Knowledge Management"])

@router.post("/documents",response_model=DocumentResponse,status_code=201)
def create_document(data:DocumentCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    h=content_hash(data.content)
    if db.scalar(select(KnowledgeDocument).where(KnowledgeDocument.content_hash==h)):
        raise HTTPException(409,"A document with identical content already exists.")
    chunks=chunk_text(data.content)
    doc=KnowledgeDocument(title=data.title,source=data.source,content=data.content,content_hash=h,chunk_count=len(chunks),metadata_json=data.metadata)
    db.add(doc); db.flush()
    for i,c in enumerate(chunks): db.add(KnowledgeChunk(document_id=doc.id,chunk_index=i,content=c,metadata_json={"title":data.title}))
    db.commit(); db.refresh(doc)
    return {"id":doc.id,"title":doc.title,"source":doc.source,"chunk_count":doc.chunk_count,"created_at":doc.created_at.isoformat()}

@router.post("/documents/upload",response_model=DocumentResponse,status_code=201)
async def upload_document(file:UploadFile=File(...),db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    data=await file.read()
    try: text=extract_text(file.filename or "upload.txt",data)
    except ValueError as e: raise HTTPException(400,str(e)) from e
    if not text.strip(): raise HTTPException(400,"The uploaded file contains no extractable text.")
    h=content_hash(text)
    if db.scalar(select(KnowledgeDocument).where(KnowledgeDocument.content_hash==h)): raise HTTPException(409,"A document with identical content already exists.")
    chunks=chunk_text(text)
    doc=KnowledgeDocument(title=file.filename or "Uploaded document",source=file.filename or "upload",content=text,content_hash=h,chunk_count=len(chunks),metadata_json={"content_type":file.content_type})
    db.add(doc); db.flush()
    for i,c in enumerate(chunks): db.add(KnowledgeChunk(document_id=doc.id,chunk_index=i,content=c,metadata_json={"filename":file.filename}))
    db.commit(); db.refresh(doc)
    return {"id":doc.id,"title":doc.title,"source":doc.source,"chunk_count":doc.chunk_count,"created_at":doc.created_at.isoformat()}

@router.get("/documents")
def list_documents(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    docs=db.scalars(select(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc())).all()
    return [{"id":d.id,"title":d.title,"source":d.source,"chunk_count":d.chunk_count,"created_at":d.created_at.isoformat()} for d in docs]

@router.post("/search",response_model=SearchResponse)
def search(data:SearchRequest,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return {"query":data.query,"results":search_chunks(db,data.query,data.top_k)}
