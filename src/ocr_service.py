"""OCR data extraction using Alibaba Cloud Model Studio Service."""
import base64
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError, OpenAIError

from src.base_service import AlibabaPlatformService, ServiceInitError
from src.config import ALIBABA_CLOUD_API_KEY, QWEN_MODEL_NAME
from src.validation import validate_swim_event_data

logger = logging.getLogger(__name__)


class OCRService(AlibabaPlatformService):
    """Extracts structured swimming data from screenshots using Qwen vision-language model."""

    def __init__(self) -> None:
        """Initialize OCRService with the Qwen vision model.

        Sets self.client to None if the API key is missing or initialization fails.
        """
        try:
            super().__init__(QWEN_MODEL_NAME)
        except ServiceInitError:
            self.client = None

    @staticmethod
    def _encode_image(image_path: str) -> str:
        """Encode an image file to a base64 string.

        Args:
            image_path: Absolute or relative path to the image file.

        Returns:
            Base64-encoded string of the image contents.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def _get_image_mime_type(image_path: str) -> str:
        """Detect MIME type from file extension.

        Args:
            image_path: Path to the image file.

        Returns:
            MIME type string (e.g., 'image/png'); defaults to 'image/jpeg'.
        """
        ext = Path(image_path).suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return mime_types.get(ext, "image/jpeg")

    @staticmethod
    def _get_extraction_prompt() -> str:
        """Get the system prompt for swimming data extraction.

        Returns:
            Detailed instruction string for the Qwen vision model.
        """
        return """Analyze this swimming meet result screenshot carefully and extract every piece of visible information into a single JSON object.

STEP-BY-STEP INSTRUCTIONS:
1. First, identify what type of document this is (heat sheet, results page, timing sheet, etc.)
2. Look for the swimmer's name, event details, and race times
3. Check for split times at each 50m turn
4. Look for heat/lane assignments and final rankings
5. Identify if it's a Long Course (LC/50m) or Short Course (SC/25m) pool

EXTRACT THESE FIELDS:
- date: Event date in YYYY-MM-DD format
- meet_name: Name of the swim meet or competition
- stroke: One of: freestyle, backstroke, breaststroke, butterfly, IM
- distance: Distance in meters as a NUMBER (50, 100, 200, 400, 800, 1500)
- time: Total race time with hundredths of a second (e.g., "1:23.45" or "45.67")
- splits: Array of split times at each lap/50m turn (e.g., ["32.10", "35.20", "36.15"])
- course: "LC" for 50m pool or "SC" for 25m pool
- round: One of: "heat", "semifinal", "final"
- rank: Final placement as a NUMBER (1, 2, 3, etc.)
- age_group: Age category (e.g., "8 & Under", "9-10", "11-12", "13-14")
- heat_lane: Heat and lane info (e.g., "H3 L4")
- swimmer_name: The swimmer's name as shown in the results

EXAMPLE OUTPUT:
{
  "date": "2024-03-15",
  "meet_name": "Spring Championships",
  "stroke": "freestyle",
  "distance": 100,
  "time": "1:23.45",
  "splits": ["40.20", "43.25"],
  "course": "LC",
  "round": "final",
  "rank": 2,
  "age_group": "11-12",
  "heat_lane": "H2 L3",
  "swimmer_name": "Sunny"
}

