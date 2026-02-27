# LangChain KG — fill as you learn.


from core.config import settings

from llm.base import LLMProvider
from llm.providers import GroqProvider

def get_llm() -> LLMProvider:
    """Return the LLM for the configured provider. Change LLM = change .env + one provider file."""
    provider = (settings.llm_provider or "groq").strip().lower()
    if provider == "groq":
        return GroqProvider()
    raise ValueError(f"Unknown LLM_PROVIDER={settings.llm_provider}. Use groq, gemini, or add in llm/providers/.")

def get_llm_for_chain() -> ChatGroq:
    if settings.llm_provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=settings.groq_model, 
        api_key=settings.groq_api_key,
        temperature=0.0)
    raise ValueError(f"Unknown LLM_PROVIDER={settings.llm_provider}. Use groq, gemini, or add in llm/providers/.")