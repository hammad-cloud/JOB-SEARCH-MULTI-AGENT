"""Job board search form."""

from __future__ import annotations

import streamlit as st

from job_search.tools.mock_jobs import JOB_SOURCES


def render_job_search_form(default_location: str) -> tuple[str, str, str, bool]:
    """Render search fields. Returns keywords, location, source, and submitted flag."""
    st.session_state.setdefault("job_search_keywords", "software engineer")
    st.session_state.setdefault("job_search_location", default_location)
    st.session_state.setdefault("job_search_source", "LinkedIn")

    with st.container(border=True):
        keyword_col, location_col, source_col, action_col = st.columns([2.2, 1.4, 1.2, 0.9])
        with keyword_col:
            keywords = st.text_input("Role or keywords", key="job_search_keywords")
        with location_col:
            location = st.text_input("Location", key="job_search_location")
        with source_col:
            source = st.selectbox("Source", JOB_SOURCES, key="job_search_source")
        with action_col:
            st.write("")
            st.write("")
            submitted = st.button("Search", type="primary", use_container_width=True)
    return keywords, location, source, submitted
