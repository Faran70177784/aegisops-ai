from pathlib import Path
import hashlib
from pypdf import PdfReader

def extract_text(filename:str, data:bytes)->str:
    suffix=Path(filename).suffix.lower()
    if suffix==".pdf":
        import io
        reader=PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix in {".txt",".md",".csv",".json",".py",".log",".yaml",".yml"}:
        return data.decode("utf-8", errors="replace")
    raise ValueError("Unsupported file type. Use PDF, TXT, Markdown, CSV, JSON, YAML, or text-based source files.")

def content_hash(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def chunk_text(text:str, chunk_size:int=1200, overlap:int=150)->list[str]:
    text=" ".join(text.split())
    if not text: return []
    chunks=[]; start=0
    while start<len(text):
        end=min(len(text),start+chunk_size)
        if end<len(text):
            boundary=max(text.rfind(". ",start,end),text.rfind("\n",start,end))
            if boundary>start+chunk_size//2: end=boundary+1
        chunks.append(text[start:end].strip())
        if end>=len(text): break
        start=max(end-overlap,start+1)
    return chunks
