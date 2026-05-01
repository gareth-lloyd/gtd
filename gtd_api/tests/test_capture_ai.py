from __future__ import annotations

import json
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
    initial_files = ["README.md"]
    make_env(data, "work")
    initial_files.append(str((data / "work" / "config.yml").relative_to(tmp_path)))

    (tmp_path / "README.md").write_text("test\n")
    repo.index.add(initial_files)
    repo.index.commit("initial")

    settings.BASE_DIR = tmp_path
    settings.GTD_DATA_ROOT = data
    return tmp_path


@pytest.fixture
def api(tmp_project):
    return APIClient()


def _mock_claude_cli(monkeypatch, response_dict: dict | None):
    """Mock subprocess.run to simulate the claude CLI returning JSON."""
    captured_cmds: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured_cmds.append(cmd)
        if response_dict is None:
            return subprocess.CompletedProcess(
                cmd, returncode=0, stdout="not json at all", stderr=""
            )
        return subprocess.CompletedProcess(
            cmd, returncode=0, stdout=json.dumps(response_dict), stderr=""
        )

    monkeypatch.setattr("gtd_core.ai.subprocess.run", fake_run)
    # Ensure shutil.which finds "claude"
    monkeypatch.setattr("gtd_core.ai.shutil.which", lambda name: "/usr/local/bin/claude")
    return captured_cmds


def _create_project(api, **fields):
    payload = {"id": fields["id"], "title": fields["title"], **fields}
    r = api.post("/api/envs/work/projects/", payload, format="json")
    assert r.status_code == 201, r.json()
    return r.json()


class TestCaptureAiHappyPath:
    def test_all_fields_applied_and_item_moves_to_next(self, api, monkeypatch):
        _create_project(
            api,
            id="2026-03-01-people-mgmt",
            title="People",
            outcome="Quarterly performance cycle done well",
            priority=2,
        )
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Collate Ryan's review notes",
                "body": "",
                "energy": "high",
                "time_minutes": 30,
                "contexts": ["computer"],
                "area": "engineering",
                "project_query": "People",
                "due": "2026-04-17",
                "defer_until": "2026-04-17",
                "summary": "Filed to People — due/defer 2026-04-17, 30m, high",
            },
        )

        r = api.post(
            "/api/envs/work/items/capture-ai/",
            {
                "text": "Collate notes for Ryan's performance review. "
                "high energy, due tomorrow, defer tomorrow, 30m. People"
            },
            format="json",
        )
        assert r.status_code == 201, r.json()
        body = r.json()
        assert body["summary"].startswith("Filed to People")
        assert body["skipped_inbox"] is True
        assert body["project_title"] == "People"

        item = body["item"]
        assert item["title"] == "Collate Ryan's review notes"
        assert item["status"] == "next"
        assert item["project"] == "2026-03-01-people-mgmt"
        assert item["energy"] == "high"
        assert item["time_minutes"] == 30
        assert item["contexts"] == ["computer"]
        assert item["area"] == "engineering"
        assert item["due"] == "2026-04-17"
        assert item["defer_until"] == "2026-04-17T00:00:00"


class TestCaptureAiFiltering:
    def test_unknown_contexts_are_stripped(self, api, monkeypatch):
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Call dentist",
                "contexts": ["calls", "not-a-real-context"],
                "summary": "Added to inbox",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "call dentist"}, format="json")
        assert r.status_code == 201
        assert r.json()["item"]["contexts"] == ["calls"]

    def test_unknown_area_dropped(self, api, monkeypatch):
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Plan roadmap",
                "area": "not-a-real-area",
                "summary": "Added to inbox",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "plan roadmap"}, format="json")
        assert r.status_code == 201
        assert r.json()["item"]["area"] is None

    def test_no_project_match_stays_in_inbox(self, api, monkeypatch):
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Run",
                "project_query": "nonexistent-project",
                "summary": "Added to inbox",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "run"}, format="json")
        assert r.status_code == 201
        body = r.json()
        assert body["skipped_inbox"] is False
        assert body["project_title"] is None
        assert body["item"]["status"] == "inbox"
        assert body["item"]["project"] is None


class TestCaptureAiErrors:
    def test_missing_cli_returns_503(self, api, monkeypatch):
        monkeypatch.setattr("gtd_core.ai.shutil.which", lambda name: None)
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "anything"}, format="json")
        assert r.status_code == 503
        assert "claude CLI" in r.json()["error"]

    def test_invalid_json_returns_422(self, api, monkeypatch):
        _mock_claude_cli(monkeypatch, response_dict=None)
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "anything"}, format="json")
        assert r.status_code == 422
        assert "AI did not return valid JSON" in r.json()["error"]

    def test_unknown_env_returns_404(self, api, monkeypatch):
        _mock_claude_cli(monkeypatch, {"title": "x", "summary": "x"})
        r = api.post("/api/envs/nope/items/capture-ai/", {"text": "x"}, format="json")
        assert r.status_code == 404


class TestCaptureAiPromptShape:
    def test_prompt_includes_config_and_projects(self, api, monkeypatch):
        _create_project(
            api,
            id="2026-03-01-people-mgmt",
            title="People",
            outcome="Quarterly performance cycle done well",
            priority=2,
        )
        cmds = _mock_claude_cli(monkeypatch, {"title": "x", "summary": "x"})
        api.post("/api/envs/work/items/capture-ai/", {"text": "x"}, format="json")

        # The prompt is the second arg after "claude" and "-p"
        assert len(cmds) == 1
        cmd = cmds[0]
        assert cmd[0].endswith("claude")
        assert cmd[1] == "-p"
        prompt = cmd[2]
        # Config contexts + areas
        assert "calls" in prompt and "engineering" in prompt
        # Project catalogue
        assert "People" in prompt
        assert "Quarterly performance cycle done well" in prompt


class TestFuzzyProjectMatching:
    def test_matches_case_insensitive_title(self, api, monkeypatch):
        _create_project(api, id="2026-03-01-people-mgmt", title="People", priority=2)
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Do something",
                "project_query": "PEOPLE",
                "summary": "Filed to People",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "x"}, format="json")
        assert r.json()["item"]["project"] == "2026-03-01-people-mgmt"

    def test_matches_substring(self, api, monkeypatch):
        _create_project(api, id="2026-03-01-ship-the-release", title="Ship the release")
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "Draft notes",
                "project_query": "release",
                "summary": "Filed",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "x"}, format="json")
        assert r.json()["item"]["project"] == "2026-03-01-ship-the-release"

    def test_matches_fuzzy_typo(self, api, monkeypatch):
        _create_project(api, id="2026-03-01-performance", title="Performance")
        _mock_claude_cli(
            monkeypatch,
            {
                "title": "x",
                "project_query": "Performence",
                "summary": "Filed",
            },
        )
        r = api.post("/api/envs/work/items/capture-ai/", {"text": "x"}, format="json")
        assert r.json()["item"]["project"] == "2026-03-01-performance"
