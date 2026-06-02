"""Tests for src.storage (atomic writes, dedup, batch insert, backup rotation)."""
import json
from pathlib import Path

import pytest

from src.models import SwimEvent


@pytest.fixture
def isolated_storage(monkeypatch, tmp_path):
    """Redirect storage to a temp directory so tests don't touch real data."""
    swim_events = tmp_path / "swim_events.json"
    body_metrics = tmp_path / "body_metrics.json"
    screenshot_index = tmp_path / "screenshots" / "index.json"

    monkeypatch.setattr("src.storage.SWIM_EVENTS_FILE", swim_events)
    monkeypatch.setattr("src.storage.BODY_METRICS_FILE", body_metrics)
    monkeypatch.setattr("src.storage.SCREENSHOT_INDEX_FILE", screenshot_index)

    # Drop overrides — tests should see their input data verbatim
    monkeypatch.setattr("src.storage.apply_course_override", lambda meet, course: course)

    return {"swim_events": swim_events, "body_metrics": body_metrics, "index": screenshot_index}


def make_event(date="2024-01-15", stroke="freestyle", distance=100, time="1:00.00", course="LC"):
    return SwimEvent(date=date, meet_name="Open", stroke=stroke, distance=distance, time=time, course=course)


class TestDedup:
    def test_event_key_normalizes_case(self, isolated_storage):
        from src.storage import DataStore
        a = make_event(stroke="Freestyle", course="lc")
        b = make_event(stroke="freestyle", course="LC")
        assert DataStore._event_key(a) == DataStore._event_key(b)

    def test_add_event_rejects_duplicate(self, isolated_storage):
        from src.storage import DataStore
        ok, _ = DataStore.add_swim_event(make_event())
        assert ok
        ok, reason = DataStore.add_swim_event(make_event())
        assert not ok and reason == "duplicate"
        # File should contain exactly one record
        contents = json.loads(isolated_storage["swim_events"].read_text())
        assert len(contents) == 1

    def test_add_event_accepts_different_course(self, isolated_storage):
        from src.storage import DataStore
        ok1, _ = DataStore.add_swim_event(make_event(course="LC"))
        ok2, _ = DataStore.add_swim_event(make_event(course="SC"))
        assert ok1 and ok2


class TestBatchInsert:
    def test_batch_dedupes_against_existing_and_within_batch(self, isolated_storage):
        from src.storage import DataStore

        DataStore.add_swim_event(make_event(date="2024-01-15", time="1:00.00"))
        added, dupes = DataStore.add_swim_events_batch([
            make_event(date="2024-01-15", time="1:00.00"),    # duplicate of existing
            make_event(date="2024-02-20", time="59.50"),      # new
            make_event(date="2024-02-20", time="59.50"),      # duplicate of previous candidate
            make_event(date="2024-03-10", time="58.20"),      # new
        ])
        assert added == 2 and dupes == 2
        contents = json.loads(isolated_storage["swim_events"].read_text())
        assert len(contents) == 3

    def test_empty_batch_is_noop(self, isolated_storage):
        from src.storage import DataStore
        added, dupes = DataStore.add_swim_events_batch([])
        assert (added, dupes) == (0, 0)
        # No file should be written for an empty batch
        assert not isolated_storage["swim_events"].exists()


class TestAtomicWriteAndBackup:
    def test_atomic_write_no_tempfile_left_behind(self, isolated_storage):
        from src.storage import DataStore
        DataStore.add_swim_event(make_event())
        tmp_files = [p for p in isolated_storage["swim_events"].parent.iterdir() if p.suffix == ".tmp"]
        assert tmp_files == []

    def test_backup_rotation_creates_bak_1(self, isolated_storage):
        from src.storage import DataStore
        DataStore.add_swim_event(make_event(date="2024-01-15"))
        # Second save should create .bak.1 (a snapshot of the first save)
        DataStore.add_swim_event(make_event(date="2024-01-16"))
        bak1 = isolated_storage["swim_events"].with_suffix(".json.bak.1")
        assert bak1.exists()
        first_snapshot = json.loads(bak1.read_text())
        assert len(first_snapshot) == 1

    def test_backup_rotation_keeps_three(self, isolated_storage):
        from src.storage import DataStore
        for i, day in enumerate(["15", "16", "17", "18", "19"]):
            DataStore.add_swim_event(make_event(date=f"2024-01-{day}"))
        path = isolated_storage["swim_events"]
        assert path.with_suffix(".json.bak.1").exists()
        assert path.with_suffix(".json.bak.2").exists()
        assert path.with_suffix(".json.bak.3").exists()
        # Should not keep .bak.4
        assert not path.with_suffix(".json.bak.4").exists()


class TestScreenshotIndex:
    def test_has_checksum_excludes_self(self, isolated_storage):
        from src.storage import ScreenshotIndex
        ScreenshotIndex.add({"path": "a.png", "checksum": "abc"})
        assert ScreenshotIndex.has_checksum("abc") is True
        assert ScreenshotIndex.has_checksum("abc", exclude_path="a.png") is False
        assert ScreenshotIndex.has_checksum("xyz") is False
