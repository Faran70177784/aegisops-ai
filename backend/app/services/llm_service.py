import httpx
from backend.app.core.config import settings
class LLMService:
    async def generate(self,prompt:str)->str:
        if settings.llm_provider.lower()=="ollama":
            async with httpx.AsyncClient(timeout=90) as client:
                r=await client.post("http://host.docker.internal:11434/api/generate",json={"model":settings.llm_model,"prompt":prompt,"stream":False})
                r.raise_for_status()
                return r.json().get("response","").strip()
        return "LLM provider is configured but no remote adapter is enabled. Set LLM_PROVIDER=ollama for local inference."
llm_service=LLMService()
