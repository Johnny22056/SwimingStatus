"""Performance analytics and visualization utilities."""
import logging
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go

from src.validation import time_to_seconds
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
    def get_time_development_data(cls) -> Dict[Tuple[str, int], List[Dict[str, Any]]]:
        """Get time progression data grouped by stroke+distance.

        Returns:
            Dict mapping (stroke, distance) tuples to lists of records
            sorted by date. Only groups with more than 2 records are included.
            Each record has 'date', 'time_seconds', 'time', and 'label' keys.
        """
        events = DataStore.load_swim_events()
        if not events:
            return {}

        # Group by (stroke, distance)
        groups: Dict[Tuple[str, int], List[Dict[str, Any]]] = defaultdict(list)
        for e in events:
            if not e.time or not e.stroke or not e.distance:
                continue
            time_sec = time_to_seconds(e.time)
            if time_sec <= 0:
                continue
            groups[(e.stroke, e.distance)].append({
                "date": e.date,
                "time_seconds": time_sec,
                "time": e.time,
                "label": f"{e.stroke.title()} {e.distance}m",
                "course": e.course if e.course else "",
            })

        # Filter to groups with > 2 records and sort each group by date
        result = {}
        for key, records in groups.items():
            if len(records) > 2:
                result[key] = sorted(records, key=lambda r: r["date"])
        return result

    @classmethod
    def get_time_development_insights(cls) -> Dict[str, Any]:
        """Generate insights from time development data.

        Returns:
            Dict with keys:
            - 'most_improved': (label, improvement_seconds) or None
            - 'most_consistent': (label, variance) or None
            - 'trends': list of dicts with 'label', 'direction', 'improvement' per group
        """
        data = cls.get_time_development_data()
        if not data:
            return {"most_improved": None, "most_consistent": None, "trends": []}

        most_improved = None
        best_improvement = 0.0
        most_consistent = None
        lowest_variance = float("inf")
        trends = []

        for (stroke, distance), records in data.items():
            label = f"{stroke.title()} {distance}m"

            # Improvement: time decrease from first to last record
            first_time = records[0]["time_seconds"]
            last_time = records[-1]["time_seconds"]
            improvement = first_time - last_time  # positive = improved

            if improvement > best_improvement:
                best_improvement = improvement
                most_improved = (label, round(improvement, 2))

            # Variance of time_seconds
            times = [r["time_seconds"] for r in records]
            mean = sum(times) / len(times)
            variance = sum((t - mean) ** 2 for t in times) / len(times)

            if variance < lowest_variance:
                lowest_variance = variance
                most_consistent = (label, round(variance, 4))

            # Trend direction
            if improvement > 0.5:
                direction = "improving"
            elif improvement < -0.5:
                direction = "declining"
            else:
                direction = "stable"

            trends.append({
                "label": label,
                "direction": direction,
                "improvement": round(improvement, 2),
                "first_time": records[0]["time"],
                "last_time": records[-1]["time"],
            })

        return {
            "most_improved": most_improved,
            "most_consistent": most_consistent,
            "trends": trends,
        }

    @classmethod
    def generate_html_report(cls) -> str:
        """Generate a self-contained HTML report with PBs and time development charts.

        Returns:
            Complete HTML string that can be saved as a standalone file.
            Includes inline CSS and Plotly JS via CDN for interactive charts.
        """
        from datetime import datetime as _dt

        events = DataStore.load_swim_events()
        generation_date = _dt.now().strftime("%Y-%m-%d %H:%M")

        # --- Build PB tables ---
        def _pb_table_rows(course_filter: str) -> str:
            """Return HTML <tr> rows for personal bests of a given course."""
            pb_dict: Dict[tuple, dict] = {}
            for e in events:
                if not e.time or not e.stroke or not e.distance:
                    continue
                if e.course != course_filter:
                    continue
                time_sec = time_to_seconds(e.time)
                if time_sec <= 0:
                    continue
                key = (e.stroke, e.distance)
                if key not in pb_dict or time_sec < pb_dict[key]["time_seconds"]:
                    pb_dict[key] = {
                        "stroke": e.stroke,
                        "distance": e.distance,
                        "time": e.time,
                        "time_seconds": time_sec,
                        "date": e.date,
                        "meet_name": e.meet_name,
                    }
            rows = []
            for pb in sorted(pb_dict.values(), key=lambda x: (x["stroke"], x["distance"])):
                rows.append(
                    f"<tr><td>{pb['stroke'].title()}</td>"
                    f"<td>{pb['distance']}m</td>"
                    f"<td>{pb['time']}</td>"
                    f"<td>{pb['date']}</td>"
                    f"<td>{pb['meet_name']}</td></tr>"
                )
            return "\n".join(rows)

        sc_rows = _pb_table_rows("SC")
        lc_rows = _pb_table_rows("LC")

        # --- Build Plotly time development charts ---
        dev_data = cls.get_time_development_data()
        chart_html_parts: list = []
        if dev_data:
            for (stroke, distance), records in sorted(dev_data.items()):
                label = f"{stroke.title()} {distance}m"
                dates = [r["date"] for r in records]
                times_sec = [r["time_seconds"] for r in records]
                time_labels = [r["time"] for r in records]
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, y=times_sec,
                    mode="lines+markers",
                    name=label,
                    line_shape="spline",
                    customdata=time_labels,
                    hovertemplate=(
                        f"{label}<br>"
                        "Date: %{x}<br>"
                        "Time: %{customdata}<extra></extra>"
                    ),
                ))
                fig.update_layout(
                    title=label,
                    yaxis_title="Time (seconds)",
                    xaxis_title="Date",
                    yaxis_autorange="reversed",
                    margin=dict(l=60, r=30, t=50, b=50),
                    height=350,
                )
                chart_html_parts.append(
                    fig.to_html(include_plotlyjs="cdn", full_html=False)
                )

        charts_section = "\n".join(chart_html_parts) if chart_html_parts else "<p><em>No time development data available yet.</em></p>"

        # --- Assemble HTML ---
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sunny's Swimming Analytics Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #f5f7fa; color: #333; padding: 2rem; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  h1 {{ text-align: center; color: #1a73e8; margin-bottom: 0.25rem; }}
  .subtitle {{ text-align: center; color: #666; margin-bottom: 2rem; font-size: 0.9rem; }}
  h2 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 0.3rem;
       margin: 2rem 0 1rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem;
          background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  th, td {{ padding: 0.6rem 0.8rem; text-align: left; border-bottom: 1px solid #e0e0e0; }}
  th {{ background: #1a73e8; color: #fff; font-weight: 600; }}
  tr:nth-child(even) {{ background: #f0f4ff; }}
  tr:hover {{ background: #e8edf7; }}
  .chart-card {{ background: #fff; padding: 1rem; margin-bottom: 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 6px; }}
  .empty {{ color: #999; font-style: italic; padding: 1rem; }}
</style>
</head>
<body>
<div class="container">
  <h1>🏊 Sunny's Swimming Analytics Report</h1>
  <p class="subtitle">Generated on {generation_date}</p>

  <h2>Short Course Personal Bests</h2>
  {f'<table><tr><th>Stroke</th><th>Distance</th><th>Time</th><th>Date</th><th>Meet</th></tr>{sc_rows}</table>' if sc_rows else '<p class="empty">No short course records yet.</p>'}

  <h2>Long Course Personal Bests</h2>
  {f'<table><tr><th>Stroke</th><th>Distance</th><th>Time</th><th>Date</th><th>Meet</th></tr>{lc_rows}</table>' if lc_rows else '<p class="empty">No long course records yet.</p>'}

  <h2>Time Development</h2>
  <div class="chart-card">
    {charts_section}
  </div>
</div>
</body>
</html>"""
        return html

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
