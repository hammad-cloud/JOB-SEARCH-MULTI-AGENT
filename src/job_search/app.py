"""Streamlit UI for the job search pipeline and application tracker."""

from __future__ import annotations

import sys

import streamlit as st


def _reload_job_search() -> None:
    """Pick up agent/tool edits without restarting Streamlit."""
    for name in list(sys.modules):
        if name == "job_search" or name.startswith("job_search."):
            del sys.modules[name]


_reload_job_search()

from job_search.config import get_settings  # noqa: E402
from job_search.tools.tracker import TrackerStore  # noqa: E402
from job_search.ui.components.header import render_header  # noqa: E402
from job_search.ui.pages.jobs import render_jobs_page  # noqa: E402
from job_search.ui.pages.pipeline import render_pipeline_page  # noqa: E402
from job_search.ui.pages.resume import render_resume_page  # noqa: E402
from job_search.ui.state import bootstrap_fresh_session  # noqa: E402
from job_search.ui.theme import inject_dashboard_theme  # noqa: E402

settings = get_settings()
st.set_page_config(
    page_title="Job Search Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_dashboard_theme()
bootstrap_fresh_session(settings.default_location, data_dir=settings.data_dir)

resume_file = render_header()

pipeline_tab, resume_tab, jobs_tab = st.tabs(["Pipeline", "Design resume", "Find jobs"])
store = TrackerStore(settings)

with pipeline_tab:
    render_pipeline_page(store)

with resume_tab:
    render_resume_page(settings, resume_file)

with jobs_tab:
    render_jobs_page(settings, resume_file)
