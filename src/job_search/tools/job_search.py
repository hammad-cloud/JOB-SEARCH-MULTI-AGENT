"""Job listing source. Uses mock data until API credentials are set."""

from __future__ import annotations

from job_search.config import Settings, get_settings
from job_search.models.schemas import JobBoardQuery, JobPosting, SearchPreferences
from job_search.tools.mock_jobs import MOCK_JOBS


class JobSearchTool:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def search(self, query: JobBoardQuery | SearchPreferences) -> list[JobPosting]:
        if isinstance(query, SearchPreferences):
            query = self._to_board_query(query)
        return self._filter_mock(query)

    def _to_board_query(self, preferences: SearchPreferences) -> JobBoardQuery:
        return JobBoardQuery(
            keywords=", ".join(preferences.keywords),
            location=preferences.location,
            source="All sources",
            results_limit=preferences.results_limit,
            remote_friendly=preferences.remote_only,
        )

    def _filter_mock(self, query: JobBoardQuery) -> list[JobPosting]:
        keywords = [item.lower().strip() for item in query.keywords.split(",") if item.strip()]
        if not keywords:
            keywords = [item.lower().strip() for item in query.keywords.split() if item.strip()]

        pool = list(MOCK_JOBS)
        if query.source.lower() != "all sources":
            source_key = query.source.lower()
            pool = [job for job in pool if job.source.lower() == source_key]

        location = query.location.strip().lower()
        if location and location != "remote":
            pool = [
                job
                for job in pool
                if location in job.location.lower() or (query.remote_friendly and job.remote)
            ]
        elif location == "remote":
            pool = [job for job in pool if job.remote or "remote" in job.location.lower()]

        if not keywords:
            return pool[: query.results_limit]

        ranked: list[tuple[int, JobPosting]] = []
        for job in pool:
            blob = f"{job.title} {job.description} {job.company} {job.location}".lower()
            hits = sum(1 for keyword in keywords if keyword in blob)
            if hits:
                ranked.append((hits, job))
        ranked.sort(key=lambda item: item[0], reverse=True)
        jobs = [job for _, job in ranked[: query.results_limit]]
        return jobs or pool[: query.results_limit]
