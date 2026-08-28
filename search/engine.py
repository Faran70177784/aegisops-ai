import re
from sqlalchemy import select
from backend.app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from search.vector_store import vector_score
STOP=set("the a an and or is are to of in on for with from by this that as at be it".split())
def _terms(q): return [x for x in re.findall(r"[a-z0-9_]+",q.lower()) if x not in STOP]
def search_chunks(db, query, top_k=5):
    terms=_terms(query); rows=db.execute(select(KnowledgeChunk,KnowledgeDocument).join(KnowledgeDocument,KnowledgeDocument.id==KnowledgeChunk.document_id)).all()
    scored=[]
    for chunk,doc in rows:
        hay=chunk.content.lower()
        lexical=sum(hay.count(t) for t in terms)
        vector=vector_score(query,chunk.content)
        score=(0.65*(lexical/(len(terms) or 1)))+(0.35*vector)
        if lexical or vector>0.05: scored.append((score,chunk,doc,lexical,vector))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [{"document_id":d.id,"document_title":d.title,"chunk_id":c.id,"score":round(float(s),4),"content":c.content,"lexical_score":l,"vector_score":round(v,4)} for s,c,d,l,v in scored[:top_k]]
