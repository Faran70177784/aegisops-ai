from rag.ingestion import chunk_text, content_hash
from search.vector_store import vector_score

def test_chunking_and_hash():
    text="Enterprise operations require reliable controls. " * 100
    chunks=chunk_text(text,chunk_size=300,overlap=40)
    assert len(chunks)>1
    assert content_hash(text)==content_hash(text)

def test_vector_similarity():
    assert vector_score("incident operations","incident operations response") > vector_score("incident operations","financial accounting")
