"""Design resume tab — tailor an existing CV toward a specific job posting."""

from __future__ import annotations

import streamlit as st

from job_search.agents.resume_design_agent import ResumeDesignAgent
from job_search.config import Settings
from job_search.ui.services.resume_io import load_uploaded_resume_text
from job_search.ui.state import consume_design_prefill_notice


def render_resume_page(settings: Settings, resume_file) -> None:
    notice = consume_design_prefill_notice()
    if notice:
        st.info(notice)

    with st.container(border=True):
        st.markdown("## Design resume for a required job")
        st.caption(
            "Upload your CV above, then paste the job posting. "
            "The dashboard reorders your real experience toward that role "
            "and does not invent jobs."
        )

        company = st.text_input("Company", key="design_company")
        role = st.text_input("Role", key="design_role")
        job_url = st.text_input("Job URL (optional)", key="design_job_url")
        job_description = st.text_area(
            "Job description",
            height=180,
            placeholder="Paste the full job posting",
            key="design_job_description",
        )
        pasted_resume = st.text_area(
            "Paste resume text (optional if you already uploaded a file)",
            height=160,
            placeholder="Leave blank to use the uploaded CV",
            key="design_pasted_resume",
        )

        submitted = st.button("Design resume", type="primary")

    if not submitted:
        return

    resume_text = pasted_resume.strip()
    if not resume_text:
        try:
            resume_text = load_uploaded_resume_text(resume_file)
        except Exception as exc:
            st.error(f"Could not read uploaded CV: {exc}")
            return

    if not resume_text:
        st.warning("Upload a CV above or paste resume text.")
        return
    if not company.strip() or not role.strip():
        st.warning("Company and role are required.")
        return
    if not job_description.strip():
        st.warning("Paste the full job posting in Job description.")
        return

    try:
        result = ResumeDesignAgent(settings=settings).run(
            resume_text,
            company=company,
            role=role,
            job_description=job_description,
            job_url=job_url,
        )
    except ValueError as exc:
        st.warning(str(exc))
        return

    _save_draft(settings, result.company, result.role, result.tailored_resume)

    st.success(f"Resume tailored for {result.role} at {result.company}.")
    if result.job_url:
        st.caption(f"Job URL: {result.job_url}")

    if result.focus_skills:
        st.markdown("**Focus skills**")
        st.write(", ".join(result.focus_skills))

    if result.highlighted_bullets:
        st.markdown("**Highlighted experience**")
        for bullet in result.highlighted_bullets:
            st.markdown(f"- {bullet}")

    st.markdown("**Tailored resume**")
    st.text_area(
        "Tailored resume output",
        value=result.tailored_resume,
        height=360,
        label_visibility="collapsed",
    )
    st.download_button(
        "Download tailored resume",
        data=result.tailored_resume,
        file_name=f"{result.company}-{result.role}-resume.txt".replace(" ", "-").lower(),
        mime="text/plain",
    )


def _save_draft(settings: Settings, company: str, role: str, text: str) -> None:
    folder = settings.data_dir / "resumes" / "designed"
    folder.mkdir(parents=True, exist_ok=True)
    safe = f"{company}-{role}".replace(" ", "-").lower()
    safe = "".join(char for char in safe if char.isalnum() or char in "-_") or "resume"
    path = folder / f"{safe}.txt"
    path.write_text(text, encoding="utf-8")
