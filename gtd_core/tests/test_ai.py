"""Unit tests for the pure functions in gtd_core/ai.py.

The CLI subprocess is never invoked here — we test the building blocks
(_build_prompt, _parse_response, _result_from_dict, recent_action_titles_by_project)
directly. End-to-end flow is covered by gtd_api/tests/test_capture_ai.py,
which mocks `subprocess.run`.
"""

from datetime import date, datetime

import pytest

import gtd_core.ai as ai_mod
from gtd_core.ai import (
    AiCaptureNoExtractionError,
    AiCaptureNotConfiguredError,
    AiCaptureResult,
    _build_prompt,
    _parse_response,
    _result_from_dict,
    ai_capture,
    recent_action_titles_by_project,
)
from gtd_core.models import EnvConfig, Item, Project


def _item(iid: str, title: str, project_id: str | None = None) -> Item:
    from gtd_core.models import Bucket

    return Item(
        id=iid,
        title=title,
        body="",
        created=datetime(2026, 4, 10, 9, 0),
        updated=datetime(2026, 4, 10, 9, 0),
        status=Bucket.NEXT,
        project=project_id,
    )


def _project(pid: str, title: str, **kwargs) -> Project:
    return Project(
        id=pid,
        title=title,
        body="",
        created=datetime(2026, 3, 1),
        updated=datetime(2026, 3, 1),
        **kwargs,
    )


# ---------------- _parse_response ----------------


class TestParseResponse:
    def test_plain_json_object(self):
        raw = '{"title": "Call dentist", "summary": "Added to inbox"}'
        result = _parse_response(raw)
        assert isinstance(result, AiCaptureResult)
        assert result.title == "Call dentist"
        assert result.summary == "Added to inbox"

    def test_strips_json_code_fences(self):
        raw = '```json\n{"title": "Buy milk", "summary": "Quick"}\n```'
        result = _parse_response(raw)
        assert result.title == "Buy milk"

    def test_strips_generic_code_fences(self):
        raw = '```\n{"title": "Thing", "summary": "ok"}\n```'
        result = _parse_response(raw)
        assert result.title == "Thing"

    def test_tolerates_whitespace(self):
        raw = '   \n\n  {"title": "Padded", "summary": "ok"}  \n\n  '
        result = _parse_response(raw)
        assert result.title == "Padded"

    def test_invalid_json_raises(self):
        with pytest.raises(AiCaptureNoExtractionError, match="valid JSON"):
            _parse_response("not json at all")

    def test_json_array_raises(self):
        # Parseable JSON but not a dict.
        with pytest.raises(AiCaptureNoExtractionError, match="title"):
            _parse_response("[1, 2, 3]")

    def test_missing_title_raises(self):
        with pytest.raises(AiCaptureNoExtractionError, match="title"):
            _parse_response('{"summary": "no title here"}')

    def test_raw_snippet_in_error_message(self):
        with pytest.raises(AiCaptureNoExtractionError, match="garbage"):
            _parse_response("garbage " * 30)


# ---------------- _result_from_dict ----------------


class TestResultFromDict:
    def test_full_payload(self):
        result = _result_from_dict(
            {
                "title": "Call Blake",
                "summary": "Filed to People",
                "body": "Ring him after lunch.",
                "energy": "low",
                "time_minutes": 5,
                "contexts": ["calls"],
                "area": "engineering",
                "project_query": "People",
                "due": "tomorrow",
                "defer_until": "eod",
            }
        )
        assert result.title == "Call Blake"
        assert result.summary == "Filed to People"
        assert result.body == "Ring him after lunch."
        assert result.energy == "low"
        assert result.time_minutes == 5
        assert result.contexts == ["calls"]
        assert result.area == "engineering"
        assert result.project_query == "People"
        assert result.due == "tomorrow"
        assert result.defer_until == "eod"

    def test_missing_optionals_default_none(self):
        result = _result_from_dict({"title": "Bare"})
        assert result.title == "Bare"
        assert result.body is None
        assert result.energy is None
        assert result.time_minutes is None
        assert result.contexts is None
        assert result.area is None
        assert result.project_query is None
        assert result.due is None
        assert result.defer_until is None

    def test_summary_default_when_missing(self):
        result = _result_from_dict({"title": "Buy milk"})
        assert result.summary == 'Added "Buy milk" to inbox'

    def test_time_minutes_string_coerced_to_none(self):
        # Defensive: the model sometimes returns strings where ints are expected.
        result = _result_from_dict({"title": "X", "time_minutes": "15"})
        assert result.time_minutes is None

    def test_contexts_non_list_coerced_to_none(self):
        result = _result_from_dict({"title": "X", "contexts": "calls"})
        assert result.contexts is None

    def test_whitespace_only_optionals_normalise_to_none(self):
        result = _result_from_dict(
            {
                "title": "X",
                "body": "   ",
                "area": "\t\n",
                "due": "",
            }
        )
        assert result.body is None
        assert result.area is None
        assert result.due is None

    def test_title_trimmed(self):
        result = _result_from_dict({"title": "  spaced  "})
        assert result.title == "spaced"


# ---------------- _build_prompt ----------------


