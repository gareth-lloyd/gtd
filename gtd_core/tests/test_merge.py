"""Tests for GtdService.merge_items and gtd_core.ai.ai_merge.

The Claude CLI is never invoked — the GTD_AI_STUB_RESPONSE env seam feeds
the merged title/body straight into the pipeline.
"""

from __future__ import annotations

import json
from datetime import date, datetime

import pytest

import gtd_core.ai as ai_mod
from gtd_core.ai import (
    AiCaptureNoExtractionError,
    AiCaptureNotConfiguredError,
    AiMergeResult,
    _build_merge_prompt,
    ai_merge,
)
from gtd_core.models import Bucket, Item
from gtd_core.service import GtdService


@pytest.fixture
def svc(data_root):
    fixed_now = datetime(2026, 4, 10, 9, 15)
    return GtdService(data_root, now=lambda: fixed_now)


def _stub(monkeypatch, title="Merged title", body="Merged body"):
    monkeypatch.setenv("GTD_AI_STUB_RESPONSE", json.dumps({"title": title, "body": body}))


def _item(iid: str, title: str, body: str = "") -> Item:
    return Item(
        id=iid,
        title=title,
        body=body,
        created=datetime(2026, 4, 1, 9, 0),
        updated=datetime(2026, 4, 1, 9, 0),
        status=Bucket.NEXT,
    )


# ---------------- ai_merge / prompt ----------------


class TestAiMerge:
    def test_stub_seam_returns_result(self, monkeypatch):
        _stub(monkeypatch, "T", "B")
        result = ai_merge(target=_item("a", "A"), source=_item("b", "B"), today=date(2026, 4, 10))
        assert result == AiMergeResult(title="T", body="B")

    def test_stub_missing_title_raises(self, monkeypatch):
        monkeypatch.setenv("GTD_AI_STUB_RESPONSE", json.dumps({"body": "x"}))
        with pytest.raises(AiCaptureNoExtractionError):
            ai_merge(target=_item("a", "A"), source=_item("b", "B"), today=date(2026, 4, 10))

    def test_stub_null_body_becomes_empty_string(self, monkeypatch):
        monkeypatch.setenv("GTD_AI_STUB_RESPONSE", json.dumps({"title": "T", "body": None}))
        result = ai_merge(target=_item("a", "A"), source=_item("b", "B"), today=date(2026, 4, 10))
        assert result.body == ""

    def test_no_cli_raises_not_configured(self, monkeypatch):
        monkeypatch.delenv("GTD_AI_STUB_RESPONSE", raising=False)
        monkeypatch.setattr(ai_mod.shutil, "which", lambda name: None)
        with pytest.raises(AiCaptureNotConfiguredError):
            ai_merge(target=_item("a", "A"), source=_item("b", "B"), today=date(2026, 4, 10))

    def test_prompt_embeds_both_items(self):
        prompt = _build_merge_prompt(
            target=_item("a", "Call dentist", "target notes here"),
            source=_item("b", "Ring the dentist", "source notes here"),
            today=date(2026, 4, 10),
        )
        assert "Call dentist" in prompt
        assert "target notes here" in prompt
        assert "Ring the dentist" in prompt
        assert "source notes here" in prompt
        assert "2026-04-10" in prompt
        assert '"title"' in prompt and '"body"' in prompt


# ---------------- service.merge_items ----------------


