"""Data models for swimming data analysis platform."""
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional, List


@dataclass
class SwimEvent:
    """Represents a single swimming event result."""
    date: str  # ISO format: YYYY-MM-DD
    meet_name: str
    stroke: str  # freestyle, backstroke, breaststroke, butterfly, IM
    distance: int  # in meters: 50, 100, 200, 400, 800, 1500
    time: str  # MM:SS.ss or SS.ss format
    splits: List[str] = field(default_factory=list)  # split times
    course: str = ""  # LC (long course) or SC (short course)
    round: str = ""  # heat, semifinal, final
    rank: int = 0
    age_group: str = ""  # e.g., "8 & Under", "9-10", "11-12"
    source_screenshot: str = ""  # path to source screenshot
    heat_lane: str = ""  # e.g., "H3 L4"
    swimmer_name: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SwimEvent":
        return cls(**data)


@dataclass
class BodyMetrics:
    """Represents body measurements at a point in time."""
    date: str  # ISO format: YYYY-MM-DD
    height_cm: float = 0.0
    weight_kg: float = 0.0
    arm_span_cm: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BodyMetrics":
        return cls(**data)

    @property
    def bmi(self) -> float:
        """Calculate BMI from height and weight."""
        if self.height_cm <= 0 or self.weight_kg <= 0:
            return 0.0
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)