class TestBuildPrompt:
    def _cfg(self, contexts=None, areas=None) -> EnvConfig:
        return EnvConfig(
            name="work",
            contexts=contexts if contexts is not None else ["calls", "computer"],
            areas=areas if areas is not None else ["engineering", "admin"],
        )

    def test_includes_today(self):
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(),
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        assert "Today: 2026-04-20" in prompt

    def test_includes_all_contexts_and_areas(self):
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(contexts=["calls", "computer", "errands"], areas=["eng", "ops"]),
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        assert "calls, computer, errands" in prompt
        assert "eng, ops" in prompt

    def test_empty_contexts_and_areas_sentinel(self):
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(contexts=[], areas=[]),
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        assert "Valid contexts: (none configured)" in prompt
        assert "Valid areas: (none configured)" in prompt

    def test_empty_projects_sentinel(self):
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(),
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        assert "(no active projects)" in prompt

    def test_project_full_row(self):
        p = _project("p1", "Launch blog", area="hobbies", outcome="3 posts live")
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(),
            projects=[p],
            sample_actions={"p1": ["Draft post", "Publish post"]},
            today=date(2026, 4, 20),
        )
        assert "- Launch blog" in prompt
        assert "(area: hobbies)" in prompt
        assert "— 3 posts live" in prompt
        assert 'Recent actions: "Draft post"; "Publish post"' in prompt

    def test_project_minimal_row(self):
        p = _project("p1", "Bare project")
        prompt = _build_prompt(
            text="x",
            cfg=self._cfg(),
            projects=[p],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        assert "- Bare project" in prompt
        # No area or outcome fragments
        assert "(area:" not in prompt
        # Sample actions omitted when empty
        assert "Recent actions:" not in prompt

    def test_user_input_included(self):
        prompt = _build_prompt(
            text="  ring blake re: meeting notes  ",
            cfg=self._cfg(),
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )
        # Input is stripped before being embedded
        assert "User input: ring blake re: meeting notes" in prompt


# ---------------- recent_action_titles_by_project ----------------


class TestRecentActionTitlesByProject:
    def test_caps_per_project(self):
        projects = [_project("p1", "P1")]
        items = [_item(f"i{n}", f"Action {n}", "p1") for n in range(5)]
        grouped = recent_action_titles_by_project(items, projects, per_project=3)
        assert grouped["p1"] == ["Action 0", "Action 1", "Action 2"]

    def test_skips_items_for_unknown_projects(self):
        projects = [_project("p1", "P1")]
        items = [
            _item("i1", "Keep", "p1"),
            _item("i2", "Skip", "p-not-in-projects"),
            _item("i3", "Orphan", None),
        ]
        grouped = recent_action_titles_by_project(items, projects)
        assert grouped == {"p1": ["Keep"]}

    def test_preserves_encounter_order(self):
        # Caller passes newest-first; we expect the output to mirror that.
        projects = [_project("p1", "P1")]
        items = [
            _item("newest", "Newest", "p1"),
            _item("middle", "Middle", "p1"),
            _item("oldest", "Oldest", "p1"),
        ]
        grouped = recent_action_titles_by_project(items, projects)
        assert grouped["p1"] == ["Newest", "Middle", "Oldest"]

    def test_empty_input(self):
        projects = [_project("p1", "P1"), _project("p2", "P2")]
        grouped = recent_action_titles_by_project([], projects)
        assert grouped == {"p1": [], "p2": []}

    def test_no_projects(self):
        grouped = recent_action_titles_by_project([_item("i1", "x", "p1")], projects=[])
        assert grouped == {}


# ---------------- GTD_AI_STUB_RESPONSE env seam ----------------


class TestAiCaptureStub:
    """Tests for the GTD_AI_STUB_RESPONSE env-var seam."""

    _cfg = EnvConfig(name="work", contexts=["calls"], areas=["admin"])

    def test_stub_env_var_short_circuits_subprocess(self, monkeypatch):
        def _boom(*_args, **_kwargs):
            raise AssertionError("subprocess.run must not be called when stub is set")

        monkeypatch.setattr(ai_mod.subprocess, "run", _boom)
        monkeypatch.setattr(ai_mod.shutil, "which", lambda _: None)
        monkeypatch.setenv(
            "GTD_AI_STUB_RESPONSE",
            '{"title": "Stubbed", "summary": "From stub", "contexts": ["calls"]}',
        )

        result = ai_capture(
            text="anything",
            cfg=self._cfg,
            projects=[],
            sample_actions={},
            today=date(2026, 4, 20),
        )

        assert result.title == "Stubbed"
        assert result.summary == "From stub"
        assert result.contexts == ["calls"]

    def test_stub_env_var_invalid_json_raises_no_extraction(self, monkeypatch):
        monkeypatch.setenv("GTD_AI_STUB_RESPONSE", "not json")
        with pytest.raises(AiCaptureNoExtractionError):
            ai_capture(
                text="x",
                cfg=self._cfg,
                projects=[],
                sample_actions={},
                today=date(2026, 4, 20),
            )

    def test_without_stub_still_requires_claude(self, monkeypatch):
        monkeypatch.delenv("GTD_AI_STUB_RESPONSE", raising=False)
        monkeypatch.setattr(ai_mod.shutil, "which", lambda _: None)

        with pytest.raises(AiCaptureNotConfiguredError):
            ai_capture(
                text="x",
                cfg=self._cfg,
                projects=[],
                sample_actions={},
                today=date(2026, 4, 20),
            )
