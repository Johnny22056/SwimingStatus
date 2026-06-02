"""Chinese Female National Swimming Standards (Effective 2025-01-01).

Source: Chinese Swimming Association. Times stored as the strings shown in
the official tables (MM:SS.ss or SS.ss).
"""
from typing import Dict, List, Optional

LC_STANDARDS: List[Dict[str, str]] = [
    {"Event": "50m Freestyle", "International Master": "24.70", "National Master": "25.85", "Level 1": "27.20", "Level 2": "31.50"},
    {"Event": "100m Freestyle", "International Master": "53.61", "National Master": "56.30", "Level 1": "1:02.50", "Level 2": "1:13.00"},
    {"Event": "200m Freestyle", "International Master": "1:57.26", "National Master": "2:01.20", "Level 1": "2:15.00", "Level 2": "2:39.00"},
    {"Event": "400m Freestyle", "International Master": "4:07.90", "National Master": "4:15.80", "Level 1": "4:44.00", "Level 2": "5:40.00"},
    {"Event": "800m Freestyle", "International Master": "8:29.17", "National Master": "8:53.40", "Level 1": "9:42.00", "Level 2": "10:57.00"},
    {"Event": "1500m Freestyle", "International Master": "16:09.09", "National Master": "17:14.00", "Level 1": "18:35.00", "Level 2": "20:49.00"},
    {"Event": "50m Backstroke", "International Master": "28.22", "National Master": "30.55", "Level 1": "33.00", "Level 2": "38.50"},
    {"Event": "100m Backstroke", "International Master": "59.99", "National Master": "1:04.30", "Level 1": "1:09.00", "Level 2": "1:21.00"},
    {"Event": "200m Backstroke", "International Master": "2:10.39", "National Master": "2:18.30", "Level 1": "2:29.50", "Level 2": "2:53.00"},
    {"Event": "50m Breaststroke", "International Master": "31.02", "National Master": "31.70", "Level 1": "36.00", "Level 2": "41.00"},
    {"Event": "100m Breaststroke", "International Master": "1:06.79", "National Master": "1:10.75", "Level 1": "1:18.00", "Level 2": "1:27.00"},
    {"Event": "200m Breaststroke", "International Master": "2:23.91", "National Master": "2:36.60", "Level 1": "2:51.00", "Level 2": "3:13.00"},
    {"Event": "50m Butterfly", "International Master": "26.32", "National Master": "27.50", "Level 1": "30.50", "Level 2": "36.50"},
    {"Event": "100m Butterfly", "International Master": "57.92", "National Master": "1:00.50", "Level 1": "1:08.00", "Level 2": "1:20.00"},
    {"Event": "200m Butterfly", "International Master": "2:08.85", "National Master": "2:14.20", "Level 1": "2:25.00", "Level 2": "2:54.50"},
    {"Event": "200m IM", "International Master": "2:11.47", "National Master": "2:18.40", "Level 1": "2:30.00", "Level 2": "2:58.00"},
    {"Event": "400m IM", "International Master": "4:38.53", "National Master": "4:56.80", "Level 1": "5:18.00", "Level 2": "6:21.00"},
]

SC_STANDARDS: List[Dict[str, str]] = [
    {"Event": "50m Freestyle", "International Master": "24.44", "National Master": "25.00", "Level 1": "26.40", "Level 2": "30.50"},
    {"Event": "100m Freestyle", "International Master": "52.85", "National Master": "54.70", "Level 1": "1:00.50", "Level 2": "1:11.00"},
    {"Event": "200m Freestyle", "International Master": "1:55.60", "National Master": "1:58.50", "Level 1": "2:12.00", "Level 2": "2:35.00"},
    {"Event": "400m Freestyle", "International Master": "4:06.95", "National Master": "4:11.40", "Level 1": "4:39.00", "Level 2": "5:35.00"},
    {"Event": "800m Freestyle", "International Master": "8:26.71", "National Master": "8:45.20", "Level 1": "9:33.00", "Level 2": "10:47.00"},
    {"Event": "1500m Freestyle", "International Master": "16:15.27", "National Master": "17:00.50", "Level 1": "18:20.00", "Level 2": "20:32.00"},
    {"Event": "50m Backstroke", "International Master": "26.54", "National Master": "28.70", "Level 1": "31.00", "Level 2": "36.20"},
    {"Event": "100m Backstroke", "International Master": "58.08", "National Master": "1:01.55", "Level 1": "1:06.00", "Level 2": "1:17.50"},
    {"Event": "200m Backstroke", "International Master": "2:05.54", "National Master": "2:13.60", "Level 1": "2:24.50", "Level 2": "2:47.00"},
    {"Event": "50m Breaststroke", "International Master": "30.45", "National Master": "30.85", "Level 1": "34.70", "Level 2": "40.00"},
    {"Event": "100m Breaststroke", "International Master": "1:05.28", "National Master": "1:08.75", "Level 1": "1:15.80", "Level 2": "1:24.50"},
    {"Event": "200m Breaststroke", "International Master": "2:23.38", "National Master": "2:33.60", "Level 1": "2:47.00", "Level 2": "3:08.80"},
    {"Event": "50m Butterfly", "International Master": "25.82", "National Master": "27.40", "Level 1": "30.40", "Level 2": "36.40"},
    {"Event": "100m Butterfly", "International Master": "57.40", "National Master": "59.00", "Level 1": "1:06.00", "Level 2": "1:18.00"},
    {"Event": "200m Butterfly", "International Master": "2:08.45", "National Master": "2:11.20", "Level 1": "2:22.00", "Level 2": "2:51.30"},
    {"Event": "100m IM", "International Master": "59.65", "National Master": "1:02.50", "Level 1": "1:07.40", "Level 2": "1:20.00"},
    {"Event": "200m IM", "International Master": "2:10.16", "National Master": "2:13.70", "Level 1": "2:25.00", "Level 2": "2:52.00"},
    {"Event": "400m IM", "International Master": "4:37.54", "National Master": "4:49.80", "Level 1": "5:10.00", "Level 2": "6:11.00"},
]


def lookup_standard(course: str, event_name: str) -> Optional[Dict[str, str]]:
    """Case-insensitive standard lookup by course ('LC'/'SC') and event name."""
    table = LC_STANDARDS if course.upper() == "LC" else SC_STANDARDS if course.upper() == "SC" else None
    if not table:
        return None
    target = event_name.strip().lower()
    return next((s for s in table if s["Event"].lower() == target), None)
