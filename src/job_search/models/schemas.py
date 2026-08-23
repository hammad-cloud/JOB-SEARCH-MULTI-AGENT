"""Shared data contracts used by agents, tools, and the UI."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ApplicationStatus(StrEnum):
    SAVED = "saved"
    DRAFTED = "drafted"
    APPLIED = "applied"
    INTERVIEW = "interview"
    REJECTED = "rejected"


class TrackerStatus(StrEnum):
    ACTIVE = "Applied / Active"
    IN_PROCESS = "In process"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    HIRED = "Hired"
    REJECTED = "Rejected/Closed"


class TrackerChannel(StrEnum):
    ONLINE = "online"
    REFERRAL = "referral"
    WALK_IN = "walk in interview"


class TrackedApplication(BaseModel):
    id: str
    date: str
    company: str
    role: str
    sector: str = ""
    status: TrackerStatus = TrackerStatus.ACTIVE
    channel: TrackerChannel = TrackerChannel.ONLINE

    @field_validator("channel", mode="before")
    @classmethod
    def _normalize_channel(cls, value: object) -> object:
        if value is None or value == "":
            return TrackerChannel.ONLINE
        text = str(value).strip().lower()
        aliases = {
            "online": TrackerChannel.ONLINE,
            "referral": TrackerChannel.REFERRAL,
            "walk in interview": TrackerChannel.WALK_IN,
            "walk-in": TrackerChannel.WALK_IN,
            "walkin": TrackerChannel.WALK_IN,
            "portal": TrackerChannel.ONLINE,
        }
        return aliases.get(text, TrackerChannel.ONLINE)


class SearchPreferences(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    location: str = "Remote"
    remote_only: bool = True
    results_limit: int = 25


class JobBoardQuery(BaseModel):
    keywords: str = "software engineer"
    location: str = "Remote"
    source: str = "LinkedIn"
    results_limit: int = 25
    remote_friendly: bool = True


class Profile(BaseModel):
    name: str = "Candidate"
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    target_titles: list[str] = Field(default_factory=list)
    years_experience: float | None = None
    locations: list[str] = Field(default_factory=list)
    source_resume: str | None = None


class JobPosting(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: HttpUrl | None = None
    source: str = "mock"
    remote: bool = True
    posted_at: datetime | None = None


class MatchResult(BaseModel):
    job_id: str
    score: int = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    job: JobPosting | None = None


class CompanyBrief(BaseModel):
    job_id: str
    company: str
    summary: str
    notes: list[str] = Field(default_factory=list)


class ApplicationDraft(BaseModel):
    job_id: str
    cover_letter: str
    resume_bullets: list[str] = Field(default_factory=list)
    status: ApplicationStatus = ApplicationStatus.DRAFTED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PipelineResult(BaseModel):
    profile: Profile
    jobs: list[JobPosting] = Field(default_factory=list)
    matches: list[MatchResult] = Field(default_factory=list)
    briefs: list[CompanyBrief] = Field(default_factory=list)
    drafts: list[ApplicationDraft] = Field(default_factory=list)
