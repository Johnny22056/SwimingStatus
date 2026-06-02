"""File-based data storage layer."""
import json
import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from src.models import SwimEvent, BodyMetrics
from src.config import SWIM_EVENTS_FILE, BODY_METRICS_FILE, SCREENSHOT_INDEX_FILE, apply_course_override

logger = logging.getLogger(__name__)

# Number of rotated backups to keep
BACKUP_KEEP = 3


def _rotate_backups(path: Path, keep: int = BACKUP_KEEP) -> None:
    """Rotate `.bak.1` … `.bak.N` so the newest snapshot is `.bak.1`."""
    if not path.exists():
        return
    # Drop the oldest, shift the rest
    oldest = path.with_suffix(path.suffix + f".bak.{keep}")
    if oldest.exists():
        try:
            oldest.unlink()
        except OSError as e:
            logger.warning("Failed to remove oldest backup %s: [%s] %s", oldest, type(e).__name__, e)
    for n in range(keep - 1, 0, -1):
        src = path.with_suffix(path.suffix + f".bak.{n}")
        dst = path.with_suffix(path.suffix + f".bak.{n + 1}")
        if src.exists():
            try:
                src.replace(dst)
            except OSError as e:
                logger.warning("Failed to rotate %s -> %s: [%s] %s", src, dst, type(e).__name__, e)
    new_backup = path.with_suffix(path.suffix + ".bak.1")
    try:
        shutil.copy2(path, new_backup)
    except OSError as e:
        logger.warning("Failed to write backup %s: [%s] %s", new_backup, type(e).__name__, e)


def _atomic_write_json(path: Path, payload: Any) -> None:
    """Write JSON atomically (tempfile in the same dir + os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


class DataStore:
    """JSON-based persistence for swimming data."""

    @staticmethod
    def _load_json(path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning("Failed to load JSON from %s: [%s] %s", path, type(e).__name__, e)
            return []

    @staticmethod
    def _save_json(path: Path, data: List[Dict[str, Any]]) -> None:
        _rotate_backups(path)
        try:
            _atomic_write_json(path, data)
            logger.debug("Saved JSON to %s (%d items)", path, len(data))
        except (OSError, TypeError) as e:
            logger.error("Failed to save JSON to %s: [%s] %s", path, type(e).__name__, e)
            raise

    # Swim Events
    @classmethod
    def load_swim_events(cls) -> List[SwimEvent]:
        data = cls._load_json(SWIM_EVENTS_FILE)
        events = [SwimEvent.from_dict(item) for item in data]
        for event in events:
            event.course = apply_course_override(event.meet_name, event.course)
        return events

    @classmethod
    def save_swim_events(cls, events: List[SwimEvent]) -> None:
        data = [event.to_dict() for event in events]
        cls._save_json(SWIM_EVENTS_FILE, data)

    @staticmethod
    def _event_key(event: SwimEvent) -> Tuple[str, str, int, str, str]:
        return (
            event.date,
            event.stroke.lower(),
            int(event.distance),
            event.time,
            event.course.upper(),
        )

    @classmethod
    def _is_duplicate_event(cls, event: SwimEvent, existing_events: List[SwimEvent]) -> bool:
        """Check if event matches an existing record on composite key fields."""
        target = cls._event_key(event)
        return any(cls._event_key(e) == target for e in existing_events)

    @classmethod
    def add_swim_event(cls, event: SwimEvent) -> Tuple[bool, str]:
        """Add a single swim event if it's not a duplicate.

        Returns:
            (True, "") if successfully added.
            (False, "duplicate") if skipped as duplicate.
        """
        event.course = apply_course_override(event.meet_name, event.course)
        events = cls.load_swim_events()
        if cls._is_duplicate_event(event, events):
            logger.info("Duplicate event skipped: %s %dm %s on %s",
                        event.stroke, event.distance, event.time, event.date)
            return (False, "duplicate")
        events.append(event)
        cls.save_swim_events(events)
        return (True, "")

    @classmethod
    def add_swim_events_batch(cls, candidates: List[SwimEvent]) -> Tuple[int, int]:
        """Add many events in a single load/save cycle.

        Returns:
            (added_count, duplicate_count). Skips duplicates against existing
            records *and* against earlier candidates in the same batch.
        """
        if not candidates:
            return (0, 0)
        events = cls.load_swim_events()
        seen = {cls._event_key(e) for e in events}
        added = 0
        duplicates = 0
        for cand in candidates:
            cand.course = apply_course_override(cand.meet_name, cand.course)
            key = cls._event_key(cand)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            events.append(cand)
            added += 1
        if added:
            cls.save_swim_events(events)
        return (added, duplicates)

    # Body Metrics
    @classmethod
    def load_body_metrics(cls) -> List[BodyMetrics]:
        data = cls._load_json(BODY_METRICS_FILE)
        return [BodyMetrics.from_dict(item) for item in data]

    @classmethod
    def save_body_metrics(cls, metrics: List[BodyMetrics]) -> None:
        data = [m.to_dict() for m in metrics]
        cls._save_json(BODY_METRICS_FILE, data)

    @classmethod
    def add_body_metric(cls, metric: BodyMetrics) -> None:
        metrics = cls.load_body_metrics()
        metrics.append(metric)
        cls.save_body_metrics(metrics)


class ScreenshotIndex:
    """Manages screenshot metadata index."""

    @classmethod
    def load(cls) -> Dict[str, Any]:
        if not SCREENSHOT_INDEX_FILE.exists():
            return {"screenshots": []}
        try:
            with open(SCREENSHOT_INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning("Failed to load screenshot index from %s: [%s] %s", SCREENSHOT_INDEX_FILE, type(e).__name__, e)
            return {"screenshots": []}

    @classmethod
    def save(cls, index: Dict[str, Any]) -> None:
        _rotate_backups(SCREENSHOT_INDEX_FILE)
        try:
            _atomic_write_json(SCREENSHOT_INDEX_FILE, index)
            logger.debug("Saved screenshot index (%d entries)", len(index.get("screenshots", [])))
        except (OSError, TypeError) as e:
            logger.error("Failed to save screenshot index to %s: [%s] %s", SCREENSHOT_INDEX_FILE, type(e).__name__, e)
            raise

    @classmethod
    def add(cls, metadata: Dict[str, Any]) -> None:
        index = cls.load()
        index["screenshots"].append(metadata)
        cls.save(index)

    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        return cls.load().get("screenshots", [])

    @classmethod
    def get_by_path(cls, path: str) -> Optional[Dict[str, Any]]:
        for screenshot in cls.list_all():
            if screenshot.get("path") == path:
                return screenshot
        return None

    @classmethod
    def remove_by_path(cls, path: str) -> bool:
        index = cls.load()
        original_len = len(index["screenshots"])
        index["screenshots"] = [s for s in index["screenshots"] if s.get("path") != path]
        cls.save(index)
        return len(index["screenshots"]) < original_len

    @classmethod
    def has_checksum(cls, checksum: str, exclude_path: Optional[str] = None) -> bool:
        """True if an entry with this checksum exists (optionally ignoring one path)."""
        for s in cls.list_all():
            if s.get("checksum") == checksum and s.get("path") != exclude_path:
                return True
        return False
