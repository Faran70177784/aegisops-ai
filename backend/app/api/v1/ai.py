from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.ai import ChatRequest, ChatResponse
from search.engine import search_chunks
from backend.app.services.llm_service import llm_service
from backend.app.core.config import settings
router=APIRouter(prefix="/ai",tags=["AI / LLM"])
@router.post("/chat",response_model=ChatResponse)
async def chat(data:ChatRequest,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    sources=search_chunks(db,data.prompt,4) if data.use_knowledge else []
    context="\n\n".join(f"[{x['document_title']}] {x['content']}" for x in sources)
    prompt=("You are AegisOps AI, an enterprise operations assistant. "
            "Answer accurately and concisely. If context is supplied, ground the answer in it. "
            "Do not invent facts.\n\nCONTEXT:\n"+context+"\n\nUSER:\n"+data.prompt)
    try: answer=await llm_service.generate(prompt)
    except Exception as exc: answer=f"LLM unavailable: {exc}"
    return {"answer":answer,"provider":settings.llm_provider,"model":settings.llm_model,
            "sources":[{"document_id":x["document_id"],"title":x["document_title"],"score":x["score"]} for x in sources]}
