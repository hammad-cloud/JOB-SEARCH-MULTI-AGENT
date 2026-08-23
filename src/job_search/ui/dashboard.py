"""Pipeline dashboard entry point (backward compatible)."""

from job_search.ui.pages.pipeline import render_pipeline_page

render_pipeline_dashboard = render_pipeline_page

__all__ = ["render_pipeline_dashboard", "render_pipeline_page"]
