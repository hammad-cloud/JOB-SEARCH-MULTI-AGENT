from job_search.agents.resume_design_agent import ResumeDesignAgent


def test_resume_design_reorders_without_inventing() -> None:
    resume = (
        "Alex Rivera\n\n"
        "Skills: Python, FastAPI, Excel, Word\n\n"
        "Built Excel reports for finance teams.\n\n"
        "Built FastAPI services and Python data pipelines for production APIs.\n"
    )
    job = "Looking for a Python FastAPI engineer to build APIs and data pipelines."
    result = ResumeDesignAgent().run(
        resume,
        company="Acme",
        role="Python Developer",
        job_description=job,
    )
    assert "Alex Rivera" in result.tailored_resume
    assert "Excel reports" in result.tailored_resume
    assert "invent" not in result.tailored_resume.lower()
    assert "Python" in result.focus_skills or "FastAPI" in result.focus_skills
    # Relevant API work should appear before less relevant Excel work.
    assert result.tailored_resume.index("FastAPI") < result.tailored_resume.index("Excel reports")
