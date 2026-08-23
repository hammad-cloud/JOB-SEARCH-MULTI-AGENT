from job_search.models.schemas import TrackerChannel, TrackerStatus
from job_search.tools.tracker import TrackerStore


def test_tracker_add_update_delete(tmp_path) -> None:
    store = TrackerStore(path=tmp_path / "tracker.json")
    created = store.add(
        "Folio3",
        "Junior engineer",
        "Python",
        TrackerStatus.IN_PROCESS,
        channel=TrackerChannel.REFERRAL,
    )
    assert store.counts()["In process"] == 1
    assert store.counts()["total"] == 1
    assert created.channel == TrackerChannel.REFERRAL

    updated = store.update(
        created.id,
        company="Folio3",
        status=TrackerStatus.INTERVIEW,
        channel=TrackerChannel.WALK_IN,
    )
    assert updated is not None
    assert updated.status == TrackerStatus.INTERVIEW
    assert updated.channel == TrackerChannel.WALK_IN
    assert store.counts()["In process"] == 0
    assert store.counts()[TrackerStatus.INTERVIEW.value] == 1

    assert store.delete(created.id) is True
    assert store.list() == []
    assert store.counts()["total"] == 0


def test_tracker_normalizes_legacy_channel(tmp_path) -> None:
    path = tmp_path / "tracker.json"
    path.write_text(
        '[{"id":"a1","date":"2026-08-23","company":"Acme","role":"Dev",'
        '"sector":"IT","status":"Applied / Active","channel":"portal"}]',
        encoding="utf-8",
    )
    store = TrackerStore(path=path)
    item = store.list()[0]
    assert item.channel == TrackerChannel.ONLINE
