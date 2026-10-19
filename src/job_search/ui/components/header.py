"""Dashboard header (greeting + date) and sidebar CV upload."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from job_search.ui.services.resume_io import load_uploaded_resume_text


def _greeting(hour: int) -> str:
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def render_header() -> object | None:
    """Render greeting row and sidebar CV uploader. Returns the uploaded file, if any."""
    now = datetime.now()
    st.markdown(
        f"""
        <div class="date-chip">{now.strftime("%b %d, %Y")} &#128197;</div>
        <p class="dash-greeting">{_greeting(now.hour)}</p>
        <p class="dash-sub">Here is your job search report and application tracker.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown('<div class="side-section">YOUR CV</div>', unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Upload CV",
            type=["txt", "md", "pdf"],
            label_visibility="collapsed",
        )
        if resume_file:
            try:
                char_count = len(load_uploaded_resume_text(resume_file).strip())
            except Exception:
                char_count = len(resume_file.getvalue())
            st.caption(f"Using {resume_file.name} ({char_count} characters)")
        else:
            st.caption("No CV uploaded yet · PDF, TXT, or MD")
    return resume_file
