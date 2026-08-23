"""CRUD store for the applications tracker table."""

from __future__ import annotations

import json
import uuid
from datetime import date
from pathlib import Path

from job_search.config import Settings, get_settings
from job_search.models.schemas import TrackedApplication, TrackerChannel, TrackerStatus


class TrackerStore:
    def __init__(self, settings: Settings | None = None, path: Path | None = None) -> None:
        self.settings = settings or get_settings()
        folder = self.settings.data_dir / "applications"
        folder.mkdir(parents=True, exist_ok=True)
        self.path = path or folder / "tracker.json"

    def list(self) -> list[TrackedApplication]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8") or "[]")
        return [TrackedApplication.model_validate(item) for item in raw]

    def get(self, application_id: str) -> TrackedApplication | None:
        for item in self.list():
            if item.id == application_id:
                return item
        return None

    def save(self, items: list[TrackedApplication]) -> None:
        payload = [item.model_dump(mode="json") for item in items]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(
        self,
        company: str,
        role: str,
        sector: str,
        status: TrackerStatus,
        channel: TrackerChannel | str = TrackerChannel.ONLINE,
    ) -> TrackedApplication:
        item = TrackedApplication(
            id=uuid.uuid4().hex[:8],
            date=date.today().isoformat(),
            company=company.strip(),
            role=role.strip(),
            sector=sector.strip(),
            status=status,
            channel=TrackerChannel(channel) if not isinstance(channel, TrackerChannel) else channel,
        )
        items = self.list()
        items.insert(0, item)
        self.save(items)
        return item

    def update(self, application_id: str, **changes) -> TrackedApplication | None:
        items = self.list()
        updated: TrackedApplication | None = None
        next_items: list[TrackedApplication] = []
        for item in items:
            if item.id != application_id:
                next_items.append(item)
                continue
            payload = item.model_dump()
            payload.update(changes)
            updated = TrackedApplication.model_validate(payload)
            next_items.append(updated)
        if updated:
            self.save(next_items)
        return updated

    def delete(self, application_id: str) -> bool:
        items = self.list()
        remaining = [item for item in items if item.id != application_id]
        if len(remaining) == len(items):
            return False
        self.save(remaining)
        return True

    def counts(self) -> dict[str, int]:
        items = self.list()
        return {
            "total": len(items),
            TrackerStatus.ACTIVE.value: sum(item.status == TrackerStatus.ACTIVE for item in items),
            TrackerStatus.IN_PROCESS.value: sum(
                item.status == TrackerStatus.IN_PROCESS for item in items
            ),
            TrackerStatus.INTERVIEW.value: sum(
                item.status == TrackerStatus.INTERVIEW for item in items
            ),
            TrackerStatus.OFFER.value: sum(item.status == TrackerStatus.OFFER for item in items),
            TrackerStatus.HIRED.value: sum(item.status == TrackerStatus.HIRED for item in items),
            TrackerStatus.REJECTED.value: sum(
                item.status == TrackerStatus.REJECTED for item in items
            ),
        }
