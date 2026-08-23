"""Application settings loaded from YAML, then overridden by environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "settings.yaml"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Multi-Agent Job Search"
    log_level: str = "INFO"
    data_dir: Path = ROOT_DIR / "data"
    use_mock_jobs: bool = True
    use_llm: bool = False

    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 2000
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"

    adzuna_app_id: str = ""
    adzuna_app_key: str = ""

    default_location: str = "Remote"
    results_limit: int = 25
    top_matches: int = 5
    country: str = "us"
    min_score: int = 40

    prompts_dir: Path = Field(default=ROOT_DIR / "prompts")


def _load_yaml() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return {
        "app_name": raw.get("app", {}).get("name"),
        "log_level": raw.get("app", {}).get("log_level"),
        "data_dir": ROOT_DIR / raw.get("app", {}).get("data_dir", "data"),
        "use_mock_jobs": raw.get("app", {}).get("use_mock_jobs"),
        "use_llm": raw.get("app", {}).get("use_llm"),
        "llm_provider": raw.get("llm", {}).get("provider"),
        "llm_model": raw.get("llm", {}).get("model"),
        "llm_temperature": raw.get("llm", {}).get("temperature"),
        "llm_max_tokens": raw.get("llm", {}).get("max_tokens"),
        "default_location": raw.get("search", {}).get("default_location"),
        "results_limit": raw.get("search", {}).get("results_limit"),
        "top_matches": raw.get("search", {}).get("top_matches"),
        "country": raw.get("search", {}).get("country"),
        "min_score": raw.get("matching", {}).get("min_score"),
    }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    yaml_values = {key: value for key, value in _load_yaml().items() if value is not None}
    return Settings(**yaml_values)
