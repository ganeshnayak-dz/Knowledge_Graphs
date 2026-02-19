from core.config import settings

from llm.base import LLMProvider
from llm.providers import GroqProvider



def get_llm() -> LLMProvider:
    """Return the LLM for the configured provider. Change LLM = change .env + one provider file."""
    provider = (settings.llm_provider or "groq").strip().lower()
    if provider == "groq":
        return GroqProvider()
    raise ValueError(f"Unknown LLM_PROVIDER={settings.llm_provider}. Use groq, gemini, or add in llm/providers/.")