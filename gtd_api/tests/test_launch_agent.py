from __future__ import annotations

import subprocess

import git
import pytest
from rest_framework.test import APIClient

from gtd_core.tests.conftest import make_env


@pytest.fixture
def tmp_project(tmp_path, settings):
    repo = git.Repo.init(tmp_path)
    with repo.config_writer() as cw:
        cw.set_value("user", "email", "test@example.com")
        cw.set_value("user", "name", "Test")

    data = tmp_path / "data"
    make_env(data, "work")
    (tmp_path / "README.md").write_text("test\n")
    repo.index.add(["README.md", str((data / "work" / "config.yml").relative_to(tmp_path))])
    repo.index.commit("initial")

    settings.BASE_DIR = tmp_path
    settings.GTD_DATA_ROOT = data
    return tmp_path


@pytest.fixture
def api(tmp_project):
    return APIClient()


class LauncherMock:
    """Captures the AppleScript cmds and the prompt-file contents for inspection."""

    def __init__(self):
        self.cmds: list[list[str]] = []
        self.prompts: list[str] = []


def _mock_launcher(
    monkeypatch, *, claude: str | None = "/usr/local/bin/claude", returncode=0, stderr=""
) -> LauncherMock:
    import tempfile as _tempfile

    mock = LauncherMock()
    real_mkstemp = _tempfile.mkstemp

    def fake_mkstemp(*args, **kwargs):
        fd, path = real_mkstemp(*args, **kwargs)
        # Read the prompt content right before subprocess.run (which would
        # normally hand it off to iTerm); store for assertions.
        mock.prompts.append(path)
        return fd, path

    def fake_run(cmd, **kwargs):
        mock.cmds.append(cmd)
        return subprocess.CompletedProcess(cmd, returncode=returncode, stdout="", stderr=stderr)

    def fake_which(name):
        if name == "claude":
            return claude
        if name == "osascript":
            return "/usr/bin/osascript"
        if name == "open":
            return "/usr/bin/open"
        return None

    monkeypatch.setattr("gtd_core.agent_launch.tempfile.mkstemp", fake_mkstemp)
    monkeypatch.setattr("gtd_core.agent_launch.subprocess.run", fake_run)
    monkeypatch.setattr("gtd_core.agent_launch.shutil.which", fake_which)
    return mock


def _read_prompt(mock: LauncherMock) -> str:
    assert len(mock.prompts) == 1
    with open(mock.prompts[0]) as f:
        return f.read()


def _capture_item(api, title: str, body: str = "") -> str:
    r = api.post("/api/envs/work/items/", {"title": title, "body": body}, format="json")
    assert r.status_code == 201, r.json()
    return r.json()["id"]


class TestLaunchAgentEndpoint:
    def test_launches_iterm(self, api, monkeypatch):
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "Review PR #123", body="https://github.com/x/y/pull/123")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 204
        assert len(mock.cmds) == 1
        as_script = mock.cmds[0][2]
        assert "iTerm" in as_script
        assert "claude" in as_script

    def test_uses_settings_agent_cwd(self, api, monkeypatch, settings, tmp_path):
        import shlex

        settings.GTD_AGENT_CWD = tmp_path
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 204
        assert f"cd {shlex.quote(str(tmp_path))}" in mock.cmds[0][2]

    def test_runs_claude_in_auto_mode(self, api, monkeypatch):
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 204
        assert "--permission-mode auto" in mock.cmds[0][2]
        assert "--dangerously-skip-permissions" not in mock.cmds[0][2]

    def test_returns_404_for_unknown_item(self, api, monkeypatch):
        _mock_launcher(monkeypatch)
        r = api.post("/api/envs/work/items/no-such-item/launch-agent/")
        assert r.status_code == 404

    def test_returns_503_when_claude_missing(self, api, monkeypatch):
        _mock_launcher(monkeypatch, claude=None)
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 503
        assert "claude" in r.json()["error"]

    def test_sets_working_on_true_before_launch(self, api, monkeypatch):
        _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")
        # Sanity check: starts as false
        before = api.get(f"/api/envs/work/items/{item_id}/").json()
        assert before["working_on"] is False

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")
        assert r.status_code == 204

        after = api.get(f"/api/envs/work/items/{item_id}/").json()
        assert after["working_on"] is True

    def test_includes_project_context_in_prompt(self, api, monkeypatch):
        api.post(
            "/api/envs/work/projects/",
            {
                "id": "2026-03-01-people",
                "title": "People",
                "outcome": "Quarterly cycle done well",
            },
            format="json",
        )
        item_id = _capture_item(api, "Plan reviews")
        api.patch(
            f"/api/envs/work/items/{item_id}/",
            {"project": "2026-03-01-people"},
            format="json",
        )
        mock = _mock_launcher(monkeypatch)

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")
        assert r.status_code == 204

        prompt = _read_prompt(mock)
        assert "Project context" in prompt
        assert "People" in prompt
        assert "Quarterly cycle done well" in prompt

    def test_includes_item_file_path_in_prompt(self, api, monkeypatch, tmp_path):
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")
        assert r.status_code == 204

        # Item starts in `inbox` after capture.
        expected_path = tmp_path / "data" / "work" / "inbox" / f"{item_id}.md"
        assert str(expected_path) in _read_prompt(mock)

    def test_returns_502_when_osascript_fails(self, api, monkeypatch):
        _mock_launcher(monkeypatch, returncode=1, stderr="not allowed")
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 502
        assert "not allowed" in r.json()["error"]

    def test_no_target_defaults_to_iterm(self, api, monkeypatch):
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(f"/api/envs/work/items/{item_id}/launch-agent/")

        assert r.status_code == 204
        assert "iTerm" in mock.cmds[0][2]

    def test_launches_desktop_agent_via_deep_link(self, api, monkeypatch):
        mock = _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "Review PR")

        r = api.post(
            f"/api/envs/work/items/{item_id}/launch-agent/",
            {"target": "desktop"},
            format="json",
        )

        assert r.status_code == 204
        assert len(mock.cmds) == 1
        cmd = mock.cmds[0]
        assert cmd[0] == "/usr/bin/open"
        assert "com.anthropic.claudefordesktop" in cmd
        assert cmd[-1].startswith("claude://code/new?")

    def test_desktop_target_sets_working_on_true(self, api, monkeypatch):
        _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(
            f"/api/envs/work/items/{item_id}/launch-agent/",
            {"target": "desktop"},
            format="json",
        )
        assert r.status_code == 204

        after = api.get(f"/api/envs/work/items/{item_id}/").json()
        assert after["working_on"] is True

    def test_rejects_unknown_target(self, api, monkeypatch):
        _mock_launcher(monkeypatch)
        item_id = _capture_item(api, "anything")

        r = api.post(
            f"/api/envs/work/items/{item_id}/launch-agent/",
            {"target": "bogus"},
            format="json",
        )

        assert r.status_code == 400
        assert "bogus" in r.json()["error"]
