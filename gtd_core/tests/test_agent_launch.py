"""Unit tests for gtd_core/agent_launch.py.

The osascript subprocess is never invoked here — we mock subprocess.run and
shutil.which to verify the command shape and prompt-file contents.
"""

from __future__ import annotations

import shlex
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from gtd_core.agent_launch import (
    AgentLaunchError,
    AgentLaunchNotConfiguredError,
    AgentLaunchUpstreamError,
    build_prompt,
    launch_claude_session,
)
from gtd_core.models import Bucket, Item, Project


def _mock_subprocess(
    monkeypatch, returncode: int = 0, stderr: str = "", *, raise_exc: Exception | None = None
) -> list[list[str]]:
    captured: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured.append(cmd)
        if raise_exc is not None:
            raise raise_exc
        return subprocess.CompletedProcess(cmd, returncode=returncode, stdout="", stderr=stderr)

    monkeypatch.setattr("gtd_core.agent_launch.subprocess.run", fake_run)
    return captured


def _mock_which(monkeypatch, *, claude: str | None = "/usr/local/bin/claude"):
    def fake_which(name):
        if name == "claude":
            return claude
        if name == "osascript":
            return "/usr/bin/osascript"
        return None

    monkeypatch.setattr("gtd_core.agent_launch.shutil.which", fake_which)


def _capture_prompt_file(monkeypatch) -> list[Path]:
    """Capture paths returned by mkstemp inside agent_launch."""
    paths: list[Path] = []
    real_mkstemp = tempfile.mkstemp

    def fake_mkstemp(*args, **kwargs):
        fd, p = real_mkstemp(*args, **kwargs)
        paths.append(Path(p))
        return fd, p

    monkeypatch.setattr("gtd_core.agent_launch.tempfile.mkstemp", fake_mkstemp)
    return paths


