"""Tests for the merge flow: deterministic apply (`merge_items`), the
management command wrapping it, the agent prompt, and the session launcher.

No Claude CLI is involved — the prose merge happens in a separate agent
session that the launcher opens; these tests only check the plumbing.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest
from django.core.management import call_command

from gtd_core.agent_launch import GTD_REPO_ROOT, build_merge_prompt
from gtd_core.models import Bucket, Item
from gtd_core.service import GtdService


@pytest.fixture
def svc(data_root):
    fixed_now = datetime(2026, 4, 10, 9, 15)
    return GtdService(data_root, now=lambda: fixed_now)


def _item(iid: str, title: str, body: str = "", **kw) -> Item:
    return Item(
        id=iid,
        title=title,
        body=body,
        created=datetime(2026, 4, 1, 9, 0),
        updated=datetime(2026, 4, 1, 9, 0),
        status=Bucket.NEXT,
        **kw,
    )


# ---------------- service.merge_items (deterministic apply) ----------------


class TestMergeItems:
    def test_target_keeps_identity_project_status(self, svc):
        svc.create_project("work", title="Proj", project_id="2026-04-01-proj")
        target = svc.capture("work", "Target")
        target = svc.update("work", target.id, {"project": "2026-04-01-proj"})
        target = svc.move("work", target.id, Bucket.NEXT)
        source = svc.capture("work", "Source")
        source = svc.move("work", source.id, Bucket.SOMEDAY)

        merged = svc.merge_items(
            "work", target.id, source.id, title="Merged title", body="Merged body"
        )

        assert merged.id == target.id
        assert merged.created == target.created
        assert merged.status is Bucket.NEXT
        assert merged.project == "2026-04-01-proj"
        assert merged.title == "Merged title"
        assert merged.body == "Merged body"
        assert merged.updated == datetime(2026, 4, 10, 9, 15)

    def test_source_moves_to_trash(self, svc, data_root):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.merge_items("work", target.id, source.id, title="T", body="")
        assert (data_root / "work" / "trash" / f"{source.id}.md").exists()
        assert not (data_root / "work" / "inbox" / f"{source.id}.md").exists()
        assert svc.get_item("work", source.id).status is Bucket.TRASH

    def test_contexts_and_tags_unioned_in_order(self, svc):
        target = svc.capture("work", "Target", contexts=["calls", "office"])
        target = svc.update("work", target.id, {"tags": ["a", "b"]})
        source = svc.capture("work", "Source", contexts=["office", "computer"])
        source = svc.update("work", source.id, {"tags": ["b", "c"]})
        merged = svc.merge_items("work", target.id, source.id, title="T", body="")
        assert merged.contexts == ["calls", "office", "computer"]
        assert merged.tags == ["a", "b", "c"]

    def test_unknown_source_context_dropped(self, svc, data_root):
        target = svc.capture("work", "Target", contexts=["calls"])
        source = svc.capture("work", "Source")
        path = data_root / "work" / "inbox" / f"{source.id}.md"
        path.write_text(path.read_text().replace("contexts: []", "contexts: [ghost, computer]"))
        merged = svc.merge_items("work", target.id, source.id, title="T", body="")
        assert merged.contexts == ["calls", "computer"]

    def test_empty_target_scalars_filled_from_source(self, svc):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source", energy="high", time_minutes=45)
        source = svc.update(
            "work",
            source.id,
            {"due": "2026-05-01", "defer_until": "2026-04-20T09:00", "waiting_on": "Sam"},
        )
        merged = svc.merge_items("work", target.id, source.id, title="T", body="")
        assert merged.energy == "high"
        assert merged.time_minutes == 45
        assert merged.due == date(2026, 5, 1)
        assert merged.defer_until == datetime(2026, 4, 20, 9, 0)
        assert merged.waiting_on == "Sam"

    def test_non_empty_target_scalars_untouched(self, svc):
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
        merged = svc.merge_items("work", target.id, source.id, title="T", body="")
        assert merged.energy == "low"
        assert merged.time_minutes == 5
        assert merged.due == date(2026, 4, 15)
        assert merged.defer_until == datetime(2026, 4, 12, 8, 0)
        assert merged.waiting_on == "Ann"

    def test_blank_title_rejected(self, svc):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        with pytest.raises(ValueError):
            svc.merge_items("work", target.id, source.id, title="   ", body="")
        assert svc.get_item("work", source.id).status is Bucket.INBOX

    def test_same_item_rejected(self, svc):
        target = svc.capture("work", "Target")
        with pytest.raises(ValueError):
            svc.merge_items("work", target.id, target.id, title="T", body="")

    def test_missing_target_raises_key_error(self, svc):
        source = svc.capture("work", "Source")
        with pytest.raises(KeyError):
            svc.merge_items("work", "nope", source.id, title="T", body="")
        assert svc.get_item("work", source.id).status is Bucket.INBOX

    def test_missing_source_raises_key_error(self, svc):
        target = svc.capture("work", "Target")
        with pytest.raises(KeyError):
            svc.merge_items("work", target.id, "nope", title="T", body="")
        assert svc.get_item("work", target.id).title == "Target"


# ---------------- manage.py merge_items ----------------


class TestMergeItemsCommand:
    def test_merges_with_body_file(self, svc, data_root, settings, tmp_path, capsys):
        settings.GTD_DATA_ROOT = data_root
        target = svc.capture("work", "Target", contexts=["calls"])
        source = svc.capture("work", "Source", contexts=["office"])
        body_file = tmp_path / "body.md"
        body_file.write_text("- one\n- two\n")

        call_command(
            "merge_items",
            "work",
            target.id,
            source.id,
            title="Merged title",
            body_file=str(body_file),
        )

        merged = svc.get_item("work", target.id)
        assert merged.title == "Merged title"
        assert merged.body == "- one\n- two"
        assert merged.contexts == ["calls", "office"]
        assert svc.get_item("work", source.id).status is Bucket.TRASH
        out = capsys.readouterr().out
        assert target.id in out and "trash" in out

    def test_body_inline(self, svc, data_root, settings):
        settings.GTD_DATA_ROOT = data_root
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        call_command("merge_items", "work", target.id, source.id, title="T", body="inline")
        assert svc.get_item("work", target.id).body == "inline"

    def test_missing_item_errors_cleanly(self, svc, data_root, settings):
        from django.core.management.base import CommandError

        settings.GTD_DATA_ROOT = data_root
        target = svc.capture("work", "Target")
        with pytest.raises(CommandError):
            call_command("merge_items", "work", target.id, "nope", title="T", body="")


# ---------------- build_merge_prompt ----------------


def _prompt(**kw) -> str:
    defaults = dict(
        target=_item("2026-04-01T0900-target", "Call dentist", "target notes here"),
        source=_item("2026-04-01T0901-source", "Ring the dentist", "source notes here"),
        env="work",
        target_path=Path("/data/work/next/2026-04-01T0900-target.md"),
        source_path=Path("/data/work/inbox/2026-04-01T0901-source.md"),
        prior_working_on=False,
    )
    return build_merge_prompt(**{**defaults, **kw})


class TestBuildMergePrompt:
    def test_embeds_both_items_and_paths(self):
        p = _prompt()
        assert "Call dentist" in p and "target notes here" in p
        assert "Ring the dentist" in p and "source notes here" in p
        assert "/data/work/next/2026-04-01T0900-target.md" in p
        assert "/data/work/inbox/2026-04-01T0901-source.md" in p

    def test_gives_exact_apply_command(self):
        p = _prompt()
        assert "manage.py merge_items work 2026-04-01T0900-target 2026-04-01T0901-source" in p
        assert "--title" in p and "--body-file" in p
        assert str(GTD_REPO_ROOT) in p

    def test_states_merge_rules(self):
        p = _prompt().lower()
        assert "all information from both" in p
        assert "do not invent" in p
        assert "project" in p and "bucket" in p

    def test_forbids_manual_moves_and_field_edits(self):
        p = _prompt()
        assert "do NOT `mv`" in p
        assert "do NOT edit" in p

    def test_exit_protocol_records_output_and_restores_working_on(self):
        assert "`working_on: false`" in _prompt(prior_working_on=False)
        assert "`working_on: true`" in _prompt(prior_working_on=True)
        assert "## Agent run" in _prompt()
        assert "`updated:`" in _prompt()

    def test_forbids_external_and_salesforce_writes(self):
        p = _prompt()
        assert "Salesforce" in p
        assert "external" in p.lower()


# ---------------- service.launch_merge_session ----------------


class TestLaunchMergeSession:
    @pytest.fixture
    def launched(self, monkeypatch):
        calls: dict = {}

        def fake_iterm(*, prompt, cwd=None, auto=True, config_dir=None):
            calls["iterm"] = dict(prompt=prompt, cwd=cwd, config_dir=config_dir)

        def fake_desktop(*, prompt, cwd=None):
            calls["desktop"] = dict(prompt=prompt, cwd=cwd)

        monkeypatch.setattr("gtd_core.service.launch_claude_session", fake_iterm)
        monkeypatch.setattr("gtd_core.service.launch_desktop_session", fake_desktop)
        return calls

    def test_launches_iterm_in_repo_root_with_prompt(self, svc, launched):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.launch_merge_session("work", target.id, source.id)
        call = launched["iterm"]
        assert call["cwd"] == GTD_REPO_ROOT
        assert target.id in call["prompt"] and source.id in call["prompt"]
        assert "desktop" not in launched

    def test_pins_target_only(self, svc, launched):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.launch_merge_session("work", target.id, source.id)
        assert svc.get_item("work", target.id).working_on is True
        assert svc.get_item("work", source.id).working_on is False
        assert "`working_on: false`" in launched["iterm"]["prompt"]

    def test_prior_pin_is_preserved_in_prompt(self, svc, launched):
        target = svc.capture("work", "Target")
        svc.update("work", target.id, {"working_on": True})
        source = svc.capture("work", "Source")
        svc.launch_merge_session("work", target.id, source.id)
        assert "`working_on: true`" in launched["iterm"]["prompt"]

    def test_desktop_target(self, svc, launched):
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.launch_merge_session("work", target.id, source.id, target="desktop")
        assert "desktop" in launched and "iterm" not in launched

    def test_uses_env_claude_config_dir(self, svc, data_root, launched):
        cfg = data_root / "work" / "config.yml"
        cfg.write_text(cfg.read_text() + "claude_config_dir: ~/.claude-personal\n")
        target = svc.capture("work", "Target")
        source = svc.capture("work", "Source")
        svc.launch_merge_session("work", target.id, source.id)
        assert launched["iterm"]["config_dir"] == Path("~/.claude-personal").expanduser()

    def test_same_item_rejected_before_launch(self, svc, launched):
        target = svc.capture("work", "Target")
        with pytest.raises(ValueError):
            svc.launch_merge_session("work", target.id, target.id)
        assert not launched
        assert svc.get_item("work", target.id).working_on is False

    def test_missing_source_rejected_before_pin(self, svc, launched):
        target = svc.capture("work", "Target")
        with pytest.raises(KeyError):
            svc.launch_merge_session("work", target.id, "nope")
        assert not launched
        assert svc.get_item("work", target.id).working_on is False

    def test_missing_target_rejected(self, svc, launched):
        source = svc.capture("work", "Source")
        with pytest.raises(KeyError):
            svc.launch_merge_session("work", "nope", source.id)
        assert not launched
