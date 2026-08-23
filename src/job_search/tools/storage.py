"""JSON persistence for jobs and application drafts."""

from __future__ import annotations

import json
from pathlib import Path

from job_search.config import Settings, get_settings
from job_search.models.schemas import ApplicationDraft, JobPosting, PipelineResult


class Storage:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.jobs_dir = self.settings.data_dir / "jobs"
        self.applications_dir = self.settings.data_dir / "applications"
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.applications_dir.mkdir(parents=True, exist_ok=True)

    def save_jobs(self, jobs: list[JobPosting], name: str = "latest") -> Path:
        path = self.jobs_dir / f"{name}.json"
        payload = [job.model_dump(mode="json") for job in jobs]
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def save_draft(self, draft: ApplicationDraft) -> Path:
        path = self.applications_dir / f"{draft.job_id}.json"
        path.write_text(draft.model_dump_json(indent=2), encoding="utf-8")
        return path

    def save_pipeline_result(self, result: PipelineResult, name: str = "latest") -> Path:
        path = self.applications_dir / f"{name}_pipeline.json"
        path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return path
