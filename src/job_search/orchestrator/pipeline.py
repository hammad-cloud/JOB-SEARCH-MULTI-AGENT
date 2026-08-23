"""Run agents in a fixed pipeline: profile → search → match → research → writer → tracker."""

from __future__ import annotations

from pathlib import Path

from job_search.agents.match_agent import MatchAgent
from job_search.agents.profile_agent import ProfileAgent
from job_search.agents.research_agent import ResearchAgent
from job_search.agents.search_agent import SearchAgent
from job_search.agents.tracker_agent import TrackerAgent
from job_search.agents.writer_agent import WriterAgent
from job_search.config import Settings, get_settings
from job_search.models.schemas import PipelineResult, SearchPreferences


class JobSearchPipeline:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.profile_agent = ProfileAgent(settings=self.settings)
        self.search_agent = SearchAgent(settings=self.settings)
        self.match_agent = MatchAgent(settings=self.settings)
        self.research_agent = ResearchAgent(settings=self.settings)
        self.writer_agent = WriterAgent(settings=self.settings)
        self.tracker_agent = TrackerAgent(settings=self.settings)

    def run(
        self,
        resume_path: str | Path,
        preferences: SearchPreferences | None = None,
    ) -> PipelineResult:
        profile = self.profile_agent.run(resume_path)
        jobs = self.search_agent.run(profile, preferences)
        matches = self.match_agent.run(profile, jobs)
        qualified = [item for item in matches if item.score >= self.settings.min_score]
        selected = qualified or matches[: self.settings.top_matches]
        briefs = self.research_agent.run(profile, selected)
        drafts = self.writer_agent.run(profile, selected)
        result = PipelineResult(
            profile=profile,
            jobs=jobs,
            matches=matches,
            briefs=briefs,
            drafts=drafts,
        )
        self.tracker_agent.run(result)
        return result
