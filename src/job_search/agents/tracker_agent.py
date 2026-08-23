"""Persist pipeline outputs for later review."""

from __future__ import annotations

from pathlib import Path

from job_search.agents.base import BaseAgent
from job_search.models.schemas import PipelineResult
from job_search.tools.storage import Storage


class TrackerAgent(BaseAgent):
    name = "tracker"

    def __init__(self, storage: Storage | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage = storage or Storage(self.settings)

    def run(self, result: PipelineResult) -> Path:
        self.storage.save_jobs(result.jobs)
        for draft in result.drafts:
            self.storage.save_draft(draft)
        return self.storage.save_pipeline_result(result)
