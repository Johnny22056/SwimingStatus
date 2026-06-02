"""Tests for src.screenshot_manager: checksum-before-write and dedup behavior."""
from pathlib import Path

import pytest


@pytest.fixture
def isolated_screenshots(monkeypatch, tmp_path):
    screenshots_dir = tmp_path / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    index_file = screenshots_dir / "index.json"

    monkeypatch.setattr("src.screenshot_manager.SCREENSHOTS_DIR", screenshots_dir)
    monkeypatch.setattr("src.storage.SCREENSHOT_INDEX_FILE", index_file)
    return screenshots_dir


class FakeUpload:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


def test_sanitize_meet_name_replaces_special_chars():
    from src.screenshot_manager import ScreenshotManager
    assert ScreenshotManager.sanitize_meet_name("Spring Open / 2024!") == "Spring_Open___2024_"


def test_upload_writes_and_indexes_file(isolated_screenshots):
    from src.screenshot_manager import ScreenshotManager
    ok, path = ScreenshotManager.save_uploaded_screenshot(
        FakeUpload("shot.png", b"PNG-DATA-A"),
        meet_name="Test Meet",
        event_date="2024-01-15",
    )
    assert ok
    target = Path(path)
    assert target.exists()
    assert target.read_bytes() == b"PNG-DATA-A"


def test_duplicate_checksum_does_not_write_file(isolated_screenshots):
    """Bug fix: previously the file was written before the dedup check, leaving an orphan."""
    from src.screenshot_manager import ScreenshotManager

    ok, _ = ScreenshotManager.save_uploaded_screenshot(
        FakeUpload("first.png", b"SAME-BYTES"), "Meet One", "2024-01-15"
    )
    assert ok

    # Different filename + meet, same bytes → must be rejected as duplicate
    ok, msg = ScreenshotManager.save_uploaded_screenshot(
        FakeUpload("second.png", b"SAME-BYTES"), "Meet Two", "2024-02-20"
    )
    assert not ok
    assert "duplicate" in msg.lower()

    # And no orphan file should exist for the rejected upload
    second_path = isolated_screenshots / "Meet_Two" / "2024-02-20" / "second.png"
    assert not second_path.exists()


def test_save_from_path_rejects_missing_source(isolated_screenshots, tmp_path):
    from src.screenshot_manager import ScreenshotManager
    ok, msg = ScreenshotManager.save_from_path(str(tmp_path / "nope.png"), "M", "2024-01-15")
    assert not ok and "not found" in msg.lower()
