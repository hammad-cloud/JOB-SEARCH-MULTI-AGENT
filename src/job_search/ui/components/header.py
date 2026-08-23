"""Dashboard header with title and CV upload."""

from __future__ import annotations

from datetime import date

import streamlit as st

from job_search.ui.services.resume_io import load_uploaded_resume_text


def render_header() -> object | None:
    """Render title row and CV uploader. Returns the uploaded file, if any."""
    top_left, top_right = st.columns([2, 1])
    with top_left:
        st.title("Job Search Dashboard")
        st.caption(f"Generated: {date.today().isoformat()}")
    with top_right:
        resume_file = st.file_uploader(
            "Upload CV",
            type=["txt", "md", "pdf"],
            label_visibility="visible",
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
