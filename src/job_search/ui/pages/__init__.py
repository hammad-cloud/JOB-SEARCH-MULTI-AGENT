"""Dashboard pages."""

from job_search.ui.pages.jobs import render_jobs_page
from job_search.ui.pages.pipeline import render_pipeline_page
from job_search.ui.pages.resume import render_resume_page

__all__ = ["render_jobs_page", "render_pipeline_page", "render_resume_page"]
