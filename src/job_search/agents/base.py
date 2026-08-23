"""Shared agent contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from job_search.config import Settings, get_settings
from job_search.llm.client import LLMClient


class BaseAgent(ABC):
    name: str = "base"

    def __init__(
        self,
        settings: Settings | None = None,
        llm: LLMClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.llm = llm or LLMClient(self.settings)

    def load_prompt(self, filename: str) -> str:
        path: Path = self.settings.prompts_dir / filename
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
