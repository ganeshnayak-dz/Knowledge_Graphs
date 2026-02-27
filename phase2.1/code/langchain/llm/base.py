"""Base interface for LLM providers. Implement in providers/ for Groq, OpenAI, etc. Fill as you learn."""

from typing import Protocol, runtime_checkable

@runtime_checkable
class LLMProvider(Protocol):
    """Implement this for each LLM (Groq, Gemini, etc.). Rest of app uses only this interface."""

    def generate(self,system:str,user:str,max_tokens:int=512) -> str:
        """Generate a response from the LLM."""
        ...