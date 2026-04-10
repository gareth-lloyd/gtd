import git
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def tmp_project(tmp_path, settings):
    repo = git.Repo.init(tmp_path)
    with repo.config_writer() as cw:
        cw.set_value("user", "email", "test@example.com")
        cw.set_value("user", "name", "Test")

    data = tmp_path / "data"
    initial_files = ["README.md"]
    for env in ["work", "home"]:
        env_dir = data / env
        for bucket in [
            "inbox", "next", "waiting", "someday", "reference", "projects", "archive", "trash",
        ]:
            (env_dir / bucket).mkdir(parents=True)
        cfg = env_dir / "config.yml"
        cfg.write_text(
            f"name: {env}\n"
            "contexts: [calls, computer, errands]\n"
            "areas: [engineering, health]\n"
            "default_energy: medium\n"
        )
        initial_files.append(str(cfg.relative_to(tmp_path)))

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
