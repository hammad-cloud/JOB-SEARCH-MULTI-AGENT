"""Derive job-board search keywords from a CV."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

from job_search.agents.profile_agent import ProfileAgent
from job_search.models.schemas import Profile


def keywords_from_resume_text(resume_text: str) -> str:
    """Build a search query string from resume content."""
    text = resume_text.strip()
    if not text:
        return "software engineer"

    profile = _profile_from_text(text)
    parts: list[str] = []
    for title in profile.target_titles[:3]:
        cleaned = _clean_phrase(title)
        if cleaned:
            parts.append(cleaned)
    for skill in profile.skills[:5]:
        cleaned = _clean_phrase(skill)
        if cleaned and cleaned.lower() not in {item.lower() for item in parts}:
            parts.append(cleaned)

    if not parts:
        parts = _fallback_tokens(text)

    return ", ".join(parts[:6]) or "software engineer"


def _profile_from_text(text: str) -> Profile:
    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
        mode="w",
        encoding="utf-8",
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    try:
        return ProfileAgent().run(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)


def _clean_phrase(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip(" -•*|")
    if len(cleaned) < 2 or len(cleaned) > 60:
        return ""
    return cleaned


def _fallback_tokens(text: str) -> list[str]:
    known = [
        "python",
        "django",
        "flask",
        "fastapi",
        "javascript",
        "react",
        "software engineer",
        "backend",
        "frontend",
        "full stack",
        "machine learning",
        "data engineer",
    ]
    lower = text.lower()
    found = [token for token in known if token in lower]
    return found[:5] or ["software engineer"]
