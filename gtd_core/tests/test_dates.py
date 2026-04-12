from datetime import date, datetime

import pytest

from gtd_core.dates import parse_human_date


class TestParseHumanDate:
    def test_none(self):
        assert parse_human_date(None) is None

    def test_empty_string(self):
        assert parse_human_date("") is None

    def test_already_date(self):
        d = date(2026, 5, 1)
        assert parse_human_date(d) is d

    def test_iso_string(self):
        assert parse_human_date("2026-05-01") == date(2026, 5, 1)

    def test_iso_datetime_string(self):
        assert parse_human_date("2026-05-01T10:00:00") == date(2026, 5, 1)

    def test_tomorrow(self):
        result = parse_human_date("tomorrow")
        assert result is not None
        assert result > date.today()

    def test_next_thursday(self):
        result = parse_human_date("next thursday")
        assert result is not None
        assert result > date.today()
        assert result.weekday() == 3  # Thursday

    def test_in_2_weeks(self):
        result = parse_human_date("in 2 weeks")
        assert result is not None
        assert result > date.today()

    def test_partial_month_day(self):
        result = parse_human_date("Apr 30")
        assert result is not None
        assert result.month == 4
        assert result.day == 30

    def test_end_of_month(self):
        result = parse_human_date("end of month")
        assert result is not None
        assert result >= date.today()

    def test_garbage_raises(self):
        with pytest.raises(ValueError, match="Could not parse"):
            parse_human_date("xyzzy not a date")

    def test_prefers_future(self):
        """Ambiguous dates should resolve to the future for due/defer use."""
        result = parse_human_date("friday")
        assert result is not None
        assert result >= date.today()

    def test_datetime_passthrough(self):
        dt = datetime(2026, 5, 1, 10, 30)
        assert parse_human_date(dt) == date(2026, 5, 1)
