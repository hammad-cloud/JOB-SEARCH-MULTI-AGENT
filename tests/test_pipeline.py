from pathlib import Path

from job_search.agents.match_agent import MatchAgent
from job_search.agents.profile_agent import ProfileAgent
from job_search.models.schemas import JobPosting, SearchPreferences
from job_search.orchestrator.pipeline import JobSearchPipeline
from job_search.tools.job_search import JobSearchTool
from job_search.tools.resume_parser import ResumeParser

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_RESUME = ROOT / "data" / "resumes" / "sample.txt"


def test_resume_parser_reads_sample() -> None:
    text = ResumeParser().parse(SAMPLE_RESUME)
    assert "Python" in text


def test_resume_parser_reads_pdf(monkeypatch, tmp_path) -> None:
    pdf_path = tmp_path / "resume.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%mock\n")

    class FakePage:
        def extract_text(self) -> str:
            return "Jane Doe\nPython Developer\nSkills: Python, Django"

    class FakeReader:
        def __init__(self, path: str) -> None:
            self.pages = [FakePage()]

    monkeypatch.setattr("job_search.tools.resume_parser.PdfReader", FakeReader)
    text = ResumeParser().parse(pdf_path)
    assert "Jane Doe" in text
    assert "Django" in text


def test_profile_agent_heuristic() -> None:
    profile = ProfileAgent().run(SAMPLE_RESUME)
    assert profile.name == "Alex Rivera"
    assert "Python" in profile.skills


def test_match_agent_ranks_python_jobs() -> None:
    profile = ProfileAgent().run(SAMPLE_RESUME)
    jobs = JobSearchTool().search(SearchPreferences(keywords=["python"]))
    matches = MatchAgent().run(profile, jobs)
    assert matches
    assert matches[0].score >= matches[-1].score
    assert all(item.job is None or isinstance(item.job, JobPosting) for item in matches)


def test_profile_agent_parses_bullet_skills() -> None:
    resume = ROOT / "data" / "resumes" / "jestina-mangol-resume.txt"
    profile = ProfileAgent().run(resume)
    assert profile.name == "Jestina Mangol"
    assert "Django" in profile.skills
    assert "Flask" in profile.skills
    assert any("Python Developer" in title for title in profile.target_titles)


def test_pipeline_ranks_related_jobs(tmp_path, monkeypatch) -> None:
    from job_search.config import get_settings

    settings = get_settings()
    monkeypatch.setattr(settings, "data_dir", tmp_path)
    resume = ROOT / "data" / "resumes" / "jestina-mangol-resume.txt"
    result = JobSearchPipeline(settings).run(
        resume,
        SearchPreferences(keywords=["python", "django"], remote_only=True),
    )
    assert result.matches
    titles = [match.job.title for match in result.matches if match.job]
    assert any("Django" in title or "Python" in title for title in titles)


def test_pipeline_writes_output(tmp_path, monkeypatch) -> None:
    from job_search.config import get_settings

    settings = get_settings()
    monkeypatch.setattr(settings, "data_dir", tmp_path)
    result = JobSearchPipeline(settings).run(SAMPLE_RESUME)
    assert result.profile.name
    assert result.jobs
    assert (tmp_path / "applications" / "latest_pipeline.json").exists()
