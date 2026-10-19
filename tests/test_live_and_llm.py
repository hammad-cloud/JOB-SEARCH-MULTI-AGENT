import httpx

from job_search.agents.research_agent import ResearchAgent
from job_search.agents.writer_agent import WriterAgent
from job_search.config import get_settings
from job_search.models.schemas import JobBoardQuery, JobPosting, MatchResult, Profile
from job_search.tools.job_search import JobSearchTool

JOB = JobPosting(id="j1", title="Backend Engineer", company="Acme", location="Remote",
                 description="Python APIs")
MATCH = MatchResult(job_id="j1", score=80, reasons=["Matched skill: python"], job=JOB)
PROFILE = Profile(name="Alex", skills=["Python"])


class FakeLLM:
    is_configured = True

    def __init__(self, reply: str) -> None:
        self.reply = reply

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return self.reply


def _live_settings(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "use_mock_jobs", False)
    monkeypatch.setattr(settings, "adzuna_app_id", "id")
    monkeypatch.setattr(settings, "adzuna_app_key", "key")
    return settings


def test_adzuna_results_are_mapped(monkeypatch) -> None:
    settings = _live_settings(monkeypatch)
    payload = {"results": [{
        "id": "42", "title": "Python Dev", "company": {"display_name": "Acme"},
        "location": None, "description": "Remote Python role",
        "redirect_url": "https://example.com/j/42", "created": "2026-10-01T00:00:00Z",
    }]}
    monkeypatch.setattr(httpx, "get", lambda *a, **k: httpx.Response(
        200, json=payload, request=httpx.Request("GET", "https://x")))
    jobs = JobSearchTool(settings).search(JobBoardQuery(keywords="python"))
    assert [(j.id, j.company, j.location, j.remote) for j in jobs] == [
        ("adzuna-42", "Acme", "Unspecified", True)
    ]


def test_adzuna_failure_falls_back_to_mock(monkeypatch) -> None:
    settings = _live_settings(monkeypatch)

    def boom(*args, **kwargs):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(httpx, "get", boom)
    jobs = JobSearchTool(settings).search(JobBoardQuery(keywords="python", source="All sources"))
    assert jobs and all(job.source != "adzuna" for job in jobs)


def test_writer_uses_llm_json(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "use_llm", True)
    reply = '{"cover_letter": "Hi Acme", "resume_bullets": ["Built APIs"]}'
    draft = WriterAgent(settings=settings, llm=FakeLLM(reply)).run(PROFILE, [MATCH])[0]
    assert (draft.cover_letter, draft.resume_bullets) == ("Hi Acme", ["Built APIs"])


def test_writer_and_research_fall_back_on_bad_llm_reply(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "use_llm", True)
    draft = WriterAgent(settings=settings, llm=FakeLLM("not json")).run(PROFILE, [MATCH])[0]
    assert draft.cover_letter.startswith("Dear Acme hiring team")
    brief = ResearchAgent(settings=settings, llm=FakeLLM("")).run(PROFILE, [MATCH])[0]
    assert brief.summary.startswith("Acme is hiring")
