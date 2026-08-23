"""Short company/role brief for top matches."""

from __future__ import annotations

from job_search.agents.base import BaseAgent
from job_search.models.schemas import CompanyBrief, MatchResult, Profile


class ResearchAgent(BaseAgent):
    name = "research"

    def run(self, profile: Profile, matches: list[MatchResult]) -> list[CompanyBrief]:
        top = matches[: self.settings.top_matches]
        return [self._brief(profile, match) for match in top if match.job]

    def _brief(self, profile: Profile, match: MatchResult) -> CompanyBrief:
        job = match.job
        assert job is not None
        summary = (
            f"{job.company} is hiring a {job.title} ({job.location}). "
            f"Fit score {match.score}/100 for {profile.name}."
        )
        notes = match.reasons[:3]
        if match.missing_skills:
            notes.append("Gaps: " + ", ".join(match.missing_skills[:4]))
        return CompanyBrief(
            job_id=job.id,
            company=job.company,
            summary=summary,
            notes=notes,
        )
