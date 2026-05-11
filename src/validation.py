"""Data validation utilities."""
import logging
import re
from datetime import datetime
from typing import Tuple, Optional
from src.config import TIME_FORMAT_MM_SS, TIME_FORMAT_SS

logger = logging.getLogger(__name__)


def validate_time_format(time_str: str) -> Tuple[bool, str]:
    """Validate swimming time format (MM:SS.ss or SS.ss).
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not time_str or not isinstance(time_str, str):
        return False, "Time cannot be empty"
    
    time_str = time_str.strip()
    
    if re.match(TIME_FORMAT_MM_SS, time_str):
        return True, ""
    if re.match(TIME_FORMAT_SS, time_str):
        return True, ""
    
    return False, f"Invalid time format: '{time_str}'. Expected MM:SS.ss or SS.ss"


def time_to_seconds(time_str: str) -> float:
    """Convert time string to total seconds.
    
    Args:
        time_str: Time in MM:SS.ss or SS.ss format
        
    Returns:
        Total seconds as float, or 0.0 on invalid input
    """
    if not isinstance(time_str, str):
        logger.warning("time_to_seconds: expected str, got %s", type(time_str).__name__)
        return 0.0

    time_str = time_str.strip()
    if not time_str:
        logger.warning("time_to_seconds: empty time string")
        return 0.0

    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) != 2:
            logger.warning("time_to_seconds: malformed time '%s' (multiple colons)", time_str)
            return 0.0
        try:
            minutes = float(parts[0])
            seconds = float(parts[1])
        except ValueError:
            logger.warning("time_to_seconds: non-numeric parts in '%s'", time_str)
            return 0.0
        return minutes * 60 + seconds
    else:
        try:
            return float(time_str)
        except ValueError:
            logger.warning("time_to_seconds: cannot parse '%s' as number", time_str)
            return 0.0


def seconds_to_time(total_seconds: float) -> str:
    """Convert total seconds to time string.
    
    Args:
        total_seconds: Total seconds as float
        
    Returns:
        Time string in MM:SS.ss or SS.ss format
    """
    if total_seconds < 0:
        logger.warning("seconds_to_time: negative value %.2f, returning '0.00'", total_seconds)
        return "0.00"

    if total_seconds >= 60:
        minutes = int(total_seconds // 60)
        seconds = total_seconds - (minutes * 60)
        return f"{minutes:02d}:{seconds:05.2f}"
    else:
        return f"{total_seconds:.2f}"


def validate_required_fields(data: dict, required: list) -> Tuple[bool, list]:
    """Validate that all required fields are present and non-empty.
    
    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing = []
    for field in required:
        if field not in data or data[field] is None or data[field] == "":
            missing.append(field)
    return len(missing) == 0, missing


def validate_swim_event_data(data: dict) -> Tuple[bool, list]:
    """Validate swim event data.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    required = ["date", "meet_name", "stroke", "distance", "time"]
    is_valid, missing = validate_required_fields(data, required)
    if not is_valid:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    
    # Validate time format
    if "time" in data and data["time"]:
        time_valid, time_error = validate_time_format(data["time"])
        if not time_valid:
            errors.append(time_error)
    
    # Validate splits if present
    if "splits" in data and data["splits"]:
        for i, split in enumerate(data["splits"]):
            split_valid, split_error = validate_time_format(split)
            if not split_valid:
                errors.append(f"Split {i+1}: {split_error}")
    
    return len(errors) == 0, errors


def validate_field_types(data: dict) -> Tuple[bool, list]:
    """Validate field types and basic constraints for swim event data.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # distance: must be int > 0
    distance = data.get("distance")
    if distance is not None:
        if not isinstance(distance, int):
            errors.append(f"distance must be an integer, got {type(distance).__name__}")
        elif distance <= 0:
            errors.append(f"distance must be > 0, got {distance}")

    # time: must be non-empty string matching time format
    time_val = data.get("time")
    if time_val is not None:
        if not isinstance(time_val, str) or not time_val.strip():
            errors.append("time must be a non-empty string")
        else:
            time_valid, time_error = validate_time_format(time_val)
            if not time_valid:
                errors.append(time_error)

    # stroke: must be a non-empty string
    stroke = data.get("stroke")
    if stroke is not None:
        if not isinstance(stroke, str) or not stroke.strip():
            errors.append("stroke must be a non-empty string")

    # date: must be a valid date string
    date_val = data.get("date")
    if date_val is not None:
        if not isinstance(date_val, str) or not date_val.strip():
            errors.append("date must be a non-empty string")
        else:
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except ValueError:
                errors.append(f"date must be in YYYY-MM-DD format, got '{date_val}'")

    # meet_name: must be a non-empty string
    meet_name = data.get("meet_name")
    if meet_name is not None:
        if not isinstance(meet_name, str) or not meet_name.strip():
            errors.append("meet_name must be a non-empty string")

    return len(errors) == 0, errors


def validate_body_metrics(height: float, weight: float) -> Tuple[bool, list]:
    """Validate body metric values are within reasonable ranges.
    
    Args:
        height: Height in centimeters
        weight: Weight in kilograms
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if height < 50 or height > 250:
        errors.append(f"height must be between 50-250 cm, got {height}")

    if weight < 10 or weight > 200:
        errors.append(f"weight must be between 10-200 kg, got {weight}")

    return len(errors) == 0, errors
