"""Project configuration and paths.

Requires Python 3.9+ for built-in generic types (e.g., dict, list)
used in type annotations throughout the codebase.
"""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # Load .env or .env.local if present

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
EXTRACTED_DIR = DATA_DIR / "extracted"

# Data files
BODY_METRICS_FILE = DATA_DIR / "body_metrics.json"
SWIM_EVENTS_FILE = DATA_DIR / "swim_events.json"
SCREENSHOT_INDEX_FILE = SCREENSHOTS_DIR / "index.json"

# Ensure directories exist
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

# Alibaba Cloud Model Studio settings
ALIBABA_CLOUD_API_KEY = os.getenv("ALIBABA_CLOUD_API_KEY", "").strip()
ALIBABA_CLOUD_BASE_URL = os.getenv("ALIBABA_CLOUD_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1").strip()
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen-vl-max").strip()
QWEN_TEXT_MODEL_NAME = os.getenv("QWEN_TEXT_MODEL_NAME", "qwen-max").strip()

# Startup validation
if not ALIBABA_CLOUD_API_KEY:
    logger.warning("ALIBABA_CLOUD_API_KEY not set - OCR and Q&A features will be unavailable")

# Swimming domain terms used for query scope classification
SWIMMING_TERMS = ["swim", "stroke", "time", "race", "meet", "freestyle", "backstroke",
                  "breaststroke", "butterfly", "sunny", "personal best", "rank", "split",
                  "training", "improve", "progress", "benchmark", "analytics", "body",
                  "height", "weight", "bmi", "metric"]

# Time format regex patterns
TIME_FORMAT_MM_SS = r"^\d{1,2}:\d{2}\.\d{2}$"
TIME_FORMAT_SS = r"^\d{1,2}\.\d{2}$"

# Internal metadata: override course for meets where OCR may extract wrong course info
MEET_COURSE_OVERRIDES: dict[str, str] = {
    "CWSC+Millfield 2024 Int'l Open (Heats)": "SC",
    "CWSC+Millfield 2024 Int'l Open (Finals)": "SC",
    "CWSC+Millfield 2023 Int'l Open": "SC",
}


def apply_course_override(meet_name: str, course: str) -> str:
    """Return the correct course for a meet, applying override if matched (case-insensitive)."""
    meet_lower = meet_name.strip().lower()
    for override_meet, override_course in MEET_COURSE_OVERRIDES.items():
        if override_meet.lower() == meet_lower:
            if course.upper() != override_course.upper():
                logger.info("Course override applied: '%s' %s -> %s", meet_name, course, override_course)
            return override_course
    return course
