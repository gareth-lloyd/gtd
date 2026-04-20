from datetime import date, datetime

import pytest

from gtd_core.dates import parse_human_date, parse_human_datetime


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


class TestParseHumanDatetime:
    def test_none(self):
        assert parse_human_datetime(None) is None

    def test_empty_string(self):
        assert parse_human_datetime("") is None

    def test_already_datetime(self):
        dt = datetime(2026, 5, 1, 14, 30)
        assert parse_human_datetime(dt) is dt

    def test_date_promotes_to_midnight(self):
        d = date(2026, 5, 1)
        assert parse_human_datetime(d) == datetime(2026, 5, 1, 0, 0)

    def test_iso_date_string(self):
        assert parse_human_datetime("2026-05-01") == datetime(2026, 5, 1, 0, 0)

    def test_iso_datetime_string(self):
        assert parse_human_datetime("2026-05-01T14:30") == datetime(2026, 5, 1, 14, 30)

    def test_iso_datetime_with_seconds(self):
        assert parse_human_datetime("2026-05-01T14:30:00") == datetime(2026, 5, 1, 14, 30, 0)

    def test_in_n_hours(self):
        fixed = datetime(2026, 5, 1, 9, 0)
        result = parse_human_datetime("in 2 hours", now=lambda: fixed)
        assert result == datetime(2026, 5, 1, 11, 0)

    def test_nh_shorthand(self):
        fixed = datetime(2026, 5, 1, 9, 0)
        result = parse_human_datetime("3h", now=lambda: fixed)
        assert result == datetime(2026, 5, 1, 12, 0)

    def test_in_n_minutes(self):
        fixed = datetime(2026, 5, 1, 9, 0)
        result = parse_human_datetime("in 45 minutes", now=lambda: fixed)
        assert result == datetime(2026, 5, 1, 9, 45)

    def test_garbage_raises(self):
        with pytest.raises(ValueError, match="Could not parse"):
            parse_human_datetime("xyzzy not a date")

    def test_natural_language_date_promotes_to_midnight(self):
        result = parse_human_datetime("next thursday")
        assert result is not None
        assert result.hour == 0
        assert result.minute == 0
        assert result.weekday() == 3
