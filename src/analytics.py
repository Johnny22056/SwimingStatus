"""Performance analytics and visualization utilities."""
import logging
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.models import SwimEvent
from src.validation import time_to_seconds, seconds_to_time
from src.storage import DataStore

logger = logging.getLogger(__name__)


class PerformanceAnalytics:
    """Analyzes swimming performance data and generates visualizations."""

    @staticmethod
    def get_events_df() -> pd.DataFrame:
        """Load swim events as a pandas DataFrame.

        Returns:
            DataFrame with event data including a 'time_seconds' column,
            or an empty DataFrame if no events exist.
        """
        events = DataStore.load_swim_events()
        if not events:
            return pd.DataFrame()
        data = []
        for e in events:
            d = e.to_dict()
            d["time_seconds"] = time_to_seconds(e.time) if e.time else 0
            d["date"] = pd.to_datetime(e.date)
            data.append(d)
        return pd.DataFrame(data)

    @classmethod
    def get_time_progression(cls, stroke: Optional[str] = None, distance: Optional[int] = None) -> pd.DataFrame:
        """Get time progression data for a specific stroke and distance.

        Args:
            stroke: Optional stroke filter (e.g., 'freestyle').
            distance: Optional distance filter in meters.

        Returns:
            Filtered DataFrame sorted by date, or empty DataFrame.
        """
        df = cls.get_events_df()
        if df.empty:
            return df
        if stroke:
            df = df[df["stroke"] == stroke]
        if distance:
            df = df[df["distance"] == distance]
        return df.sort_values("date")

    @classmethod
    def create_time_progression_chart(cls, stroke: str, distance: int) -> go.Figure:
        """Create a line chart showing time progression for a stroke/distance.

        Args:
            stroke: Stroke name to filter by.
            distance: Distance in meters to filter by.

        Returns:
            Plotly line Figure with reversed y-axis (faster at top),
            or empty Figure if no data matches.
        """
        df = cls.get_time_progression(stroke, distance)
        if df.empty:
            return go.Figure()
        
        fig = px.line(
            df, x="date", y="time_seconds",
            title=f"{stroke.title()} {distance}m - Time Progression",
            labels={"time_seconds": "Time (seconds)", "date": "Date"},
            markers=True
        )
        fig.update_layout(
            yaxis_autorange="reversed",  # Faster times at top
            hovertemplate="Date: %{x}<br>Time: %{customdata}<extra></extra>"
        )
        fig.update_traces(customdata=df["time"])
        return fig

    @classmethod
    def get_stroke_comparison_data(cls) -> pd.DataFrame:
        """Get average times per stroke for radar chart comparison.

        Returns:
            DataFrame with 'stroke', 'average_time', and 'count' columns,
            or empty DataFrame if no events exist.
        """
        events = DataStore.load_swim_events()
        if not events:
            return pd.DataFrame()
        
        # Group by stroke and get best times
        stroke_bests = {}
        for e in events:
            if not e.time:
                continue
            key = e.stroke
            if key not in stroke_bests:
                stroke_bests[key] = []
            stroke_bests[key].append(time_to_seconds(e.time))
        
        # Calculate average performance (lower is better, so invert for radar)
        data = []
        for stroke, times in stroke_bests.items():
            avg_time = sum(times) / len(times)
            data.append({
                "stroke": stroke,
                "average_time": avg_time,
                "count": len(times)
            })
        return pd.DataFrame(data)

    @classmethod
    def create_stroke_radar_chart(cls) -> go.Figure:
        """Create radar chart comparing relative stroke performance.

        Returns:
            Plotly polar Figure where higher score = better relative performance,
            or empty Figure if no comparison data exists.
        """
        df = cls.get_stroke_comparison_data()
        if df.empty:
            return go.Figure()
        
        # Normalize: invert so faster = higher score
        max_time = df["average_time"].max()
        df["score"] = max_time / df["average_time"] * 100
        
        fig = go.Figure(data=go.Scatterpolar(
            r=df["score"].tolist() + [df["score"].iloc[0]],
            theta=df["stroke"].tolist() + [df["stroke"].iloc[0]],
            fill='toself',
            name='Performance Score'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Stroke Comparison (Higher = Better Relative Performance)"
        )
        return fig

    @classmethod
    def get_personal_bests(cls) -> pd.DataFrame:
        """Get personal best times for each stroke-distance-course combination.

        Returns:
            DataFrame with best-time rows keyed by (stroke, distance, course),
            or empty DataFrame if no events exist.
        """
        events = DataStore.load_swim_events()
        if not events:
            return pd.DataFrame()
        
        pb_dict = {}
        for e in events:
            if not e.time:
                continue
            key = (e.stroke, e.distance, e.course)
            time_sec = time_to_seconds(e.time)
            if key not in pb_dict or time_sec < pb_dict[key]["time_seconds"]:
                pb_dict[key] = {
                    "stroke": e.stroke,
                    "distance": e.distance,
                    "course": e.course,
                    "time": e.time,
                    "time_seconds": time_sec,
                    "date": e.date,
                    "meet_name": e.meet_name
                }
        
        return pd.DataFrame(list(pb_dict.values()))

    @classmethod
    def get_age_adjusted_performance(cls) -> pd.DataFrame:
        """Calculate improvement rate per stroke-distance-course event group.

        Returns:
            DataFrame with 'event', 'first_time', 'last_time', 'improvement_percent',
            'num_races', 'stroke', 'distance' columns; only groups with 2+ races
            are included. Empty DataFrame if no data.
        """
        df = cls.get_events_df()
        if df.empty:
            return df
        
        # Group by stroke, distance, course
        df["event_key"] = df["stroke"] + "_" + df["distance"].astype(str) + "m_" + df["course"]
        
        # Calculate improvement rate
        results = []
        for key, group in df.groupby("event_key"):
            group = group.sort_values("date")
            if len(group) < 2:
                continue
            first_time = group.iloc[0]["time_seconds"]
            last_time = group.iloc[-1]["time_seconds"]
            improvement = ((first_time - last_time) / first_time * 100) if first_time > 0 else 0
            
            results.append({
                "event": key,
                "first_time": group.iloc[0]["time"],
                "last_time": group.iloc[-1]["time"],
                "improvement_percent": round(improvement, 2),
                "num_races": len(group),
                "stroke": group.iloc[0]["stroke"],
                "distance": group.iloc[0]["distance"]
            })
        return pd.DataFrame(results)

    @classmethod
    def get_dashboard_summary(cls) -> Dict[str, Any]:
        """Get summary statistics for the dashboard.

        Returns:
            Dict with 'total_meets', 'total_events', 'personal_bests',
            'strokes', and 'latest_event' keys.
        """
        events = DataStore.load_swim_events()
        pb_df = cls.get_personal_bests()
        
        return {
            "total_meets": len(set(e.meet_name for e in events)),
            "total_events": len(events),
            "personal_bests": len(pb_df),
            "strokes": sorted(list(set(e.stroke for e in events))),
            "latest_event": events[-1].date if events else None
        }