CRITICAL RULES:
- Return ONLY valid JSON — no markdown, no explanations, no code blocks
- Look at EVERY part of the image — top, bottom, left, right corners
- Extract ALL visible numbers and text related to swimming
- Use null for fields you cannot find in the image
- Time values MUST have exactly 2 digits after the decimal point
- Distance MUST be a number, never a string
- Splits MUST be an array of strings, even if there's only one split"""

    def extract_from_screenshot(self, image_path: str) -> Tuple[bool, Dict[str, Any], str]:
        """Extract structured swimming data from a screenshot using the Qwen vision model.

        Args:
            image_path: Path to the screenshot image file.

        Returns:
            Tuple of (success, extracted_data_dict, message).
            extracted_data_dict includes '_extraction_confidence',
            '_extraction_errors', and '_raw_response' metadata keys.
        """
        logger.info("Starting extraction from screenshot: %s", image_path)
        if not ALIBABA_CLOUD_API_KEY or self.client is None:
            logger.warning("Extraction aborted: API key not configured or client unavailable.")
            return False, {}, "Alibaba Cloud API key not configured. Set ALIBABA_CLOUD_API_KEY environment variable."
        
        try:
            base64_image = self._encode_image(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            logger.debug("Calling API with model '%s' for image: %s", self.model, image_path)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise swimming data extraction assistant. Your job is to carefully examine screenshots of swimming meet results and extract every visible detail into structured JSON."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": self._get_extraction_prompt()
                            }
                        ]
                    }
                ],
                max_tokens=4096,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            
            # Clean up potential markdown formatting
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Parse JSON
            try:
                data = json.loads(content)
                logger.debug("JSON response parsed successfully.")
            except json.JSONDecodeError as e:
                logger.warning("Failed to parse JSON response: %s", e)
                return False, {"raw_response": content}, f"Failed to parse JSON response: {str(e)}"
            
            # Normalize data: convert None to appropriate defaults
            text_fields = ["date", "meet_name", "stroke", "time", "course", "round", "age_group", "heat_lane", "swimmer_name"]
            numeric_fields = ["distance", "rank"]
            for field in text_fields:
                if field in data and data[field] is None:
                    data[field] = ""
            for field in numeric_fields:
                if field in data and data[field] is None:
                    data[field] = 0
            if "splits" in data and data["splits"] is None:
                data["splits"] = []
            
            # Validate extracted data
            is_valid, errors = validate_swim_event_data(data)
            logger.info("Extraction complete. Valid=%s, errors=%s", is_valid, errors)
            
            # Add confidence scores (placeholder since we can't get real confidence from the API)
            data["_extraction_confidence"] = {
                field: 95 if data.get(field) else 0
                for field in ["date", "meet_name", "stroke", "distance", "time", "splits", "course", "round", "rank", "age_group"]
            }
            data["_extraction_errors"] = errors
            data["_raw_response"] = content[:2000]  # Include raw model response for debugging
            
            return is_valid, data, "Extraction complete" + (". Validation errors: " + "; ".join(errors) if errors else "")
            
        except APIConnectionError as e:
            logger.error("API connection error during extraction: %s", e)
            return False, {}, f"Connection error. Please check your internet connection and API base URL. Details: {str(e)}"
        except AuthenticationError as e:
            logger.error("API authentication error during extraction: %s", e)
            return False, {}, f"Authentication failed. Please check your Alibaba Cloud API key. Details: {str(e)}"
        except RateLimitError as e:
            logger.error("API rate limit exceeded during extraction: %s", e)
            return False, {}, f"Rate limit exceeded. Please wait and try again. Details: {str(e)}"
        except Exception as e:
            logger.error("Extraction failed: %s: %s", type(e).__name__, e, exc_info=True)
            return False, {}, f"Extraction failed: {type(e).__name__}: {str(e)}"

    @classmethod
    def manual_entry_form_fields(cls) -> List[Dict[str, Any]]:
        """Return field definitions for a manual data entry fallback form.

        Returns:
            List of field descriptor dicts with 'name', 'label', 'type',
            and optionally 'options' and 'required' keys.
        """
        return [
            {"name": "date", "label": "Date", "type": "date", "required": True},
            {"name": "meet_name", "label": "Meet Name", "type": "text", "required": True},
            {"name": "stroke", "label": "Stroke", "type": "select", "options": ["freestyle", "backstroke", "breaststroke", "butterfly", "IM"], "required": True},
            {"name": "distance", "label": "Distance (m)", "type": "number", "required": True},
            {"name": "time", "label": "Time (MM:SS.ss)", "type": "text", "required": True},
            {"name": "splits", "label": "Splits (comma-separated)", "type": "text", "required": False},
            {"name": "course", "label": "Course", "type": "select", "options": ["LC", "SC"], "required": False},
            {"name": "round", "label": "Round", "type": "select", "options": ["heat", "semifinal", "final"], "required": False},
            {"name": "rank", "label": "Rank", "type": "number", "required": False},
            {"name": "age_group", "label": "Age Group", "type": "text", "required": False},
            {"name": "heat_lane", "label": "Heat/Lane", "type": "text", "required": False},
        ]

    @classmethod
    def parse_splits(cls, splits_text: str) -> List[str]:
        """Parse comma-separated split time strings.

        Args:
            splits_text: Comma-separated split times (e.g., '32.10, 35.20').

        Returns:
            List of trimmed, non-empty split time strings.
        """
        if not splits_text:
            return []
        return [s.strip() for s in splits_text.split(",") if s.strip()]

    @staticmethod
    def _standards_prompt() -> str:
        return """Extract all swimming time standards from this image into a structured format.
For each event, provide: Event name (in English, e.g. "50m Freestyle"), and times for each level.
The columns are: International Master (国际级运动健将), National Master (运动健将), Level 1 (一级运动员), Level 2 (二级运动员).
There may be separate columns for 50m pool (Long Course) and 25m pool (Short Course).

Return as JSON with this structure:
{
  "lc_standards": [{"Event": "50m Freestyle", "International Master": "24.70", "National Master": "25.85", "Level 1": "27.20", "Level 2": "31.50"}, ...],
  "sc_standards": [{"Event": "50m Freestyle", "International Master": "24.44", "National Master": "25.00", "Level 1": "26.40", "Level 2": "30.50"}, ...]
}

Use English event names: "50m Freestyle", "100m Freestyle", "200m Freestyle", "400m Freestyle", "800m Freestyle", "1500m Freestyle", "50m Backstroke", "100m Backstroke", "200m Backstroke", "50m Breaststroke", "100m Breaststroke", "200m Breaststroke", "50m Butterfly", "100m Butterfly", "200m Butterfly", "100m IM", "200m IM", "400m IM".
Format times as SS.ss or M:SS.ss or MM:SS.ss as appropriate.
Return ONLY the JSON, no other text."""

    def extract_standards_from_bytes(self, image_bytes: bytes, file_ext: str) -> Tuple[bool, Dict[str, Any], str]:
        """Extract standards table from a raw image-bytes upload.

        Returns:
            (success, parsed_dict, message). parsed_dict has keys 'lc_standards'
            and/or 'sc_standards' on success, or {'raw_response': ...} when the
            model returned text that didn't parse as JSON.
        """
        if not ALIBABA_CLOUD_API_KEY or self.client is None:
            return False, {}, "Alibaba Cloud API key not configured."

        ext = file_ext.lower().lstrip(".")
        mime_type = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext or 'jpeg'}"
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._standards_prompt()},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}},
                    ],
                }],
            )
        except (APIConnectionError, AuthenticationError, RateLimitError, OpenAIError) as e:
            logger.error("Standards extraction failed: %s: %s", type(e).__name__, e)
            return False, {}, f"{type(e).__name__}: {e}"

        text = response.choices[0].message.content or ""
        # Strip markdown code fences
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        try:
            parsed = json.loads(text.strip())
        except json.JSONDecodeError as e:
            return False, {"raw_response": text}, f"Could not parse JSON: {e}"
        if not isinstance(parsed, dict) or ("lc_standards" not in parsed and "sc_standards" not in parsed):
            return False, {"raw_response": text}, "Response did not contain lc_standards or sc_standards."
        return True, parsed, "OK"
