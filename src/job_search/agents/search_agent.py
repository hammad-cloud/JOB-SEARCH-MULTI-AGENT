"""Find jobs from configured sources (mock or live API)."""

from __future__ import annotations

from job_search.agents.base import BaseAgent
from job_search.models.schemas import JobPosting, Profile, SearchPreferences
from job_search.tools.job_search import JobSearchTool


class SearchAgent(BaseAgent):
    name = "search"

    def __init__(self, job_search: JobSearchTool | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.job_search = job_search or JobSearchTool(self.settings)

    def run(
        self,
        profile: Profile,
        preferences: SearchPreferences | None = None,
    ) -> list[JobPosting]:
        prefs = preferences or SearchPreferences(
            location=self.settings.default_location,
            results_limit=self.settings.results_limit,
        )
        merged = list(prefs.keywords)
        for extra in [*profile.target_titles, *profile.skills[:8]]:
            if extra and extra.lower() not in {item.lower() for item in merged}:
                merged.append(extra)
        prefs.keywords = merged
        return self.job_search.search(prefs)
