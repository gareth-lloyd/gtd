"""Natural-language date parsing for due dates and defer_until.

Wraps the dateparser library with a GTD-friendly API: accepts None,
date objects, ISO strings, or natural language ("next thursday",
"in 2 weeks", "end of month"). Always returns a date or None.
Prefers future dates since these are typically deadlines or defer targets.

dateparser doesn't handle every colloquial pattern (e.g. "next Thursday",
"end of month"), so we preprocess common GTD phrases before falling through.
"""

import re
from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import Any

import dateparser

_DATEPARSER_SETTINGS: dict[str, Any] = {
    "PREFER_DATES_FROM": "future",
    "RETURN_AS_TIMEZONE_AWARE": False,
}


def parse_human_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise TypeError(f"Expected date or string, got {type(value).__name__}")
    value = value.strip()
    if not value:
        return None
    # Fast path: ISO format
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        pass
    # Preprocess common phrases dateparser misses
    preprocessed = _preprocess(value)
    if isinstance(preprocessed, date):
        return preprocessed
    text = preprocessed or value
    # Natural language via dateparser
    result = dateparser.parse(text, settings=_DATEPARSER_SETTINGS)
    if result is not None:
        return result.date()
    raise ValueError(f"Could not parse date: {value!r}")


def _preprocess(text: str) -> str | date | None:
    """Handle common phrases that dateparser doesn't understand."""
    lower = text.lower().strip()
    today = date.today()

    # "next <weekday>" → strip "next " prefix; dateparser handles bare weekday
    # names with PREFER_DATES_FROM=future
    if re.match(r"^next\s+(mon|tue|wed|thu|fri|sat|sun)", lower):
        return lower.split(None, 1)[1]

    # "end of month" / "eom"
    if lower in ("end of month", "eom", "end of this month"):
        _, last_day = monthrange(today.year, today.month)
        return date(today.year, today.month, last_day)

    # "end of next month"
    if lower == "end of next month":
        if today.month == 12:
            y, m = today.year + 1, 1
        else:
            y, m = today.year, today.month + 1
        _, last_day = monthrange(y, m)
        return date(y, m, last_day)

    # "end of week" / "eow" → next Friday
    if lower in ("end of week", "eow", "end of this week"):
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        return today + timedelta(days=days_until_friday)

    # "Nw" / "Nd" shorthand (e.g. "2w" → "in 2 weeks", "3d" → "in 3 days")
    m = re.match(r"^(\d+)\s*([dwm])$", lower)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        if unit == "d":
            return today + timedelta(days=n)
        if unit == "w":
            return today + timedelta(weeks=n)
        if unit == "m":
            from dateutil.relativedelta import relativedelta

            return today + relativedelta(months=n)

    return None
