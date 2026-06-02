"""Tests for src.standards."""
import pytest

from src.standards import LC_STANDARDS, SC_STANDARDS, lookup_standard


def test_tables_populated():
    assert len(LC_STANDARDS) == 17
    assert len(SC_STANDARDS) == 18  # SC has 100m IM, LC does not


@pytest.mark.parametrize("table", [LC_STANDARDS, SC_STANDARDS])
def test_required_columns_present(table):
    required = {"Event", "International Master", "National Master", "Level 1", "Level 2"}
    for row in table:
        assert required.issubset(row.keys()), f"missing keys in {row}"


def test_lookup_case_insensitive():
    row = lookup_standard("LC", "50m freestyle")
    assert row is not None
    assert row["National Master"] == "25.85"


def test_lookup_unknown_event():
    assert lookup_standard("LC", "75m underwater") is None


def test_lookup_unknown_course():
    assert lookup_standard("XX", "50m Freestyle") is None


def test_lc_does_not_have_100im_but_sc_does():
    assert lookup_standard("LC", "100m IM") is None
    assert lookup_standard("SC", "100m IM") is not None
