from groq import Groq

from core.config import settings


class GroqProvider:
    def __init__(self):
        if not settings.groq_api_key or not settings.groq_model:
            raise ValueError("Set GROQ_API_KEY and GROQ_MODEL when LLM_PROVIDER=groq")
        self._client = Groq(api_key=settings.groq_api_key)
        self._model = settings.groq_model

        
    def generate(self, system: str, user: str, max_tokens: int = 512) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()