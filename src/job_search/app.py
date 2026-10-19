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
    initial_sidebar_state="expanded",
)
inject_dashboard_theme()
bootstrap_fresh_session(settings.default_location, data_dir=settings.data_dir)

# Only the selected page renders; re-assign form keys so Streamlit keeps them while hidden.
for _key in (
    "design_company", "design_role", "design_job_url", "design_job_description",
    "design_pasted_resume", "job_search_keywords", "job_search_location", "job_search_source",
):
    if _key in st.session_state:
        st.session_state[_key] = st.session_state[_key]

PAGES = {
    "Dashboard": ":material/space_dashboard: Dashboard",
    "Design resume": ":material/description: Design resume",
    "Find jobs": ":material/work: Find jobs",
}
with st.sidebar:
    st.markdown('<div class="brand">JobSearch.ai</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", list(PAGES), format_func=PAGES.get, label_visibility="collapsed")

resume_file = render_header()
store = TrackerStore(settings)

if page == "Dashboard":
    render_pipeline_page(store)
elif page == "Design resume":
    render_resume_page(settings, resume_file)
else:
    render_jobs_page(settings, resume_file)
