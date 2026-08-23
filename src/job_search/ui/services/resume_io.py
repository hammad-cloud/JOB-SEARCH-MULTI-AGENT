"""Load resume text from Streamlit uploads or pasted content."""

from __future__ import annotations

import tempfile
from pathlib import Path

from job_search.tools.resume_parser import ResumeParser


def load_uploaded_resume_text(uploaded_file) -> str:
    """Parse an uploaded CV file into plain text."""
    if not uploaded_file:
        return ""
    suffix = Path(uploaded_file.name).suffix.lower() or ".txt"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = Path(tmp.name)
    try:
        return ResumeParser().parse(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)


def resume_fingerprint(uploaded_file) -> str:
    """Stable id for the currently uploaded CV (name + size)."""
    if not uploaded_file:
        return ""
    size = getattr(uploaded_file, "size", None)
    if size is None:
        size = len(uploaded_file.getvalue())
    return f"{uploaded_file.name}:{size}"
