"""Score jobs against the candidate profile."""

from __future__ import annotations

from job_search.agents.base import BaseAgent
from job_search.models.schemas import JobPosting, MatchResult, Profile


class MatchAgent(BaseAgent):
    name = "match"

    def run(self, profile: Profile, jobs: list[JobPosting]) -> list[MatchResult]:
        matches = [self._score(profile, job) for job in jobs]
        matches.sort(key=lambda item: item.score, reverse=True)
        return matches

    def _score(self, profile: Profile, job: JobPosting) -> MatchResult:
        haystack = f"{job.title} {job.description}".lower()
        skills = [self._clean(skill) for skill in profile.skills if self._clean(skill)]
        if any("python" in self._clean(title) for title in profile.target_titles):
            if "python" not in skills:
                skills = ["python", *skills]
        hits = [skill for skill in skills if skill in haystack]
        missing = [skill for skill in skills if skill not in hits]
        title_bonus = self._title_bonus(profile, job)
        token_hit = title_bonus > 0 or any(
            token in haystack for token in self._title_tokens(profile)
        )
        base = int((len(hits) / max(len(skills), 1)) * 80) if skills else 20
        score = min(100, max(base + title_bonus, 15 if token_hit else 5))
        reasons = [f"Matched skill: {skill}" for skill in hits[:5]]
        if title_bonus >= 20:
            reasons.append("Title aligns with a target role")
        elif title_bonus or token_hit:
            reasons.append("Role keywords overlap with your background")
        return MatchResult(
            job_id=job.id,
            score=score,
            reasons=reasons or ["Limited keyword overlap; review manually"],
            missing_skills=missing[:8],
            job=job,
        )

    def _title_bonus(self, profile: Profile, job: JobPosting) -> int:
        job_title = job.title.lower()
        job_words = set(job_title.split())
        best = 0
        for title in profile.target_titles:
            cleaned = self._clean(title)
            if not cleaned:
                continue
            if cleaned in job_title or job_title in cleaned:
                best = max(best, 25)
                continue
            overlap = job_words & (set(cleaned.split()) - {"at", "and", "the", "with", "for"})
            if len(overlap) >= 2:
                best = max(best, 20)
            elif "python" in overlap or "django" in overlap or "flask" in overlap:
                best = max(best, 10)
        return best

    def _clean(self, value: str) -> str:
        return value.lower().lstrip("-*• ").strip()

    def _title_tokens(self, profile: Profile) -> set[str]:
        stop = {"at", "and", "the", "with", "for", "senior", "junior", "lead"}
        tokens: set[str] = set()
        for title in profile.target_titles:
            for part in self._clean(title).split():
                if len(part) > 2 and part not in stop:
                    tokens.add(part)
        return tokens
