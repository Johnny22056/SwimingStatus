"""File-based data storage layer."""
import json
import logging
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from src.models import SwimEvent, BodyMetrics
from src.config import SWIM_EVENTS_FILE, BODY_METRICS_FILE, SCREENSHOT_INDEX_FILE, apply_course_override

logger = logging.getLogger(__name__)


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
        path.parent.mkdir(parents=True, exist_ok=True)
        # Create backup if file already exists
        if path.exists():
            backup_path = path.with_suffix(path.suffix + ".bak")
            try:
                shutil.copy2(path, backup_path)
                logger.debug("Created backup: %s", backup_path)
            except OSError as e:
                logger.warning("Failed to create backup %s: [%s] %s", backup_path, type(e).__name__, e)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
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

    @classmethod
    def _is_duplicate_event(cls, event: SwimEvent, existing_events: List[SwimEvent]) -> bool:
        """Check if event matches an existing record on composite key fields."""
        for existing in existing_events:
            if (existing.date == event.date
                    and existing.stroke.lower() == event.stroke.lower()
                    and int(existing.distance) == int(event.distance)
                    and existing.time == event.time
                    and existing.course.upper() == event.course.upper()):
                return True
        return False

    @classmethod
    def add_swim_event(cls, event: SwimEvent) -> Tuple[bool, str]:
        """Add a swim event if it's not a duplicate.

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
        SCREENSHOT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Create backup if file already exists
        if SCREENSHOT_INDEX_FILE.exists():
            backup_path = SCREENSHOT_INDEX_FILE.with_suffix(SCREENSHOT_INDEX_FILE.suffix + ".bak")
            try:
                shutil.copy2(SCREENSHOT_INDEX_FILE, backup_path)
                logger.debug("Created backup: %s", backup_path)
            except OSError as e:
                logger.warning("Failed to create backup %s: [%s] %s", backup_path, type(e).__name__, e)
        try:
            with open(SCREENSHOT_INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
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
