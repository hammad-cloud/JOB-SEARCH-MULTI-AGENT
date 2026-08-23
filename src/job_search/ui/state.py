"""Session-state helpers for cross-tab UI actions and fresh starts."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from job_search.models.schemas import JobPosting
from job_search.tools.tracker import TrackerStore

# Keys that should not stick around from a previous visit / search.
_STICKY_PREFIXES = (
    "job_search_",
    "job_results",
    "job_search_origin",
    "active_cv_fp",
    "design_company",
    "design_role",
    "design_job_url",
    "design_job_description",
    "design_pasted_resume",
    "design_prefill_notice",
    "edit_id",
    "form_",
)


def bootstrap_fresh_session(
    default_location: str = "Remote",
    *,
    data_dir: Path | None = None,
) -> None:
    """
    Start each browser connection clean.

    Reloading the page creates a new Streamlit session id — wipe Find jobs
    and Pipeline tracker data so nothing from the last visit comes back.
    """
    session_id = _current_session_id()
    previous_id = st.session_state.get("_streamlit_session_id")
    already_ready = st.session_state.get("_dashboard_bootstrapped_v4")
    if already_ready and previous_id == session_id:
        return

    _clear_sticky_keys()
    for key in (
        "_dashboard_bootstrapped",
        "_dashboard_bootstrapped_v2",
        "_dashboard_bootstrapped_v3",
    ):
        st.session_state.pop(key, None)

    st.session_state.job_search_keywords = "software engineer"
    st.session_state.job_search_location = default_location
    st.session_state.job_search_source = "LinkedIn"
    st.session_state.job_search_origin = "fresh"
    st.session_state.active_cv_fp = ""
    st.session_state.job_results = []
    st.session_state._streamlit_session_id = session_id
    st.session_state._dashboard_bootstrapped_v4 = True

    if data_dir is not None:
        clear_pipeline_tracker(data_dir)


def clear_pipeline_tracker(data_dir: Path) -> None:
    """Wipe saved applications so Pipeline opens at TOTAL 0."""
    folder = data_dir / "applications"
    folder.mkdir(parents=True, exist_ok=True)
    TrackerStore(path=folder / "tracker.json").save([])


def reset_job_search(
    *,
    keywords: str,
    location: str,
    source: str = "All sources",
) -> None:
    """Replace search fields and drop cached results (call before widgets)."""
    st.session_state.job_search_keywords = keywords
    st.session_state.job_search_location = location
    st.session_state.job_search_source = source
    st.session_state.job_results = []


def apply_cv_search(
    *,
    fingerprint: str,
    keywords: str,
    location: str,
    source: str = "All sources",
) -> bool:
    """
    If the uploaded CV changed, refresh search fields from that CV.
    Returns True when a CV-driven refresh happened.
    """
    previous = st.session_state.get("active_cv_fp", "")
    if fingerprint == previous:
        return False
    reset_job_search(keywords=keywords, location=location, source=source)
    st.session_state.active_cv_fp = fingerprint
    st.session_state.job_search_origin = "cv"
    return True


def clear_cv_search(default_location: str) -> bool:
    """When the CV is removed, clear results and return filters to defaults."""
    if not st.session_state.get("active_cv_fp"):
        return False
    reset_job_search(
        keywords="software engineer",
        location=default_location,
        source="LinkedIn",
    )
    st.session_state.active_cv_fp = ""
    st.session_state.job_search_origin = "fresh"
    return True


def prefill_design_resume(job: JobPosting) -> None:
    """Load a job listing into the Design resume tab fields."""
    st.session_state.design_company = job.company
    st.session_state.design_role = job.title
    st.session_state.design_job_description = job.description
    st.session_state.design_job_url = str(job.url) if job.url else ""
    st.session_state.design_prefill_notice = (
        f"Loaded **{job.title}** at **{job.company}**. "
        "Open the **Design resume** tab to continue."
    )


def consume_design_prefill_notice() -> str | None:
    return st.session_state.pop("design_prefill_notice", None)


def peek_design_prefill_notice() -> str | None:
    return st.session_state.get("design_prefill_notice")


def _current_session_id() -> str:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        if ctx and getattr(ctx, "session_id", None):
            return str(ctx.session_id)
    except Exception:
        pass
    return "unknown"


def _clear_sticky_keys() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("_"):
            continue
        if key.startswith(_STICKY_PREFIXES):
            del st.session_state[key]
