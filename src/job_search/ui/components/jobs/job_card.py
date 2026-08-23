"""Single job listing card."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from job_search.models.schemas import JobPosting
from job_search.ui.state import prefill_design_resume


def _format_posted_date(posted_at: datetime | None) -> str:
    if not posted_at:
        return "Date unavailable"
    return posted_at.date().isoformat()


def render_job_card(job: JobPosting, index: int) -> None:
    with st.container(border=True):
        if job.url:
            st.markdown(f"[{job.title}]({job.url})")
        else:
            st.markdown(f"**{job.title}**")

        st.caption(f"{job.company} · {job.location} · {_format_posted_date(job.posted_at)}")

        _, action_col = st.columns([3, 1.2])
        with action_col:
            if st.button(
                "Design resume for this job",
                key=f"design-resume-{job.id}-{index}",
                use_container_width=True,
            ):
                prefill_design_resume(job)
                st.rerun()
