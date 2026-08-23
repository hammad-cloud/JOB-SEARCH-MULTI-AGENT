"""Thin OpenAI-compatible chat wrapper (OpenAI, Groq, Ollama, Azure)."""

from __future__ import annotations

from openai import OpenAI

from job_search.config import Settings, get_settings


class LLMClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client = OpenAI(
            api_key=self.settings.openai_api_key or "not-set",
            base_url=self.settings.openai_base_url,
        )

    @property
    def is_configured(self) -> bool:
        return bool(self.settings.openai_api_key)

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        if not self.is_configured:
            return ""
        try:
            response = self._client.chat.completions.create(
                model=self.settings.llm_model,
                temperature=self.settings.llm_temperature,
                max_tokens=self.settings.llm_max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except Exception:
            return ""
        return (response.choices[0].message.content or "").strip()
