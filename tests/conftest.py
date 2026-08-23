import pytest

from job_search.config import get_settings


@pytest.fixture(autouse=True)
def disable_live_llm(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "openai_api_key", "")
