"""Screenshot ingestion and management."""
import hashlib
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

from src.config import SCREENSHOTS_DIR, SCREENSHOT_INDEX_FILE
from src.storage import ScreenshotIndex

logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Handles screenshot upload, storage, duplicate detection, and gallery."""

    @staticmethod
    def compute_checksum(file_path: Path) -> str:
        """Compute MD5 checksum of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @classmethod
    def sanitize_meet_name(cls, meet_name: str) -> str:
        """Sanitize meet name for use as a folder name.
        
        Replaces special characters and spaces to create a safe directory name.
        
        Args:
            meet_name: Raw meet name string
            
        Returns:
            Sanitized string suitable for filesystem paths
        """
        safe_meet = "".join(c if c.isalnum() or c in "-_ " else "_" for c in meet_name).strip()
        safe_meet = safe_meet.replace(" ", "_")
        return safe_meet

    @classmethod
    def save_uploaded_screenshot(
        cls,
        uploaded_file: Any,
        meet_name: str = "unknown_meet",
        event_date: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Save an uploaded screenshot to organized storage.

        Args:
            uploaded_file: Streamlit UploadedFile object.
            meet_name: Name of the swim meet.
            event_date: Date string in YYYY-MM-DD format; defaults to today.

        Returns:
            Tuple of (success, message). Success is False if a duplicate is detected.
        """
        if event_date is None:
            event_date = datetime.now().strftime("%Y-%m-%d")
        
        # Sanitize meet name for folder
        safe_meet = cls.sanitize_meet_name(meet_name)
        
        # Create folder structure
        target_dir = SCREENSHOTS_DIR / safe_meet / event_date
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = target_dir / uploaded_file.name
        
        # Remove old file if it exists (allow re-upload / overwrite)
        if target_path.exists():
            target_path.unlink()
            # Remove old index entry for this path
            ScreenshotIndex.remove_by_path(str(target_path.relative_to(SCREENSHOTS_DIR)))
        
        # Save file
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Compute checksum
        checksum = cls.compute_checksum(target_path)
        
        # Check for duplicate by checksum elsewhere in the index
        index = ScreenshotIndex.load()
        for screenshot in index.get("screenshots", []):
            if screenshot.get("checksum") == checksum and screenshot.get("path") != str(target_path.relative_to(SCREENSHOTS_DIR)):
                return False, f"Duplicate screenshot detected (checksum match): '{uploaded_file.name}'"
        
        # Add to index
        metadata = {
            "path": str(target_path.relative_to(SCREENSHOTS_DIR)),
            "original_filename": uploaded_file.name,
            "meet_name": meet_name,
            "date": event_date,
            "uploaded_at": datetime.now().isoformat(),
            "checksum": checksum,
            "size_bytes": target_path.stat().st_size
        }
        ScreenshotIndex.add(metadata)
        
        return True, f"Screenshot saved to {target_path}"

    @classmethod
    def save_from_path(
        cls,
        source_path: str,
        meet_name: str = "unknown_meet",
        event_date: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Save a screenshot from a local file path into the organized directory.

        Args:
            source_path: Absolute path to the image file.
            meet_name: Name of the swim meet.
            event_date: Date string in YYYY-MM-DD format; defaults to today.

        Returns:
            Tuple of (success, message_or_saved_path). Success is False if a
            duplicate is detected.
        """
        if event_date is None:
            event_date = datetime.now().strftime("%Y-%m-%d")

        source = Path(source_path)
        if not source.exists():
            return False, f"Source file not found: {source_path}"

        # Sanitize meet name for folder
        safe_meet = cls.sanitize_meet_name(meet_name)

        # Create folder structure
        target_dir = SCREENSHOTS_DIR / safe_meet / event_date
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / source.name

        # Remove old file if it exists (allow overwrite)
        if target_path.exists():
            target_path.unlink()
            # Remove old index entry for this path
            ScreenshotIndex.remove_by_path(str(target_path.relative_to(SCREENSHOTS_DIR)))

        # Copy file
        shutil.copy2(source, target_path)

        # Compute checksum
        checksum = cls.compute_checksum(target_path)

        # Check for duplicate by checksum elsewhere in the index
        index = ScreenshotIndex.load()
        for screenshot in index.get("screenshots", []):
            if screenshot.get("checksum") == checksum and screenshot.get("path") != str(target_path.relative_to(SCREENSHOTS_DIR)):
                return False, f"Duplicate screenshot detected (checksum match): '{source.name}'"

        # Add to index
        metadata = {
            "path": str(target_path.relative_to(SCREENSHOTS_DIR)),
            "original_filename": source.name,
            "meet_name": meet_name,
            "date": event_date,
            "uploaded_at": datetime.now().isoformat(),
            "checksum": checksum,
            "size_bytes": target_path.stat().st_size
        }
        ScreenshotIndex.add(metadata)

        return True, str(target_path)


