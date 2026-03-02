"""Groq LLM provider via LangChain ChatGroq. Implements LLMProvider for custom pipelines."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from core.config import settings
from llm.base import LLMProvider


def get_llm_for_chain():
    """Return a LangChain ChatGroq instance for use in chains (e.g. GraphCypherQAChain)."""
    if not settings.groq_api_key or not settings.groq_model:
        raise ValueError("Set GROQ_API_KEY and GROQ_MODEL in .env when using Groq for chains")
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0,
    )


class GroqProvider:
    """Implements LLMProvider using LangChain's ChatGroq. Used by get_llm()."""

    def __init__(self) -> None:
        if not settings.groq_api_key or not settings.groq_model:
            raise ValueError(
                "Set GROQ_API_KEY and GROQ_MODEL in .env when LLM_PROVIDER=groq"
            )
        self._llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0,
        )

    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 512,
    ) -> str:
        messages = [
            SystemMessage(content=system),
            HumanMessage(content=user),
        ]
        response = self._llm.invoke(messages, max_tokens=max_tokens)
        return (response.content or "").strip()
