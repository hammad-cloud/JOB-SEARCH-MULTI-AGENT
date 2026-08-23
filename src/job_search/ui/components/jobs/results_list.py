"""Job search results list."""

from __future__ import annotations

import streamlit as st

from job_search.models.schemas import JobPosting
from job_search.ui.components.jobs.job_card import render_job_card


def render_job_results(jobs: list[JobPosting], *, has_searched: bool = False) -> None:
    if not has_searched:
        st.info("No search yet. Upload a CV or click **Search** to load jobs.")
        return

    count = len(jobs)
    label = "job" if count == 1 else "jobs"
    st.caption(f"{count} {label} found")

    if not jobs:
        st.info("No jobs matched your search. Try broader keywords or another source.")
        return

    for index, job in enumerate(jobs):
        render_job_card(job, index)
