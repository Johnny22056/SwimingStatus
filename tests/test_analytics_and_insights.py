"""Tests for src.analytics and src.insights."""
from pathlib import Path

import pytest

from src.models import SwimEvent


@pytest.fixture
def fake_events(monkeypatch):
    """Patch DataStore.load_swim_events to return a controlled fixture set."""
    events = [
        SwimEvent(date="2024-01-15", meet_name="Open A", stroke="freestyle",
                  distance=100, time="1:05.00", course="LC"),
        SwimEvent(date="2024-04-20", meet_name="Open B", stroke="freestyle",
                  distance=100, time="1:02.50", course="LC"),
        SwimEvent(date="2024-09-12", meet_name="Open C", stroke="freestyle",
                  distance=100, time="1:00.00", course="LC"),
        SwimEvent(date="2024-02-10", meet_name="Open A", stroke="backstroke",
                  distance=100, time="1:15.00", course="SC"),
        SwimEvent(date="2024-06-15", meet_name="Open B", stroke="backstroke",
                  distance=100, time="1:14.50", course="SC"),
        # 50m fly: only 2 records — should be excluded from time-development (requires > 2)
        SwimEvent(date="2024-03-01", meet_name="Open A", stroke="butterfly",
                  distance=50, time="32.00", course="LC"),
        SwimEvent(date="2024-08-01", meet_name="Open B", stroke="butterfly",
                  distance=50, time="31.50", course="LC"),
    ]
    monkeypatch.setattr("src.storage.DataStore.load_swim_events", classmethod(lambda cls: list(events)))
    monkeypatch.setattr("src.analytics.DataStore.load_swim_events", classmethod(lambda cls: list(events)))
    monkeypatch.setattr("src.insights.DataStore.load_swim_events", classmethod(lambda cls: list(events)))
    return events


class TestPersonalBests:
    def test_picks_fastest_per_group(self, fake_events):
        from src.analytics import PerformanceAnalytics
        pb_df = PerformanceAnalytics.get_personal_bests()
        free100 = pb_df[(pb_df["stroke"] == "freestyle") & (pb_df["distance"] == 100) & (pb_df["course"] == "LC")]
        assert len(free100) == 1
        assert free100.iloc[0]["time"] == "1:00.00"

    def test_separates_by_course(self, fake_events):
        from src.analytics import PerformanceAnalytics
        pb_df = PerformanceAnalytics.get_personal_bests()
        sc_back = pb_df[(pb_df["stroke"] == "backstroke") & (pb_df["course"] == "SC")]
        assert len(sc_back) == 1


class TestTimeDevelopment:
    def test_filters_groups_with_too_few_records(self, fake_events):
        from src.analytics import PerformanceAnalytics
        dev = PerformanceAnalytics.get_time_development_data()
        # freestyle 100m has 3 records → included
        assert ("freestyle", 100) in dev
        # backstroke 100m has 2 → excluded (> 2 required)
        assert ("backstroke", 100) not in dev
        # butterfly 50m has 2 → excluded
        assert ("butterfly", 50) not in dev

    def test_records_sorted_by_date(self, fake_events):
        from src.analytics import PerformanceAnalytics
        dev = PerformanceAnalytics.get_time_development_data()
        records = dev[("freestyle", 100)]
        assert [r["date"] for r in records] == sorted(r["date"] for r in records)


class TestDashboardSummary:
    def test_counts(self, fake_events):
        from src.analytics import PerformanceAnalytics
        summary = PerformanceAnalytics.get_dashboard_summary()
        assert summary["total_events"] == 7
        assert summary["total_meets"] == 3
        assert set(summary["strokes"]) == {"backstroke", "butterfly", "freestyle"}


class TestInsights:
    def test_trend_insights_detect_improvement(self, fake_events):
        from src.insights import InsightGenerator
        insights = InsightGenerator.generate_trend_insights()
        positives = [i for i in insights if i["type"] == "positive"]
        # The freestyle 100m LC group went from 65.00s → 60.00s (~7.7% improvement)
        assert any("Freestyle 100m" in i["message"] for i in positives)

    def test_strengths_weaknesses(self, fake_events):
        from src.insights import InsightGenerator
        sw = InsightGenerator.identify_strengths_weaknesses()
        assert sw["strongest"] in {"freestyle", "backstroke", "butterfly"}
        assert sw["weakest"] in {"freestyle", "backstroke", "butterfly"}

    def test_html_report_escapes_data(self, monkeypatch):
        """A meet name containing <script> must not appear unescaped in the report."""
        events = [
            SwimEvent(date="2024-01-15", meet_name="<script>alert(1)</script>",
                      stroke="freestyle", distance=50, time="30.00", course="LC"),
        ]
        monkeypatch.setattr("src.storage.DataStore.load_swim_events", classmethod(lambda cls: events))
        monkeypatch.setattr("src.analytics.DataStore.load_swim_events", classmethod(lambda cls: events))
        from src.analytics import PerformanceAnalytics
        html = PerformanceAnalytics.generate_html_report()
        assert "<script>alert(1)</script>" not in html
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
