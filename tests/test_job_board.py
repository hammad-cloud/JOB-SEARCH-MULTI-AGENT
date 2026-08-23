from job_search.models.schemas import JobBoardQuery
from job_search.tools.job_search import JobSearchTool


def test_job_board_search_defaults_to_linkedin() -> None:
    jobs = JobSearchTool().search(JobBoardQuery(keywords="software engineer", source="LinkedIn"))
    assert jobs
    assert all(job.source == "linkedin" for job in jobs)
    assert any("Software Engineer" in job.title for job in jobs)


def test_job_board_search_filters_by_keywords() -> None:
    jobs = JobSearchTool().search(
        JobBoardQuery(keywords="python", source="All sources", location="Remote")
    )
    assert jobs
    assert any("Python" in job.title or "python" in job.description.lower() for job in jobs)
