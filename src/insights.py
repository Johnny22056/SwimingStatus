"""Insight generation and analysis."""
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from src.models import SwimEvent
from src.validation import time_to_seconds
from src.storage import DataStore
from src.analytics import PerformanceAnalytics

logger = logging.getLogger(__name__)


class InsightGenerator:
    """Generates insights, potential assessments, and training suggestions."""

    @classmethod
    def generate_trend_insights(cls) -> List[Dict[str, Any]]:
        """Generate insights about performance trends across all stroke-distance groups.

        Returns:
            List of insight dicts with 'type' ('positive'/'warning'/'neutral'/'info')
            and 'message' keys. Returns a single info message if fewer than 2 events exist.
        """
        events = DataStore.load_swim_events()
        insights = []
        
        if len(events) < 2:
            return [{"type": "info", "message": "Add more race data to see trend insights."}]
        
        # Group by stroke-distance-course
        groups = defaultdict(list)
        for e in events:
            if e.time:
                key = (e.stroke, e.distance, e.course)
                groups[key].append(e)
        
        for key, group in groups.items():
            if len(group) < 2:
                continue
            
            group.sort(key=lambda x: x.date)
            first = group[0]
            last = group[-1]
            first_time = time_to_seconds(first.time)
            last_time = time_to_seconds(last.time)
            
            if first_time > 0 and last_time > 0:
                improvement = ((first_time - last_time) / first_time) * 100
                stroke, distance, course = key
                event_label = f"{stroke.title()} {distance}m ({course})"
                
                if improvement > 5:
                    insights.append({
                        "type": "positive",
                        "message": f"{event_label}: Improved by {improvement:.1f}% from {first.time} ({first.date}) to {last.time} ({last.date})",
                        "event": event_label,
                        "improvement_pct": round(improvement, 1),
                        "from_time": first.time,
                        "from_date": first.date,
                        "to_time": last.time,
                        "to_date": last.date,
                        "data_points": [first.date, last.date]
                    })
                elif improvement < -5:
                    insights.append({
                        "type": "warning",
                        "message": f"{event_label}: Declined by {abs(improvement):.1f}% from {first.time} ({first.date}) to {last.time} ({last.date})",
                        "event": event_label,
                        "improvement_pct": round(improvement, 1),
                        "from_time": first.time,
                        "from_date": first.date,
                        "to_time": last.time,
                        "to_date": last.date,
                        "data_points": [first.date, last.date]
                    })
                else:
                    insights.append({
                        "type": "neutral",
                        "message": f"{event_label}: Consistent performance around {last.time} over {len(group)} races",
                        "event": event_label,
                        "improvement_pct": round(improvement, 1),
                        "from_time": first.time,
                        "from_date": first.date,
                        "to_time": last.time,
                        "to_date": last.date,
                        "data_points": [e.date for e in group]
                    })
        
        return insights

    @classmethod
    def identify_strengths_weaknesses(cls) -> Dict[str, Any]:
        """Identify strongest and weakest strokes based on average pace.

        Returns:
            Dict with 'strongest', 'weakest', and 'stroke_paces' keys,
            or {'error': ...} if no data is available.
        """
        events = DataStore.load_swim_events()
        if not events:
            return {"error": "No data available"}
        
        stroke_times: Dict[str, List[float]] = defaultdict(list)
        for e in events:
            if e.time:
                stroke_times[e.stroke].append(time_to_seconds(e.time) / e.distance)
        
        if not stroke_times:
            return {"error": "No valid times found"}
        
        avg_pace: Dict[str, float] = {stroke: sum(times)/len(times) for stroke, times in stroke_times.items()}
        sorted_strokes: List[Tuple[str, float]] = sorted(avg_pace.items(), key=lambda x: x[1])
        
        return {
            "strongest": sorted_strokes[0][0] if sorted_strokes else None,
            "weakest": sorted_strokes[-1][0] if sorted_strokes else None,
            "stroke_paces": {k: f"{v:.3f} sec/m" for k, v in avg_pace.items()}
        }

    @classmethod
    def assess_potential(cls) -> Dict[str, Any]:
        """Assess swimming potential based on progression trends and strengths.

        Returns:
            Dict with 'total_races', 'positive_trends', 'trajectory', 'consistency',
            and 'recommendation' keys, or {'error': ...} if no data.
        """
        events = DataStore.load_swim_events()
        insights = cls.generate_trend_insights()
        strengths = cls.identify_strengths_weaknesses()
        
        if not events:
            return {"error": "No data available for assessment"}
        
        positive_trends = sum(1 for i in insights if i["type"] == "positive")
        total_events = len(events)
        
        assessment = {
            "total_races": total_events,
            "positive_trends": positive_trends,
            "strengths": strengths.get("strongest", "N/A"),
            "areas_for_improvement": strengths.get("weakest", "N/A"),
            "consistency": "High" if len(events) > 5 else "Building",
            "trajectory": "Improving" if positive_trends > 0 else "Steady",
            "recommendation": cls._generate_recommendation(strengths, insights)
        }
        return assessment

    @classmethod
    def _generate_recommendation(cls, strengths: Dict[str, Any], insights: List[Dict[str, Any]]) -> str:
        """Generate a training recommendation from strengths/weaknesses analysis.

        Args:
            strengths: Dict from identify_strengths_weaknesses.
            insights: List from generate_trend_insights.

        Returns:
            Human-readable recommendation string.
        """
        weakest = strengths.get("weakest")
        if weakest:
            return f"Focus training on {weakest} to balance stroke development. Consider drills specific to this stroke."
        return "Continue balanced training across all strokes."

    @classmethod
    def get_training_suggestions(cls) -> List[Dict[str, Any]]:
        """Generate prioritized training drill suggestions.

        Returns:
            List of suggestion dicts with 'focus', 'drills', and 'priority' keys.
            Highest-priority suggestion targets the weakest stroke.
        """
        strengths = cls.identify_strengths_weaknesses()
        suggestions = []
        
        weakest = strengths.get("weakest")
        if weakest:
            drill_map = {
                "freestyle": "Catch-up drill, fingertip drag, and bilateral breathing practice",
                "backstroke": "Single-arm backstroke, streamline kicking, and rotation drills",
                "breaststroke": "Pull-kick separation, sculling, and timing drills",
                "butterfly": "Single-arm butterfly, body dolphin, and breathing timing",
                "IM": "Transition practice and weak stroke focus sets"
            }
            suggestions.append({
                "focus": weakest,
                "drills": drill_map.get(weakest, "General technique drills"),
                "priority": "high"
            })
        
        # Add general suggestions
        suggestions.append({
            "focus": "General",
            "drills": "Endurance sets, starts and turns practice, and race pace training",
            "priority": "medium"
        })
        
        return suggestions
