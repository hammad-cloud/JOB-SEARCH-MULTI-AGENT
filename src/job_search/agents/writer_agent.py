"""Draft cover letters and resume bullets for top matches."""

from __future__ import annotations

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