class TestBuildPrompt:
    def _item(self, title: str, body: str = "", project: str | None = None) -> Item:
        return Item(
            id="2026-04-10T0900-test",
            title=title,
            body=body,
            created=datetime(2026, 4, 10, 9, 0),
            updated=datetime(2026, 4, 10, 9, 0),
            status=Bucket.NEXT,
            project=project,
        )

    def _kwargs(self, tmp_path):
        return {
            "item_path": tmp_path / "data" / "work" / "next" / "x.md",
            "env_dir": tmp_path / "data" / "work",
        }

    def test_includes_preamble_and_title(self, tmp_path):
        out = build_prompt(self._item("Review PR #123"), **self._kwargs(tmp_path))
        assert out.startswith("You were launched from a GTD")
        assert "Review PR #123" in out

    def test_includes_body_when_present(self, tmp_path):
        item = self._item("t", body="https://example.com/pr/1")
        out = build_prompt(item, **self._kwargs(tmp_path))
        assert "https://example.com/pr/1" in out

    def test_omits_body_when_empty(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert out.endswith("t")

    def test_includes_item_file_path(self, tmp_path):
        kw = self._kwargs(tmp_path)
        out = build_prompt(self._item("t"), **kw)
        assert str(kw["item_path"]) in out

    def test_includes_env_dir_and_bucket_names(self, tmp_path):
        kw = self._kwargs(tmp_path)
        out = build_prompt(self._item("t"), **kw)
        assert str(kw["env_dir"]) in out
        for bucket in ("inbox", "next", "waiting", "someday", "reference", "archive", "trash"):
            assert bucket in out

    def test_instructs_output_field_and_updated_bump(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "`output:`" in out
        assert "`updated:`" in out

    def test_instructs_working_on_clear_on_completion(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "working_on" in out

    def test_forbids_unilateral_task_completion(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        # Past behavior: agent autonomously archived after completing work.
        # The prompt must make clear that completion/move is the user's call.
        assert "do not decide when the task is finished" in out
        assert "user's call" in out
        assert "stop" in out.lower()
        assert "archive" in out  # mentioned in the forbidden-by-default list

    def test_forbids_external_writes_without_approval(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        # The guardrail must name each high-risk surface so the agent can't
        # rationalize "the task seems to want this" — see CLAUDE.md / user feedback.
        assert "STRICT" in out
        assert "Linear" in out
        assert "Notion" in out
        assert "GitHub" in out
        assert "Slack" in out
        assert "ASK FIRST" in out

    def test_instructs_including_links_in_output(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        # Output is far more useful when references are clickable — the agent
        # must include URLs for PRs, Slack messages, Notion docs, etc., not
        # just bare identifiers like "PR #4012".
        assert "Include links" in out
        assert "Slack messages" in out
        assert "Notion docs" in out
        assert "alongside" in out

    def test_mentions_review_pr_and_debug_shell_commands(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        # The agent should know these helper commands exist so it can reach
        # for them when the task calls for a PR review or a backend repro.
        assert "/pr-review-toolkit:review-pr" in out
        assert "/debug_in_shell" in out

    def test_includes_project_section_when_project_given(self, tmp_path):
        project = Project(
            id="2026-03-01-people",
            title="People",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            outcome="Quarterly cycle done well",
            area="management",
        )
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path), project=project)
        assert "Project context" in out
        assert "People" in out
        assert "Quarterly cycle done well" in out
        assert "management" in out

    def test_includes_working_dir_when_set(self, tmp_path):
        project = Project(
            id="2026-03-01-code",
            title="Code",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            working_dir="~/projects/foo",
        )
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path), project=project)
        assert "Working directory: ~/projects/foo" in out

    def test_omits_project_section_when_no_project(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "Project context" not in out

    def test_includes_prior_output_section_when_output_present(self, tmp_path):
        item = self._item("t")
        item.output = "## Agent run 2026-05-06\nReviewed PR. Found two nits."
        out = build_prompt(item, **self._kwargs(tmp_path))
        assert "Prior agent runs" in out
        assert "## Agent run 2026-05-06" in out
        assert "Reviewed PR. Found two nits." in out
        # Wraps the verbatim content in a fence to keep it from blending into
        # the surrounding instructions.
        assert "```\n## Agent run 2026-05-06" in out
        # Anti-overwrite signposting must be present.
        assert "APPEND" in out

    def test_omits_prior_output_section_when_output_empty(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "Prior agent runs" not in out

    def test_prior_output_appears_before_task(self, tmp_path):
        item = self._item("Do the thing")
        item.output = "Earlier work happened."
        out = build_prompt(item, **self._kwargs(tmp_path))
        assert out.index("Prior agent runs") < out.index("## Task")


class TestLaunchClaudeSession:
    def test_invokes_osascript_with_iterm_app(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)
        prompt_files = _capture_prompt_file(monkeypatch)

        launch_claude_session(prompt="Review this PR", cwd=tmp_path)

        assert len(cmds) == 1
        cmd = cmds[0]
        assert cmd[:2] == ["/usr/bin/osascript", "-e"]
        as_script = cmd[2]
        assert 'tell application "iTerm"' in as_script
        assert "create tab with default profile" in as_script
        assert "create window with default profile" in as_script  # fallback path
        assert "write text" in as_script
        assert "claude" in as_script

        assert len(prompt_files) == 1
        assert prompt_files[0].read_text() == "Review this PR"

    def test_writes_prompt_to_temp_file(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        _mock_subprocess(monkeypatch)
        prompt_files = _capture_prompt_file(monkeypatch)

        prompt = 'A "tricky" prompt with $shell and `backticks` and \nnewlines'
        launch_claude_session(prompt=prompt, cwd=tmp_path)

        assert prompt_files[0].read_text() == prompt

    def test_command_references_prompt_file_via_cat(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)
        prompt_files = _capture_prompt_file(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path)

        as_script = cmds[0][2]
        assert str(prompt_files[0]) in as_script
        assert "cat" in as_script

    def test_uses_trap_to_cleanup_on_sighup(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path)

        as_script = cmds[0][2]
        assert "trap" in as_script
        assert "EXIT" in as_script

    def test_command_changes_to_requested_cwd(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path)

        as_script = cmds[0][2]
        assert f"cd {shlex.quote(str(tmp_path))}" in as_script

    def test_missing_claude_cli_raises_not_configured(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch, claude=None)
        _mock_subprocess(monkeypatch)

        with pytest.raises(AgentLaunchNotConfiguredError, match="claude"):
            launch_claude_session(prompt="hi", cwd=tmp_path)

    def test_osascript_failure_raises_upstream(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        _mock_subprocess(monkeypatch, returncode=1, stderr="not allowed")

        with pytest.raises(AgentLaunchUpstreamError, match="not allowed"):
            launch_claude_session(prompt="hi", cwd=tmp_path)

    def test_osascript_failure_cleans_up_temp_file(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        _mock_subprocess(monkeypatch, returncode=1, stderr="boom")
        prompt_files = _capture_prompt_file(monkeypatch)

        with pytest.raises(AgentLaunchError):
            launch_claude_session(prompt="hi", cwd=tmp_path)

        assert not prompt_files[0].exists()

    def test_osascript_timeout_raises_upstream_and_cleans_up(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        _mock_subprocess(
            monkeypatch, raise_exc=subprocess.TimeoutExpired(cmd="osascript", timeout=10)
        )
        prompt_files = _capture_prompt_file(monkeypatch)

        with pytest.raises(AgentLaunchUpstreamError, match="timed out"):
            launch_claude_session(prompt="hi", cwd=tmp_path)

        assert not prompt_files[0].exists()

    def test_default_cwd_is_home(self, monkeypatch):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi")

        as_script = cmds[0][2]
        assert f"cd {shlex.quote(str(Path.home()))}" in as_script

    def test_auto_mode_default_passes_permission_mode_auto(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path)

        assert "--permission-mode auto" in cmds[0][2]
        assert "--dangerously-skip-permissions" not in cmds[0][2]

    def test_auto_mode_off_omits_permission_mode_flag(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path, auto=False)

        assert "--permission-mode" not in cmds[0][2]
        assert "--dangerously-skip-permissions" not in cmds[0][2]
