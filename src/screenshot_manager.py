"""Screenshot ingestion and management."""
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

from src.config import SCREENSHOTS_DIR
from src.storage import ScreenshotIndex

logger = logging.getLogger(__name__)


def _hash_bytes(data: bytes) -> str:
    h = hashlib.md5(usedforsecurity=False)
    h.update(data)
    return h.hexdigest()


class ScreenshotManager:
    """Handles screenshot upload, storage, duplicate detection, and gallery."""

    @staticmethod
    def compute_checksum(file_path: Path) -> str:
        """Compute MD5 checksum of a file (used only for dedup)."""
        hash_md5 = hashlib.md5(usedforsecurity=False)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @classmethod
    def sanitize_meet_name(cls, meet_name: str) -> str:
        """Sanitize meet name for use as a folder name.

        Replaces special characters and spaces to create a safe directory name.
        """
        safe_meet = "".join(c if c.isalnum() or c in "-_ " else "_" for c in meet_name).strip()
        return safe_meet.replace(" ", "_")

    @classmethod
    def _commit_screenshot(
        cls,
        data: bytes,
        original_filename: str,
        meet_name: str,
        event_date: Optional[str],
    ) -> Tuple[bool, str]:
        """Hash, dedup-check, then write the screenshot.

        Returns (True, saved_path_str) on success, (False, message) otherwise.
        The file is NEVER written when a duplicate is detected.
        """
        if event_date is None:
            event_date = datetime.now().strftime("%Y-%m-%d")

        checksum = _hash_bytes(data)

        safe_meet = cls.sanitize_meet_name(meet_name) or "unknown_meet"
        target_dir = SCREENSHOTS_DIR / safe_meet / event_date
        target_path = target_dir / original_filename
        relative_path = str(target_path.relative_to(SCREENSHOTS_DIR))

        # Reject duplicates against any *other* indexed screenshot
        if ScreenshotIndex.has_checksum(checksum, exclude_path=relative_path):
            return False, f"Duplicate screenshot detected (checksum match): '{original_filename}'"

        # Safe to write
        target_dir.mkdir(parents=True, exist_ok=True)
        if target_path.exists():
            # Replacing an existing file at the same path — drop the stale index entry first
            ScreenshotIndex.remove_by_path(relative_path)
        target_path.write_bytes(data)

        metadata = {
            "path": relative_path,
            "original_filename": original_filename,
            "meet_name": meet_name,
            "date": event_date,
            "uploaded_at": datetime.now().isoformat(),
            "checksum": checksum,
            "size_bytes": len(data),
        }
        ScreenshotIndex.add(metadata)
        return True, str(target_path)

    @classmethod
    def save_uploaded_screenshot(
        cls,
        uploaded_file: Any,
        meet_name: str = "unknown_meet",
        event_date: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Save a Streamlit UploadedFile into organized storage."""
        try:
            data = uploaded_file.getvalue()
        except AttributeError:
            data = bytes(uploaded_file.getbuffer())
        return cls._commit_screenshot(data, uploaded_file.name, meet_name, event_date)

    @classmethod
    def save_from_path(
        cls,
        source_path: str,
        meet_name: str = "unknown_meet",
        event_date: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Save a screenshot from a local file path into organized storage."""
        source = Path(source_path)
        if not source.exists():
            return False, f"Source file not found: {source_path}"
        try:
            data = source.read_bytes()
        except OSError as e:
            return False, f"Failed to read source file: {type(e).__name__}: {e}"
        return cls._commit_screenshot(data, source.name, meet_name, event_date)
