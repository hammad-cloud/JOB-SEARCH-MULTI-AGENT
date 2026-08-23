"""Demo tracker data matching the dashboard screenshot."""

from __future__ import annotations

from job_search.models.schemas import TrackedApplication, TrackerChannel, TrackerStatus
from job_search.tools.tracker import TrackerStore

DEMO_APPLICATIONS = [
    TrackedApplication(
        id="demo-001",
        date="2026-08-18",
        company="Nova AI",
        role="AI ML Engineer",
        sector="AI ML enginner",
        status=TrackerStatus.ACTIVE,
        channel=TrackerChannel.ONLINE,
    ),
    TrackedApplication(
        id="demo-002",
        date="2026-08-18",
        company="FinServe",
        role="Backend Developer",
        sector="Bank End Developer",
        status=TrackerStatus.INTERVIEW,
        channel=TrackerChannel.ONLINE,
    ),
    TrackedApplication(
        id="demo-003",
        date="2026-08-18",
        company="Pixel Labs",
        role="Frontend Developer",
        sector="Front End Developer",
        status=TrackerStatus.OFFER,
        channel=TrackerChannel.ONLINE,
    ),
    TrackedApplication(
        id="demo-004",
        date="2026-08-18",
        company="StackWorks",
        role="Full Stack Developer",
        sector="Full stack developers",
        status=TrackerStatus.HIRED,
        channel=TrackerChannel.WALK_IN,
    ),
    TrackedApplication(
        id="demo-005",
        date="2026-08-18",
        company="PyCore",
        role="Python Developer",
        sector="Python Developer",
        status=TrackerStatus.REJECTED,
        channel=TrackerChannel.REFERRAL,
    ),
]


def ensure_demo_data(store: TrackerStore) -> None:
    """Seed the tracker with demo rows when empty (first run)."""
    if store.list():
        return
    store.save(list(DEMO_APPLICATIONS))