class TestMergeItems:
    def test_target_keeps_identity_project_status(self, svc, monkeypatch):
        _stub(monkeypatch, "Merged title", "Merged body")
        svc.create_project("work", title="Proj", project_id="2026-04-01-proj")
        target = svc.capture("work", "Target")
        target = svc.update("work", target.id, {"project": "2026-04-01-proj"})
        target = svc.move("work", target.id, Bucket.NEXT)
        source = svc.capture("work", "Source")
        source = svc.update("work", source.id, {"project": None})
        source = svc.move("work", source.id, Bucket.SOMEDAY)

        merged = svc.merge_items("work", target.id, source.id)

        assert merged.id == target.id
        assert merged.created == target.created
        assert merged.status is Bucket.NEXT
        assert merged.project == "2026-04-01-proj"
        assert merged.title == "Merged title"
        assert merged.body == "Merged body"
        assert merged.updated == datetime(2026, 4, 10, 9, 15)

    def test_source_moves_to_trash(self, svc, data_root, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.merge_items("work", target.id, source.id)
        assert (data_root / "work" / "trash" / f"{source.id}.md").exists()
        assert not (data_root / "work" / "inbox" / f"{source.id}.md").exists()
        assert svc.get_item("work", source.id).status is Bucket.TRASH

    def test_contexts_and_tags_unioned_in_order(self, svc, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target", contexts=["calls", "office"])
        target = svc.update("work", target.id, {"tags": ["a", "b"]})
        source = svc.capture("work", "Source", contexts=["office", "computer"])
        source = svc.update("work", source.id, {"tags": ["b", "c"]})
        merged = svc.merge_items("work", target.id, source.id)
        assert merged.contexts == ["calls", "office", "computer"]
        assert merged.tags == ["a", "b", "c"]

    def test_unknown_source_context_dropped(self, svc, data_root, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target", contexts=["calls"])
        source = svc.capture("work", "Source")
        # Write a context that is no longer in config directly into the file.
        path = data_root / "work" / "inbox" / f"{source.id}.md"
        text = path.read_text().replace("contexts: []", "contexts: [ghost, computer]")
        path.write_text(text)
        merged = svc.merge_items("work", target.id, source.id)
        assert merged.contexts == ["calls", "computer"]

    def test_empty_target_scalars_filled_from_source(self, svc, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source", energy="high", time_minutes=45)
        source = svc.update(
            "work",
            source.id,
            {
                "due": "2026-05-01",
                "defer_until": "2026-04-20T09:00",
                "waiting_on": "Sam",
            },
        )
        merged = svc.merge_items("work", target.id, source.id)
        assert merged.energy == "high"
        assert merged.time_minutes == 45
        assert merged.due == date(2026, 5, 1)
        assert merged.defer_until == datetime(2026, 4, 20, 9, 0)
        assert merged.waiting_on == "Sam"

    def test_non_empty_target_scalars_untouched(self, svc, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target", energy="low", time_minutes=5)
        target = svc.update(
            "work",
            target.id,
            {"due": "2026-04-15", "defer_until": "2026-04-12T08:00", "waiting_on": "Ann"},
        )
        source = svc.capture("work", "Source", energy="high", time_minutes=45)
        source = svc.update(
            "work",
            source.id,
            {"due": "2026-05-01", "defer_until": "2026-04-20T09:00", "waiting_on": "Sam"},
        )
        merged = svc.merge_items("work", target.id, source.id)
        assert merged.energy == "low"
        assert merged.time_minutes == 5
        assert merged.due == date(2026, 4, 15)
        assert merged.defer_until == datetime(2026, 4, 12, 8, 0)
        assert merged.waiting_on == "Ann"

    def test_same_item_rejected(self, svc, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target")
        with pytest.raises(ValueError):
            svc.merge_items("work", target.id, target.id)

    def test_missing_target_raises_key_error(self, svc, monkeypatch):
        _stub(monkeypatch)
        source = svc.capture("work", "Source")
        with pytest.raises(KeyError):
            svc.merge_items("work", "nope", source.id)
        assert svc.get_item("work", source.id).status is Bucket.INBOX

    def test_missing_source_raises_key_error(self, svc, monkeypatch):
        _stub(monkeypatch)
        target = svc.capture("work", "Target")
        with pytest.raises(KeyError):
            svc.merge_items("work", target.id, "nope")
        assert svc.get_item("work", target.id).title == "Target"

    def test_ai_failure_leaves_both_items_untouched(self, svc, monkeypatch):
        monkeypatch.setenv("GTD_AI_STUB_RESPONSE", "not json")
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        with pytest.raises(AiCaptureNoExtractionError):
            svc.merge_items("work", target.id, source.id)
        assert svc.get_item("work", target.id).title == "Target"
        assert svc.get_item("work", source.id).status is Bucket.INBOX
