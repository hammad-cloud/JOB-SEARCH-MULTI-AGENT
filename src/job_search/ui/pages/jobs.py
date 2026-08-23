"""Find jobs tab — search from CV upload or manual filters."""

from __future__ import annotations

import streamlit as st

from job_search.config import Settings
from job_search.models.schemas import JobBoardQuery
from job_search.tools.job_search import JobSearchTool
from job_search.ui.components.jobs.results_list import render_job_results
from job_search.ui.components.jobs.search_form import render_job_search_form
from job_search.ui.services.cv_keywords import keywords_from_resume_text
from job_search.ui.services.resume_io import load_uploaded_resume_text, resume_fingerprint
from job_search.ui.state import apply_cv_search, clear_cv_search, peek_design_prefill_notice


def render_jobs_page(settings: Settings, resume_file) -> None:
    notice = peek_design_prefill_notice()
    if notice:
        st.success(notice)

    refreshed_from_cv = _sync_search_with_cv(settings, resume_file)
    keywords, location, source, submitted = render_job_search_form(settings.default_location)

    # Only search when the user asks (Search) or a new CV is uploaded — never on reload.
    if submitted or refreshed_from_cv:
        query = JobBoardQuery(
            keywords=keywords,
            location=location,
            source=source,
            results_limit=settings.results_limit,
        )
        st.session_state.job_results = JobSearchTool(settings).search(query)
        st.session_state.job_search_origin = "cv" if refreshed_from_cv else "manual"
    elif st.session_state.get("job_search_origin", "fresh") == "fresh":
        # Reload / first open: never show leftover "N jobs found".
        st.session_state.job_results = []

    results = st.session_state.get("job_results", [])
    origin = st.session_state.get("job_search_origin", "fresh")

    if origin == "cv" and resume_file and results:
        st.caption(
            f"Results matched to your CV (**{resume_file.name}**). "
            "Adjust filters and click Search to refine."
        )
    elif origin == "fresh" or not results:
        st.caption("Upload a CV above or click Search to find jobs.")
    elif not resume_file:
        st.caption("Upload a CV above to match jobs to your profile.")

    render_job_results(results, has_searched=origin in {"cv", "manual"})


def _sync_search_with_cv(settings: Settings, resume_file) -> bool:
    """Update keywords/results when a CV is uploaded or changed."""
    if not resume_file:
        clear_cv_search(settings.default_location)
        return False

    fingerprint = resume_fingerprint(resume_file)
    if fingerprint == st.session_state.get("active_cv_fp"):
        return False

    try:
        resume_text = load_uploaded_resume_text(resume_file)
        keywords = keywords_from_resume_text(resume_text)
    except Exception as exc:
        st.warning(f"Could not read CV for job search: {exc}")
        return False

    return apply_cv_search(
        fingerprint=fingerprint,
        keywords=keywords,
        location=settings.default_location,
        source="All sources",
    )
