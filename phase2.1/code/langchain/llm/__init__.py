# LLM — single entry point for chains and custom pipelines.
from llm.providers.groq import GroqProvider, get_llm_for_chain

from core.config import settings
from llm.base import LLMProvider


def get_llm() -> LLMProvider:
    """Return the LLM for the configured provider (custom pipelines)."""
    provider = (settings.llm_provider or "groq").strip().lower()
    if provider == "groq":
        return GroqProvider()
    raise ValueError(
        f"Unknown LLM_PROVIDER={settings.llm_provider}. "
        "Use groq or add a provider in llm/providers/."
    )


__all__ = ["get_llm", "get_llm_for_chain", "LLMProvider", "GroqProvider"]
