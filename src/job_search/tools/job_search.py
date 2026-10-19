"""Job listing source. Uses mock data until API credentials are set."""

from __future__ import annotations

import logging

import httpx

from job_search.config import Settings, get_settings
from job_search.models.schemas import JobBoardQuery, JobPosting, SearchPreferences
from job_search.tools.mock_jobs import MOCK_JOBS

ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"
logger = logging.getLogger(__name__)


class JobSearchTool:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def search(self, query: JobBoardQuery | SearchPreferences) -> list[JobPosting]:
        if isinstance(query, SearchPreferences):
            query = self._to_board_query(query)
        if self.uses_live_api:
            jobs = self._search_adzuna(query)
            if jobs:
                return jobs
        return self._filter_mock(query)

    @property
    def uses_live_api(self) -> bool:
        s = self.settings
        return not s.use_mock_jobs and bool(s.adzuna_app_id and s.adzuna_app_key)

    def _search_adzuna(self, query: JobBoardQuery) -> list[JobPosting]:
        """Live listings; returns [] on any failure so the caller falls back to mock data."""
        keywords = " ".join(item.strip() for item in query.keywords.split(",") if item.strip())
        params = {
            "app_id": self.settings.adzuna_app_id,
            "app_key": self.settings.adzuna_app_key,
            "results_per_page": min(query.results_limit, 50),
            "what_or": keywords,
        }
        location = query.location.strip()
        if location and location.lower() != "remote":
            params["where"] = location
        try:
            response = httpx.get(
                ADZUNA_URL.format(country=self.settings.country), params=params, timeout=15
            )
            response.raise_for_status()
            results = response.json().get("results", [])
        except (httpx.HTTPError, ValueError) as error:
            logger.warning("Adzuna search failed, using mock jobs: %s", error)
            return []
        jobs: list[JobPosting] = []
        for item in results:
            try:
                where = (item.get("location") or {}).get("display_name", "")
                description = item.get("description", "")
                jobs.append(
                    JobPosting(
                        id=f"adzuna-{item['id']}",
                        title=item.get("title", "Untitled role"),
                        company=(item.get("company") or {}).get("display_name", "Unknown company"),
                        location=where or "Unspecified",
                        description=description,
                        url=item.get("redirect_url") or None,
                        source="adzuna",
                        remote="remote" in f"{where} {description}".lower(),
                        posted_at=item.get("created"),
                    )
                )
            except (KeyError, ValueError) as error:
                logger.warning("Skipping malformed Adzuna result: %s", error)
        return jobs

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
