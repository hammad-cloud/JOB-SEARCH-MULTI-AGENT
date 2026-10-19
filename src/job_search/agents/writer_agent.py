"""Draft cover letters and resume bullets for top matches."""

from __future__ import annotations

import json

from job_search.agents.base import BaseAgent
from job_search.models.schemas import ApplicationDraft, MatchResult, Profile


class WriterAgent(BaseAgent):
    name = "writer"

    def run(self, profile: Profile, matches: list[MatchResult]) -> list[ApplicationDraft]:
        drafts: list[ApplicationDraft] = []
        for match in matches[: self.settings.top_matches]:
            if not match.job:
                continue
            drafts.append(self._draft(profile, match))
        return drafts

    def _draft(self, profile: Profile, match: MatchResult) -> ApplicationDraft:
        if self.settings.use_llm and self.llm.is_configured:
            drafted = self._draft_with_llm(profile, match)
            if drafted:
                return drafted
        return self._draft_template(profile, match)

    def _draft_with_llm(self, profile: Profile, match: MatchResult) -> ApplicationDraft | None:
        job = match.job
        assert job is not None
        system_prompt = self.load_prompt("cover_letter.md") or "Write a short cover letter."
        user_prompt = json.dumps(
            {
                "profile": profile.model_dump(mode="json"),
                "job": job.model_dump(mode="json"),
                "match": {"score": match.score, "reasons": match.reasons},
            }
        )
        raw = self.llm.complete(system_prompt, user_prompt)
        try:
            payload = json.loads(raw)
            return ApplicationDraft(
                job_id=job.id,
                cover_letter=str(payload["cover_letter"]).strip(),
                resume_bullets=[str(item) for item in payload.get("resume_bullets", [])],
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return None

    def _draft_template(self, profile: Profile, match: MatchResult) -> ApplicationDraft:
        job = match.job
        assert job is not None
        skills = ", ".join(profile.skills[:5]) or "relevant experience"
        cover_letter = (
            f"Dear {job.company} hiring team,\n\n"
            f"I am applying for the {job.title} role. "
            f"My background includes {skills}, which maps to this position "
            f"(match score {match.score}/100).\n\n"
            f"Thank you for your consideration,\n{profile.name}\n"
        )
        bullets = [
            f"Delivered work aligned with {job.title} responsibilities",
            *[f"Applied {skill} in production settings" for skill in profile.skills[:3]],
        ]
        return ApplicationDraft(
            job_id=job.id,
            cover_letter=cover_letter,
            resume_bullets=bullets,
        )
