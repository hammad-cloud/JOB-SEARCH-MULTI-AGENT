"""Sample job board listings used when no live API is configured."""

from __future__ import annotations

from datetime import UTC, datetime

from job_search.models.schemas import JobPosting

MOCK_JOBS: list[JobPosting] = [
    JobPosting(
        id="job-001",
        title="Custom Software Engineer",
        company="Accenture",
        location="Ahmedabad, Gujarat, India",
        description=(
            "Design and deliver custom software solutions for enterprise clients. "
            "Strong experience with Python, cloud platforms, and agile delivery required."
        ),
        url="https://www.linkedin.com/jobs/view/custom-software-engineer-accenture",
        source="linkedin",
        remote=False,
        posted_at=datetime(2026, 8, 14, tzinfo=UTC),
    ),
    JobPosting(
        id="job-002",
        title="Software Engineer II",
        company="Microsoft",
        location="Remote",
        description=(
            "Build scalable services in Python and C#. Collaborate with product teams "
            "on backend APIs, observability, and deployment automation."
        ),
        url="https://www.linkedin.com/jobs/view/software-engineer-ii-microsoft",
        source="linkedin",
        remote=True,
        posted_at=datetime(2026, 8, 13, tzinfo=UTC),
    ),
    JobPosting(
        id="job-003",
        title="Backend Software Engineer",
        company="Stripe",
        location="Remote",
        description=(
            "Own payment platform services written in Python and Go. "
            "Experience with distributed systems, PostgreSQL, and API design."
        ),
        url="https://www.linkedin.com/jobs/view/backend-software-engineer-stripe",
        source="linkedin",
        remote=True,
        posted_at=datetime(2026, 8, 12, tzinfo=UTC),
    ),
    JobPosting(
        id="job-004",
        title="Python Software Engineer",
        company="Northwind Labs",
        location="Remote",
        description=(
            "Build APIs with Python, FastAPI, and PostgreSQL. "
            "LLM tooling and agent workflows experience is a plus."
        ),
        source="indeed",
        remote=True,
        posted_at=datetime(2026, 8, 11, tzinfo=UTC),
    ),
    JobPosting(
        id="job-005",
        title="Full Stack Software Engineer",
        company="Orbit Studio",
        location="Remote",
        description=(
            "Own Streamlit/React UIs and Python services that call LLMs. "
            "Pydantic, prompt design, and evaluation experience preferred."
        ),
        source="linkedin",
        remote=True,
        posted_at=datetime(2026, 8, 10, tzinfo=UTC),
    ),
    JobPosting(
        id="job-006",
        title="Software Engineer - AI Platform",
        company="Helios Analytics",
        location="New York, NY",
        description=(
            "Ship ranking and retrieval features for an AI platform. "
            "Python, scikit-learn, Pandas, and production ML experience required."
        ),
        source="glassdoor",
        remote=False,
        posted_at=datetime(2026, 8, 9, tzinfo=UTC),
    ),
    JobPosting(
        id="job-007",
        title="Django Software Engineer",
        company="Riverbend Software",
        location="Remote",
        description=(
            "Build and maintain Django web apps, REST APIs, and PostgreSQL models. "
            "Flask and front-end HTML, CSS, and JavaScript experience useful."
        ),
        source="indeed",
        remote=True,
        posted_at=datetime(2026, 8, 8, tzinfo=UTC),
    ),
    JobPosting(
        id="job-008",
        title="Junior Software Engineer",
        company="Summit Apps",
        location="Remote",
        description=(
            "Work on Flask and Django services, debug production issues, and "
            "write Python scripts for data processing with Pandas."
        ),
        source="linkedin",
        remote=True,
        posted_at=datetime(2026, 8, 7, tzinfo=UTC),
    ),
    JobPosting(
        id="job-009",
        title="Software Engineer - Platform",
        company="CloudNine Systems",
        location="Austin, TX",
        description=(
            "Improve internal developer platform tooling. Python, Kubernetes, "
            "Terraform, and CI/CD pipeline experience preferred."
        ),
        source="glassdoor",
        remote=False,
        posted_at=datetime(2026, 8, 6, tzinfo=UTC),
    ),
    JobPosting(
        id="job-010",
        title="Senior Software Engineer",
        company="DataForge",
        location="Remote",
        description=(
            "Lead backend architecture for data ingestion pipelines. "
            "Python, Kafka, Spark, and cloud-native design patterns."
        ),
        source="linkedin",
        remote=True,
        posted_at=datetime(2026, 8, 5, tzinfo=UTC),
    ),
]

JOB_SOURCES = ["LinkedIn", "Indeed", "Glassdoor", "All sources"]

SOURCE_ALIASES = {
    "linkedin": "LinkedIn",
    "indeed": "Indeed",
    "glassdoor": "Glassdoor",
}
