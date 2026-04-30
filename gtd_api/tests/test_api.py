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
    for env_name in ["work", "home"]:
        make_env(data, env_name)
        initial_files.append(str((data / env_name / "config.yml").relative_to(tmp_path)))

    (tmp_path / "README.md").write_text("test\n")
    repo.index.add(initial_files)
    repo.index.commit("initial")

    settings.BASE_DIR = tmp_path
    settings.GTD_DATA_ROOT = data
    return tmp_path


@pytest.fixture
def api(tmp_project):
    return APIClient()


class TestEnvs:
    def test_list_envs(self, api):
        r = api.get("/api/envs/")
        assert r.status_code == 200
        names = {e["name"] for e in r.json()}
        assert names == {"work", "home"}

    def test_env_config(self, api):
        r = api.get("/api/envs/work/config/")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "work"
        assert "calls" in data["contexts"]
        assert "engineering" in data["areas"]

    def test_env_config_missing(self, api):
        r = api.get("/api/envs/nope/config/")
        assert r.status_code == 404


class TestItems:
    def test_capture_creates_in_inbox(self, api):
        r = api.post("/api/envs/work/items/", {"title": "Test"}, format="json")
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "Test"
        assert data["status"] == "inbox"
        assert data["id"]

    def test_capture_with_body(self, api):
        r = api.post(
            "/api/envs/work/items/",
            {"title": "Test", "body": "Some notes"},
            format="json",
        )
        assert r.status_code == 201
        assert r.json()["body"] == "Some notes"

    def test_capture_at_top_assigns_negative_order(self, api):
        api.post("/api/envs/work/items/", {"title": "Bottom"}, format="json")
        r = api.post(
            "/api/envs/work/items/",
            {"title": "Top", "at_top": True},
            format="json",
        )
        assert r.status_code == 201
        data = r.json()
        assert data["title"] == "Top"
        assert data["order"] == -1

        listing = api.get("/api/envs/work/items/?status=inbox").json()
        titles = [i["title"] for i in listing]
        assert titles[0] == "Top"
        assert "Bottom" in titles[1:]

    def test_capture_with_source_id_persists_it(self, api):
        url = "https://github.com/canary-technologies-corp/canary/pull/40386"
        r = api.post(
            "/api/envs/work/items/",
            {"title": "Review PR 40386", "source_id": url},
            format="json",
        )
        assert r.status_code == 201
        data = r.json()
        assert data["source_id"] == url

        got = api.get(f"/api/envs/work/items/{data['id']}/").json()
        assert got["source_id"] == url

    def test_patch_can_backfill_source_id(self, api):
        created = api.post(
            "/api/envs/work/items/", {"title": "Legacy"}, format="json"
        ).json()
        assert created["source_id"] is None
        r = api.patch(
            f"/api/envs/work/items/{created['id']}/",
            {"source_id": "ENT-1234"},
            format="json",
        )
        assert r.status_code == 200
        assert r.json()["source_id"] == "ENT-1234"

    def test_list_items_filter_by_status(self, api):
        a = api.post("/api/envs/work/items/", {"title": "A"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/move/", {"to": "next"}, format="json")
        api.post("/api/envs/work/items/", {"title": "B"}, format="json")

        r = api.get("/api/envs/work/items/?status=next")
        assert r.status_code == 200
        ids = {i["id"] for i in r.json()}
        assert ids == {a["id"]}

    def test_list_all_excludes_archive(self, api):
        a = api.post("/api/envs/work/items/", {"title": "A"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/complete/")

        r = api.get("/api/envs/work/items/")
        ids = {i["id"] for i in r.json()}
        assert a["id"] not in ids

    def test_get_item(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.get(f"/api/envs/work/items/{created['id']}/")
        assert r.status_code == 200
        assert r.json()["id"] == created["id"]

    def test_get_missing(self, api):
        r = api.get("/api/envs/work/items/nonexistent/")
        assert r.status_code == 404

    def test_update_item(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.patch(
            f"/api/envs/work/items/{created['id']}/",
            {"contexts": ["calls"], "energy": "low", "time_minutes": 5},
            format="json",
        )
        assert r.status_code == 200
        data = r.json()
        assert data["contexts"] == ["calls"]
        assert data["energy"] == "low"
        assert data["time_minutes"] == 5

    def test_update_rejects_invalid_context(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.patch(
            f"/api/envs/work/items/{created['id']}/",
            {"contexts": ["bogus"]},
            format="json",
        )
        assert r.status_code == 400
        assert "context" in r.json()["error"]

    def test_move_item(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.post(
            f"/api/envs/work/items/{created['id']}/move/",
            {"to": "next"},
            format="json",
        )
        assert r.status_code == 200
        assert r.json()["status"] == "next"

    def test_move_invalid_bucket(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.post(
            f"/api/envs/work/items/{created['id']}/move/",
            {"to": "projects"},
            format="json",
        )
        assert r.status_code == 400

    def test_complete_item(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.post(f"/api/envs/work/items/{created['id']}/complete/")
        assert r.status_code == 200
        assert r.json()["status"] == "archive"

    def test_delete_soft_deletes_to_trash(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        r = api.delete(f"/api/envs/work/items/{created['id']}/")
        assert r.status_code == 200
        assert r.json()["status"] == "trash"

        # Item is still findable (now in trash), not in default list
        r = api.get(f"/api/envs/work/items/{created['id']}/")
        assert r.status_code == 200
        assert r.json()["status"] == "trash"
        r = api.get("/api/envs/work/items/")
        assert created["id"] not in {i["id"] for i in r.json()}

    def test_purge_hard_deletes(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        api.delete(f"/api/envs/work/items/{created['id']}/")  # → trash
        r = api.post(f"/api/envs/work/items/{created['id']}/purge/")
        assert r.status_code == 204
        r = api.get(f"/api/envs/work/items/{created['id']}/")
        assert r.status_code == 404

    def test_move_out_of_trash(self, api):
        created = api.post("/api/envs/work/items/", {"title": "T"}, format="json").json()
        api.delete(f"/api/envs/work/items/{created['id']}/")
        r = api.post(
            f"/api/envs/work/items/{created['id']}/move/",
            {"to": "inbox"},
            format="json",
        )
        assert r.status_code == 200
        assert r.json()["status"] == "inbox"

    def test_filter_by_context_query_param(self, api):
        a = api.post("/api/envs/work/items/", {"title": "A"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{a['id']}/", {"contexts": ["calls"]}, format="json")

        b = api.post("/api/envs/work/items/", {"title": "B"}, format="json").json()
        api.post(f"/api/envs/work/items/{b['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{b['id']}/", {"contexts": ["computer"]}, format="json")

        r = api.get("/api/envs/work/items/?status=next&contexts=calls")
        ids = {i["id"] for i in r.json()}
        assert ids == {a["id"]}

    def test_filter_by_max_minutes(self, api):
        a = api.post("/api/envs/work/items/", {"title": "A"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{a['id']}/", {"time_minutes": 5}, format="json")

        b = api.post("/api/envs/work/items/", {"title": "B"}, format="json").json()
        api.post(f"/api/envs/work/items/{b['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{b['id']}/", {"time_minutes": 60}, format="json")

        r = api.get("/api/envs/work/items/?status=next&max_minutes=15")
        ids = {i["id"] for i in r.json()}
        assert ids == {a["id"]}

    def test_filter_by_min_minutes(self, api):
        a = api.post("/api/envs/work/items/", {"title": "Quick"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{a['id']}/", {"time_minutes": 30}, format="json")

        b = api.post("/api/envs/work/items/", {"title": "Long"}, format="json").json()
        api.post(f"/api/envs/work/items/{b['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{b['id']}/", {"time_minutes": 180}, format="json")

        r = api.get("/api/envs/work/items/?status=next&min_minutes=120")
        ids = {i["id"] for i in r.json()}
        assert ids == {b["id"]}

    def test_next_items_include_project_priority(self, api):
        api.post(
            "/api/envs/work/projects/",
            {"id": "p1proj", "title": "P1", "priority": 1},
            format="json",
        )
        a = api.post("/api/envs/work/items/", {"title": "A"}, format="json").json()
        api.post(f"/api/envs/work/items/{a['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{a['id']}/", {"project": "p1proj"}, format="json")

        # Floating item with no project
        b = api.post("/api/envs/work/items/", {"title": "B"}, format="json").json()
        api.post(f"/api/envs/work/items/{b['id']}/move/", {"to": "next"}, format="json")

        r = api.get("/api/envs/work/items/?status=next")
        by_id = {i["id"]: i for i in r.json()}
        assert by_id[a["id"]]["project_priority"] == 1
        assert by_id[b["id"]]["project_priority"] is None

    def test_next_items_sorted_by_project_priority(self, api):
        api.post(
            "/api/envs/work/projects/",
            {"id": "p3proj", "title": "P3", "priority": 3},
            format="json",
        )
        api.post(
            "/api/envs/work/projects/",
            {"id": "p1proj", "title": "P1", "priority": 1},
            format="json",
        )
        # Capture P3 first (earlier id), then P1
        p3_item = api.post("/api/envs/work/items/", {"title": "P3 task"}, format="json").json()
        api.post(f"/api/envs/work/items/{p3_item['id']}/move/", {"to": "next"}, format="json")
        api.patch(
            f"/api/envs/work/items/{p3_item['id']}/",
            {"project": "p3proj"},
            format="json",
        )
        p1_item = api.post("/api/envs/work/items/", {"title": "P1 task"}, format="json").json()
        api.post(f"/api/envs/work/items/{p1_item['id']}/move/", {"to": "next"}, format="json")
        api.patch(
            f"/api/envs/work/items/{p1_item['id']}/",
            {"project": "p1proj"},
            format="json",
        )

        r = api.get("/api/envs/work/items/?status=next")
        ordered = [i["id"] for i in r.json()]
        assert ordered.index(p1_item["id"]) < ordered.index(p3_item["id"])


class TestProjects:
    def test_list_empty(self, api):
        r = api.get("/api/envs/work/projects/")
        assert r.status_code == 200
        assert r.json() == []

    def test_create_and_list(self, api):
        r = api.post(
            "/api/envs/work/projects/",
            {"id": "p1", "title": "Project one", "body": "notes"},
            format="json",
        )
        assert r.status_code == 201

        r = api.get("/api/envs/work/projects/")
        data = r.json()
        assert len(data) == 1
        assert data[0]["id"] == "p1"

    def test_get_project_with_actions(self, api):
        api.post(
            "/api/envs/work/projects/",
            {"id": "p1", "title": "Project one"},
            format="json",
        )
        action = api.post("/api/envs/work/items/", {"title": "Action"}, format="json").json()
        api.post(f"/api/envs/work/items/{action['id']}/move/", {"to": "next"}, format="json")
        api.patch(f"/api/envs/work/items/{action['id']}/", {"project": "p1"}, format="json")

        r = api.get("/api/envs/work/projects/p1/")
        assert r.status_code == 200
        data = r.json()
        assert data["project"]["id"] == "p1"
        assert len(data["actions"]) == 1
        assert data["actions"][0]["id"] == action["id"]

    def test_get_missing_project(self, api):
        r = api.get("/api/envs/work/projects/nope/")
        assert r.status_code == 404

    def test_list_hides_complete_by_default(self, api):
        api.post("/api/envs/work/projects/", {"id": "active1", "title": "Active"}, format="json")
        api.post("/api/envs/work/projects/", {"id": "done1", "title": "Done"}, format="json")
        api.patch("/api/envs/work/projects/done1/", {"status": "complete"}, format="json")

        r = api.get("/api/envs/work/projects/")
        ids = {p["id"] for p in r.json()}
        assert ids == {"active1"}

    def test_list_include_inactive(self, api):
        api.post("/api/envs/work/projects/", {"id": "active1", "title": "Active"}, format="json")
        api.post("/api/envs/work/projects/", {"id": "done1", "title": "Done"}, format="json")
        api.patch("/api/envs/work/projects/done1/", {"status": "complete"}, format="json")

        r = api.get("/api/envs/work/projects/?include_inactive=true")
        ids = {p["id"] for p in r.json()}
        assert ids == {"active1", "done1"}

    def test_patch_project_status(self, api):
        api.post("/api/envs/work/projects/", {"id": "p1", "title": "P"}, format="json")
        r = api.patch("/api/envs/work/projects/p1/", {"status": "complete"}, format="json")
        assert r.status_code == 200
        assert r.json()["status"] == "complete"

    def test_patch_project_invalid_status(self, api):
        api.post("/api/envs/work/projects/", {"id": "p1", "title": "P"}, format="json")
        r = api.patch("/api/envs/work/projects/p1/", {"status": "bogus"}, format="json")
        assert r.status_code == 400

    def test_delete_project(self, api):
        api.post("/api/envs/work/projects/", {"id": "p1", "title": "P"}, format="json")
        r = api.delete("/api/envs/work/projects/p1/")
        assert r.status_code == 204
        r = api.get("/api/envs/work/projects/p1/")
        assert r.status_code == 404


class TestTemplates:
    def test_list_empty(self, api):
        r = api.get("/api/envs/work/templates/")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_returns_templates_with_next_due(self, api, tmp_project):
        from datetime import date, timedelta

        from gtd_core.models import Template
        from gtd_core.recurring import next_upcoming_spawn_date
        from gtd_core.repository import EnvRepository

        # Anchor weekly template on the Monday two weeks before today so the
        # test is stable regardless of when it runs.
        today = date.today()
        past_monday = today - timedelta(days=today.weekday() + 14)
        expected_next = next_upcoming_spawn_date("weekly", past_monday, today)

        repo = EnvRepository(tmp_project / "data", "work")
        repo.save_template(
            Template(
                id="weekly-standup-prep",
                title="Prep for weekly standup",
                body="Review backlog",
                contexts=["computer"],
                energy="medium",
                time_minutes=15,
                recurrence="weekly",
                last_spawned=past_monday,
            )
        )
        repo.save_template(
            Template(
                id="unspawned",
                title="Never spawned",
                body="",
                recurrence="daily",
                last_spawned=None,
            )
        )

        r = api.get("/api/envs/work/templates/")
        assert r.status_code == 200
        data = sorted(r.json(), key=lambda t: t["id"])
        assert [t["id"] for t in data] == ["unspawned", "weekly-standup-prep"]
        never = next(t for t in data if t["id"] == "unspawned")
        weekly = next(t for t in data if t["id"] == "weekly-standup-prep")
        assert never["next_due"] == "now"
        assert never["last_spawned"] is None
        assert weekly["next_due"] == expected_next.isoformat()
        assert weekly["recurrence"] == "weekly"
        assert weekly["time_minutes"] == 15
        assert weekly["contexts"] == ["computer"]

    def test_list_unknown_env_404(self, api):
        r = api.get("/api/envs/nope/templates/")
        assert r.status_code == 404


class TestSnapshot:
    def test_status_clean(self, api):
        r = api.get("/api/snapshot/status/")
        assert r.status_code == 200
        assert r.json()["dirty_count"] == 0

    def test_status_dirty_after_capture(self, api):
        api.post("/api/envs/work/items/", {"title": "T"}, format="json")
        r = api.get("/api/snapshot/status/")
        assert r.status_code == 200
        assert r.json()["dirty_count"] == 1

    def test_snapshot_commit(self, api, tmp_project):
        api.post("/api/envs/work/items/", {"title": "T"}, format="json")
        r = api.post("/api/snapshot/", {"message": "test snapshot"}, format="json")
        assert r.status_code == 200
        data = r.json()
        assert data["committed"] is True
        assert data["sha"] is not None
        assert data["files_changed"] == 1

        repo = git.Repo(tmp_project)
        assert repo.head.commit.message.startswith("test snapshot")

    def test_snapshot_noop(self, api):
        r = api.post("/api/snapshot/", {}, format="json")
        assert r.status_code == 200
        assert r.json()["committed"] is False
