from datetime import date, datetime

from gtd_core.importer_nirvana import (
    clean_notes,
    gen_id,
    parse_date,
    parse_int,
    pick_timestamp,
    split_tags,
)
from gtd_core.models import EnvConfig
from gtd_core.service import slugify


class TestParseDate:
    def test_iso(self):
        assert parse_date("2024-08-11") == date(2024, 8, 11)

    def test_loose(self):
        assert parse_date("2024-8-11") == date(2024, 8, 11)

    def test_empty(self):
        assert parse_date("") is None
        assert parse_date(None) is None

    def test_garbage(self):
        assert parse_date("not a date") is None


class TestParseInt:
    def test_ok(self):
        assert parse_int("15") == 15

    def test_empty(self):
        assert parse_int("") is None
        assert parse_int(None) is None

    def test_garbage(self):
        assert parse_int("abc") is None


class TestPickTimestamp:
    def test_completed_preferred(self):
        row = {"COMPLETED": "2024-5-1", "DUEDATE": "2024-6-1", "STARTDATE": ""}
        assert pick_timestamp(row) == datetime(2024, 5, 1)

    def test_falls_back_to_due(self):
        row = {"COMPLETED": "", "DUEDATE": "2024-6-1", "STARTDATE": ""}
        assert pick_timestamp(row) == datetime(2024, 6, 1)

    def test_none_if_empty(self):
        row = {"COMPLETED": "", "DUEDATE": "", "STARTDATE": ""}
        assert pick_timestamp(row) is None


class TestSlugify:
    def test_strips_punctuation(self):
        assert slugify("Email Sarah — re: Q2 plans") == "email-sarah-re-q2-plans"


class TestGenId:
    def test_no_collision(self):
        used: set[str] = set()
        assert gen_id(datetime(2024, 1, 1), "Test", used) == "2024-01-01T0000-test"

    def test_collision_suffix(self):
        used = {"2024-01-01T0000-test"}
        assert gen_id(datetime(2024, 1, 1), "Test", used) == "2024-01-01T0000-test-2"
        used.add("2024-01-01T0000-test-2")
        assert gen_id(datetime(2024, 1, 1), "Test", used) == "2024-01-01T0000-test-3"


class TestSplitTags:
    def _cfg(self):
        return EnvConfig(
            name="work",
            contexts=["calls", "computer", "anywhere"],
            areas=["engineering"],
        )

    def test_known_contexts_promoted(self):
        row = {"TAGS": "calls, personal"}
        contexts, tags = split_tags(row, self._cfg(), env_name="work")
        assert contexts == ["calls"]
        assert tags == ["personal"]

    def test_env_name_stripped(self):
        row = {"TAGS": "work, computer, important"}
        contexts, tags = split_tags(row, self._cfg(), env_name="work")
        assert contexts == ["computer"]
        assert tags == ["important"]

    def test_empty(self):
        row = {"TAGS": ""}
        assert split_tags(row, self._cfg(), env_name="work") == ([], [])

    def test_dedups(self):
        row = {"TAGS": "calls, calls, personal"}
        contexts, tags = split_tags(row, self._cfg(), env_name="work")
        assert contexts == ["calls"]
        assert tags == ["personal"]

    def test_case_insensitive_context(self):
        row = {"TAGS": "Calls, Computer"}
        contexts, tags = split_tags(row, self._cfg(), env_name="work")
        assert contexts == ["calls", "computer"]  # canonical casing from config
        assert tags == []


class TestCleanNotes:
    def test_crlf_normalized(self):
        assert clean_notes("line1\r\nline2") == "line1\nline2"

    def test_strips(self):
        assert clean_notes("  content\n  ") == "content"

    def test_empty(self):
        assert clean_notes("") == ""
        assert clean_notes(None) == ""
