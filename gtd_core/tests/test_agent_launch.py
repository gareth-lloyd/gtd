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
from urllib.parse import quote

import pytest

from gtd_core.agent_launch import (
    AgentLaunchError,
    AgentLaunchNotConfiguredError,
    AgentLaunchUpstreamError,
    build_prompt,
    launch_claude_session,
    launch_desktop_session,
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

    def test_exit_clears_working_on_when_not_previously_pinned(self, tmp_path):
        # Default: the item was not pinned before launch, so finishing means
        # clearing the flag back to false.
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "`working_on: false`" in out
        assert "`working_on: true`" not in out

    def test_exit_restores_prior_pin_when_already_working_on(self, tmp_path):
        # The user had already pinned this item before launching the agent.
        # Finishing must restore it to that state (true), not blindly clear it.
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path), prior_working_on=True)
        assert "`working_on: true`" in out
        assert "`working_on: false`" not in out

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

    def test_absolutely_forbids_salesforce_writes(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        # Salesforce is a hard NEVER, not an ask-first surface: it is the
        # company's system of record and a stray write is not recoverable
        # by the user.
        assert "NEVER" in out
        assert "Salesforce" in out
        assert "no exception" in out.lower()

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

    def test_includes_next_task_section_when_given(self, tmp_path):
        item = self._item("Do the thing")
        item.output = "## Agent run 2026-05-06\nDid the first half."
        out = build_prompt(item, **self._kwargs(tmp_path), next_task="Now do the second half")
        assert "## Next agent work" in out
        assert "Now do the second half" in out
        # The follow-up is the thing to do now — it must come after the
        # original task so it reads as the most recent, most specific ask.
        assert out.index("## Task") < out.index("## Next agent work")
        assert out.index("Prior agent runs") < out.index("## Next agent work")

    def test_next_task_instructs_agent_to_record_it_in_output(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path), next_task="Follow up")
        section = out[out.index("## Next agent work") :]
        assert "## Agent run" in section
        assert "Follow up" in section

    def test_omits_next_task_section_by_default(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path))
        assert "Next agent work" not in out

    def test_blank_next_task_is_treated_as_absent(self, tmp_path):
        out = build_prompt(self._item("t"), **self._kwargs(tmp_path), next_task="   \n ")
        assert "Next agent work" not in out


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


def _mock_which_open(monkeypatch, *, opener: str | None = "/usr/bin/open"):
    """which() that only knows about `open` — claude/osascript are absent."""

    def fake_which(name):
        return opener if name == "open" else None

    monkeypatch.setattr("gtd_core.agent_launch.shutil.which", fake_which)


class TestLaunchDesktopSession:
    def test_opens_claude_code_deep_link(self, monkeypatch, tmp_path):
        _mock_which_open(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_desktop_session(prompt="Review this PR", cwd=tmp_path)

        assert len(cmds) == 1
        cmd = cmds[0]
        assert cmd[0] == "/usr/bin/open"
        # Routed explicitly to the desktop app's bundle so the CLI's competing
        # claude:// handler can't intercept it.
        assert cmd[1] == "-b"
        assert cmd[2] == "com.anthropic.claudefordesktop"
        url = cmd[-1]
        assert url.startswith("claude://code/new?")
        assert "q=Review%20this%20PR" in url
        assert f"folder={quote(str(tmp_path), safe='')}" in url

    def test_url_encodes_special_chars(self, monkeypatch, tmp_path):
        _mock_which_open(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_desktop_session(prompt='a "tricky" & prompt', cwd=tmp_path)

        url = cmds[0][-1]
        # Nothing that would break the URL or be read as a param separator may
        # leak through unencoded.
        assert " " not in url
        assert '"' not in url
        assert "a%20%22tricky%22%20%26%20prompt" in url

    def test_does_not_require_claude_cli(self, monkeypatch, tmp_path):
        # _mock_which_open returns None for "claude" — desktop launch only needs
        # `open` and the registered desktop-app handler, never the CLI.
        _mock_which_open(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_desktop_session(prompt="hi", cwd=tmp_path)

        assert len(cmds) == 1

    def test_default_cwd_is_home(self, monkeypatch):
        _mock_which_open(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_desktop_session(prompt="hi")

        assert f"folder={quote(str(Path.home()), safe='')}" in cmds[0][-1]

    def test_missing_open_raises_not_configured(self, monkeypatch, tmp_path):
        _mock_which_open(monkeypatch, opener=None)
        _mock_subprocess(monkeypatch)

        with pytest.raises(AgentLaunchNotConfiguredError, match="open"):
            launch_desktop_session(prompt="hi", cwd=tmp_path)

    def test_open_failure_raises_upstream(self, monkeypatch, tmp_path):
        _mock_which_open(monkeypatch)
        _mock_subprocess(monkeypatch, returncode=1, stderr="no handler")

        with pytest.raises(AgentLaunchUpstreamError, match="no handler"):
            launch_desktop_session(prompt="hi", cwd=tmp_path)

    def test_open_timeout_raises_upstream(self, monkeypatch, tmp_path):
        _mock_which_open(monkeypatch)
        _mock_subprocess(monkeypatch, raise_exc=subprocess.TimeoutExpired(cmd="open", timeout=10))

        with pytest.raises(AgentLaunchUpstreamError, match="timed out"):
            launch_desktop_session(prompt="hi", cwd=tmp_path)


class TestLaunchClaudeSessionConfigDir:
    """`config_dir` pins the session to a specific Claude Code account by
    prefixing the command with CLAUDE_CONFIG_DIR — the same mechanism the
    user's `pclaude` shell function uses for the personal account."""

    def test_prefixes_claude_config_dir_when_given(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)
        config_dir = tmp_path / ".claude-personal"

        launch_claude_session(prompt="hi", cwd=tmp_path, config_dir=config_dir)

        as_script = cmds[0][2]
        expected = f"CLAUDE_CONFIG_DIR={shlex.quote(str(config_dir))} claude --permission-mode auto"
        assert expected in as_script

    def test_omits_claude_config_dir_by_default(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)

        launch_claude_session(prompt="hi", cwd=tmp_path)

        as_script = cmds[0][2]
        assert "CLAUDE_CONFIG_DIR" not in as_script
        assert "&& claude --permission-mode auto" in as_script

    def test_config_dir_with_spaces_is_shell_quoted(self, monkeypatch, tmp_path):
        _mock_which(monkeypatch)
        cmds = _mock_subprocess(monkeypatch)
        config_dir = tmp_path / "my claude dir"

        launch_claude_session(prompt="hi", cwd=tmp_path, config_dir=config_dir)

        as_script = cmds[0][2]
        assert f"CLAUDE_CONFIG_DIR={shlex.quote(str(config_dir))}" in as_script
