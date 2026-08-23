from job_search.ui.services.cv_keywords import keywords_from_resume_text


def test_keywords_from_python_resume() -> None:
    resume = (
        "Alex Rivera\n"
        "Python Developer\n\n"
        "Skills: Python, Django, Flask, FastAPI\n"
        "Target titles: Backend Engineer, Python Developer\n"
    )
    keywords = keywords_from_resume_text(resume).lower()
    assert "python" in keywords or "backend" in keywords or "django" in keywords


def test_keywords_empty_falls_back() -> None:
    assert keywords_from_resume_text("") == "software engineer"
