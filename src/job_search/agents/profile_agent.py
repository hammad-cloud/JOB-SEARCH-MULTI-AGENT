"""Turn resume text into a structured candidate profile."""

from __future__ import annotations

import json
import re
from pathlib import Path

from job_search.agents.base import BaseAgent
from job_search.models.schemas import Profile
from job_search.tools.resume_parser import ResumeParser

SECTION_HEADINGS = {
    "skills",
    "education",
    "employment history",
    "experience",
    "work experience",
    "certificates",
    "certifications",
    "contact information",
    "relevant coursework",
    "memberships",
    "projects",
    "summary",
    "target titles",
    "titles",
}


class ProfileAgent(BaseAgent):
    name = "profile"

    def __init__(self, parser: ResumeParser | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.parser = parser or ResumeParser()

    def run(self, resume_path: str | Path) -> Profile:
        text = self.parser.parse(resume_path)
        if self.settings.use_llm and self.llm.is_configured:
            extracted = self._extract_with_llm(text)
            if extracted:
                extracted.source_resume = str(resume_path)
                return extracted
        return self._extract_heuristic(text, str(resume_path))

    def _extract_with_llm(self, text: str) -> Profile | None:
        system_prompt = self.load_prompt("profile.md") or "Extract a JSON profile from the resume."
        raw = self.llm.complete(system_prompt, text)
        try:
            payload = json.loads(raw)
            return Profile.model_validate(payload)
        except (json.JSONDecodeError, ValueError):
            return None

    def _extract_heuristic(self, text: str, source: str) -> Profile:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        name = lines[0] if lines else "Candidate"
        headline = lines[1] if len(lines) > 1 else ""
        skills = self._section_items(text, "skills")
        titles = self._section_items(text, "target titles") or self._section_items(text, "titles")
        if headline and headline.lower() not in {"skills", "education"}:
            titles = [headline, *titles]
        titles.extend(self._job_titles(text))
        titles = list(dict.fromkeys(titles))
        return Profile(
            name=name,
            summary=" ".join(lines[1:4]),
            skills=skills,
            target_titles=titles,
            source_resume=source,
        )

    def _section_items(self, text: str, heading: str) -> list[str]:
        items: list[str] = []
        capturing = False
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                if capturing:
                    continue
                continue
            key = line.lower().rstrip(":")
            if key == heading or line.lower().startswith(f"{heading}:"):
                capturing = True
                inline = line.split(":", 1)
                if len(inline) == 2 and inline[1].strip():
                    items.extend(self._split_items(inline[1]))
                continue
            if capturing and self._is_heading(line):
                break
            if capturing:
                items.extend(self._split_items(line))
        return list(dict.fromkeys(item for item in items if item))

    def _is_heading(self, line: str) -> bool:
        key = line.lower().rstrip(":")
        if key in SECTION_HEADINGS:
            return True
        return (
            line.endswith(":")
            and len(line) < 40
            and not line.startswith(("-", "*", "•"))
        )

    def _split_items(self, line: str) -> list[str]:
        cleaned = re.sub(r"^[-*•]\s*", "", line).strip()
        if not cleaned:
            return []
        if "," in cleaned or "|" in cleaned:
            return [part.strip() for part in re.split(r"[,|/]", cleaned) if part.strip()]
        return [cleaned]

    def _job_titles(self, text: str) -> list[str]:
        titles: list[str] = []
        for match in re.finditer(r"^(.+?)\s+at\s+.+$", text, flags=re.IGNORECASE | re.MULTILINE):
            title = match.group(1).strip(" -•*")
            if 2 < len(title) < 60:
                titles.append(title)
        return titles
