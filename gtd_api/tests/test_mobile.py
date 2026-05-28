import pytest
from rest_framework.test import APIClient

from gtd_core.models import Bucket
from gtd_core.service import GtdService
from gtd_core.snapshot import SnapshotResult
from gtd_core.tests.conftest import make_env

pytestmark = pytest.mark.urls("gtd_site.urls_cloud")


@pytest.fixture
def data(tmp_path, settings):
    root = tmp_path / "data"
    make_env(root, "work")
    make_env(root, "home")
    settings.BASE_DIR = tmp_path
    settings.GTD_DATA_ROOT = root
    settings.GTD_CLOUD_SYNC = False
    settings.GTD_CLOUD_TOKEN = ""
    return root


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def svc(data):
    return GtdService(data)


class TestMobileCapture:
    def test_capture_creates_inbox_item(self, api, data):
        r = api.post("/api/envs/home/capture/", {"title": "Buy milk"}, format="json")
        assert r.status_code == 201
        assert r.json()["title"] == "Buy milk"
        assert r.json()["status"] == "inbox"

    def test_capture_unknown_env_404(self, api, data):
        r = api.post("/api/envs/nope/capture/", {"title": "x"}, format="json")
        assert r.status_code == 404


class TestMobileReads:
    def test_list_envs(self, api, data):
        r = api.get("/api/envs/")
        assert r.status_code == 200
        assert {e["name"] for e in r.json()} == {"work", "home"}

    def test_inbox_lists_inbox_items(self, api, data, svc):
        svc.capture("home", "inbox task")
        r = api.get("/api/envs/home/inbox/")
        assert r.status_code == 200
        titles = [i["title"] for i in r.json()]
        assert titles == ["inbox task"]

    def test_next_respects_project_cap(self, api, data, svc):
        # Project capped at 1 visible next-action; two ordered items → only one.
        svc.create_project("home", title="Proj", project_id="proj")
        svc.update_project("home", "proj", {"max_next_items": 1})
        a = svc.capture("home", "first")
        b = svc.capture("home", "second")
        svc.move("home", a.id, Bucket.NEXT)
        svc.move("home", b.id, Bucket.NEXT)
        svc.update("home", a.id, {"project": "proj", "order": 1})
        svc.update("home", b.id, {"project": "proj", "order": 2})

        r = api.get("/api/envs/home/next/")
        assert r.status_code == 200
        titles = [i["title"] for i in r.json()]
        assert titles == ["first"]


class TestLockedSurface:
    """Routes outside capture/inbox/next must not be reachable on cloud."""

    @pytest.mark.parametrize(
        "method,path",
        [
            ("get", "/api/envs/home/items/"),
            ("get", "/api/envs/home/config/"),
            ("get", "/api/envs/home/projects/"),
            ("post", "/api/envs/home/items/capture-ai/"),
            ("post", "/api/snapshot/"),
            ("get", "/api/snapshot/status/"),
            ("get", "/bear-api/notes/"),
        ],
    )
    def test_route_not_found(self, api, data, method, path):
        r = getattr(api, method)(path)
        assert r.status_code == 404


class TestTokenGate:
    def test_requests_blocked_without_token(self, api, data, settings):
        settings.GTD_CLOUD_TOKEN = "secret123"
        assert api.get("/api/envs/").status_code == 401
        assert api.get("/api/envs/home/inbox/").status_code == 401
        assert api.get("/api/envs/home/next/").status_code == 401
        assert api.post("/api/envs/home/capture/", {"title": "x"}, format="json").status_code == 401

    def test_wrong_token_blocked(self, api, data, settings):
        settings.GTD_CLOUD_TOKEN = "secret123"
        r = api.get("/api/envs/", headers={"X-GTD-Token": "nope"})
        assert r.status_code == 401

    def test_correct_token_passes(self, api, data, settings):
        settings.GTD_CLOUD_TOKEN = "secret123"
        r = api.get("/api/envs/", headers={"X-GTD-Token": "secret123"})
        assert r.status_code == 200

    def test_health_open_without_token(self, api, data, settings):
        settings.GTD_CLOUD_TOKEN = "secret123"
        assert api.get("/api/health/").status_code == 200

    def test_no_token_required_when_unset(self, api, data, settings):
        settings.GTD_CLOUD_TOKEN = ""
        assert api.get("/api/envs/").status_code == 200


class TestCloudSyncWiring:
    def test_capture_triggers_push_when_sync_enabled(self, api, data, settings, monkeypatch):
        settings.GTD_CLOUD_SYNC = True
        calls = []
        monkeypatch.setattr(
            "gtd_api.mobile_views.commit_and_push",
            lambda root, message=None: calls.append(root)
            or SnapshotResult(committed=True, pushed=True),
        )
        monkeypatch.setattr("gtd_api.mobile_views.pull_latest", lambda root: calls.append("pull"))
        r = api.post("/api/envs/home/capture/", {"title": "x"}, format="json")
        assert r.status_code == 201
        assert r.json()["synced"] is True
        assert settings.BASE_DIR in calls

    def test_capture_reports_unsynced_when_push_fails(self, api, data, settings, monkeypatch):
        settings.GTD_CLOUD_SYNC = True
        monkeypatch.setattr(
            "gtd_api.mobile_views.commit_and_push",
            lambda root, message=None: SnapshotResult(
                committed=True, pushed=False, push_error="boom"
            ),
        )
        r = api.post("/api/envs/home/capture/", {"title": "x"}, format="json")
        # The item is still created (201) but flagged not-yet-durable so the
        # client can warn the user instead of silently claiming success.
        assert r.status_code == 201
        assert r.json()["synced"] is False

    def test_capture_synced_true_when_sync_disabled(self, api, data, settings):
        settings.GTD_CLOUD_SYNC = False
        r = api.post("/api/envs/home/capture/", {"title": "x"}, format="json")
        assert r.status_code == 201
        assert r.json()["synced"] is True

    def test_read_triggers_pull_when_sync_enabled(self, api, data, settings, monkeypatch):
        settings.GTD_CLOUD_SYNC = True
        pulled = []
        monkeypatch.setattr("gtd_api.mobile_views.pull_latest", lambda root: pulled.append(root))
        monkeypatch.setattr("gtd_api.mobile_views.commit_and_push", lambda root, message=None: None)
        api.get("/api/envs/home/inbox/")
        assert settings.BASE_DIR in pulled

    def test_no_sync_when_disabled(self, api, data, settings, monkeypatch):
        settings.GTD_CLOUD_SYNC = False
        pulled = []
        monkeypatch.setattr("gtd_api.mobile_views.pull_latest", lambda root: pulled.append(root))
        api.get("/api/envs/home/inbox/")
        assert pulled == []
