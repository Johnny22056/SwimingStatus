"""Tests for src.validation."""
import pytest

from src.validation import (
    seconds_to_time,
    time_to_seconds,
    validate_body_metrics,
    validate_field_types,
    validate_required_fields,
    validate_swim_event_data,
    validate_time_format,
)


class TestValidateTimeFormat:
    @pytest.mark.parametrize("time_str", ["1:23.45", "12:34.56", "9.99", "59.99", "1:00.00"])
    def test_accepts_valid(self, time_str):
        ok, err = validate_time_format(time_str)
        assert ok, err

    @pytest.mark.parametrize("time_str", ["", "abc", "1:2:3.45", "12:3.4", "12:34", "1.234", ":12.34"])
    def test_rejects_invalid(self, time_str):
        ok, err = validate_time_format(time_str)
        assert not ok
        assert err

    def test_rejects_non_string(self):
        ok, _ = validate_time_format(None)  # type: ignore[arg-type]
        assert not ok

    def test_trims_whitespace(self):
        ok, _ = validate_time_format("  1:23.45  ")
        assert ok


class TestTimeToSeconds:
    @pytest.mark.parametrize("text,expected", [
        ("1:23.45", 83.45),
        ("0:30.00", 30.00),
        ("45.67", 45.67),
        ("12:34.56", 754.56),
    ])
    def test_parses(self, text, expected):
        assert time_to_seconds(text) == pytest.approx(expected, abs=1e-6)

    @pytest.mark.parametrize("text", ["", "abc", "1:2:3", "1::23"])
    def test_returns_zero_on_garbage(self, text):
        assert time_to_seconds(text) == 0.0

    def test_handles_non_string(self):
        assert time_to_seconds(None) == 0.0  # type: ignore[arg-type]


class TestSecondsToTime:
    @pytest.mark.parametrize("secs,expected", [
        (59.99, "59.99"),
        (0.00, "0.00"),
        (60.00, "01:00.00"),
        (83.45, "01:23.45"),
        (3599.99, "59:59.99"),
    ])
    def test_formats(self, secs, expected):
        assert seconds_to_time(secs) == expected

    def test_negative_returns_zero(self):
        assert seconds_to_time(-1.0) == "0.00"

    def test_roundtrip(self):
        # The MM:SS.ss format must roundtrip through both directions
        for raw in ["1:23.45", "59.99", "5:00.00"]:
            assert seconds_to_time(time_to_seconds(raw)) in (raw, raw.zfill(8))


class TestValidateRequiredFields:
    def test_all_present(self):
        ok, missing = validate_required_fields({"a": 1, "b": "x"}, ["a", "b"])
        assert ok and missing == []

    def test_reports_missing(self):
        ok, missing = validate_required_fields({"a": 1, "b": ""}, ["a", "b", "c"])
        assert not ok
        assert sorted(missing) == ["b", "c"]


class TestValidateSwimEventData:
    def _full(self, **overrides):
        base = {
            "date": "2024-01-15",
            "meet_name": "Spring Open",
            "stroke": "freestyle",
            "distance": 100,
            "time": "1:02.34",
        }
        base.update(overrides)
        return base

    def test_full_payload_passes(self):
        ok, errs = validate_swim_event_data(self._full())
        assert ok and errs == []

    def test_missing_required(self):
        ok, errs = validate_swim_event_data({"stroke": "freestyle"})
        assert not ok
        assert any("required" in e.lower() for e in errs)

    def test_bad_time_rejected(self):
        ok, errs = validate_swim_event_data(self._full(time="not-a-time"))
        assert not ok
        assert any("time" in e.lower() for e in errs)

    def test_bad_split_rejected(self):
        ok, errs = validate_swim_event_data(self._full(splits=["32.10", "abc"]))
        assert not ok
        assert any("split" in e.lower() for e in errs)


class TestValidateFieldTypes:
    def test_distance_must_be_positive_int(self):
        ok, errs = validate_field_types({"distance": 0})
        assert not ok and any("distance" in e for e in errs)
        ok, errs = validate_field_types({"distance": "100"})
        assert not ok and any("integer" in e for e in errs)
        ok, errs = validate_field_types({"distance": 100})
        assert ok

    def test_date_format(self):
        ok, errs = validate_field_types({"date": "2024-13-01"})
        assert not ok and any("date" in e.lower() for e in errs)


class TestValidateBodyMetrics:
    def test_valid_range(self):
        ok, errs = validate_body_metrics(150.0, 45.0)
        assert ok and errs == []

    @pytest.mark.parametrize("h,w", [(40, 50), (300, 50), (150, 5), (150, 250)])
    def test_out_of_range(self, h, w):
        ok, _ = validate_body_metrics(h, w)
        assert not ok
