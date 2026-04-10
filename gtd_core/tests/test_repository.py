from datetime import datetime

import pytest

from gtd_core.models import Bucket, Item, Project
from gtd_core.repository import EnvRepository


@pytest.fixture
def env_root(tmp_path):
    work = tmp_path / "work"
    for bucket in [
        "inbox", "next", "waiting", "someday", "reference", "projects", "archive", "trash",
    ]:
        (work / bucket).mkdir(parents=True)
    (work / "config.yml").write_text(
        "name: work\n"
        "contexts: [calls, computer]\n"
        "areas: [engineering]\n"
        "default_energy: medium\n"
    )
    return tmp_path


@pytest.fixture
def repo(env_root):
    return EnvRepository(env_root, "work")


def _make_item(item_id: str, status: Bucket = Bucket.INBOX) -> Item:
    return Item(
        id=item_id,
        title=f"Title for {item_id}",
        body="",
        created=datetime(2026, 4, 10, 9, 0),
        updated=datetime(2026, 4, 10, 9, 0),
        status=status,
    )


class TestSaveAndGet:
    def test_save_creates_file(self, repo, env_root):
        repo.save(_make_item("test1"))
        assert (env_root / "work" / "inbox" / "test1.md").exists()

    def test_get_returns_item(self, repo):
        repo.save(_make_item("test1"))
        loaded = repo.get("test1")
        assert loaded is not None
        assert loaded.id == "test1"
        assert loaded.status == Bucket.INBOX

    def test_get_missing_returns_none(self, repo):
        assert repo.get("nonexistent") is None

    def test_save_in_next_bucket(self, repo, env_root):
        repo.save(_make_item("n1", status=Bucket.NEXT))
        assert (env_root / "work" / "next" / "n1.md").exists()
        loaded = repo.get("n1")
        assert loaded is not None
        assert loaded.status == Bucket.NEXT

    def test_save_updates_existing(self, repo):
        item = _make_item("upd")
        repo.save(item)
        item.title = "Updated title"
        repo.save(item)
        loaded = repo.get("upd")
        assert loaded is not None
        assert loaded.title == "Updated title"


class TestListItems:
    def test_empty_repo(self, repo):
        assert repo.list_items() == []

    def test_list_all_excludes_archive_and_trash(self, repo):
        repo.save(_make_item("a", Bucket.INBOX))
        repo.save(_make_item("b", Bucket.NEXT))
        repo.save(_make_item("c", Bucket.ARCHIVE))
        repo.save(_make_item("d", Bucket.TRASH))
        ids = {i.id for i in repo.list_items()}
        assert ids == {"a", "b"}

    def test_list_include_archive(self, repo):
        repo.save(_make_item("a", Bucket.INBOX))
        repo.save(_make_item("c", Bucket.ARCHIVE))
        ids = {i.id for i in repo.list_items(include_archive=True)}
        assert ids == {"a", "c"}

    def test_list_include_trash(self, repo):
        repo.save(_make_item("a", Bucket.INBOX))
        repo.save(_make_item("d", Bucket.TRASH))
        ids = {i.id for i in repo.list_items(include_trash=True)}
        assert ids == {"a", "d"}

    def test_list_by_bucket(self, repo):
        repo.save(_make_item("a", Bucket.INBOX))
        repo.save(_make_item("b", Bucket.NEXT))
        ids = {i.id for i in repo.list_items(bucket=Bucket.NEXT)}
        assert ids == {"b"}


class TestMove:
    def test_move_updates_bucket_and_file(self, repo, env_root):
        repo.save(_make_item("m1", Bucket.INBOX))
        moved = repo.move("m1", Bucket.NEXT)
        assert moved.status == Bucket.NEXT
        assert not (env_root / "work" / "inbox" / "m1.md").exists()
        assert (env_root / "work" / "next" / "m1.md").exists()
        reloaded = repo.get("m1")
        assert reloaded is not None
        assert reloaded.status == Bucket.NEXT

    def test_move_to_same_bucket_is_noop(self, repo, env_root):
        repo.save(_make_item("same", Bucket.NEXT))
        repo.move("same", Bucket.NEXT)
        assert (env_root / "work" / "next" / "same.md").exists()

    def test_move_missing_raises(self, repo):
        with pytest.raises(KeyError):
            repo.move("nonexistent", Bucket.NEXT)


class TestDelete:
    def test_delete_removes_file(self, repo, env_root):
        repo.save(_make_item("d1"))
        repo.delete("d1")
        assert not (env_root / "work" / "inbox" / "d1.md").exists()

    def test_delete_missing_raises(self, repo):
        with pytest.raises(KeyError):
            repo.delete("nonexistent")


class TestConfig:
    def test_load_config(self, repo):
        cfg = repo.load_config()
        assert cfg.name == "work"
        assert "calls" in cfg.contexts
        assert "engineering" in cfg.areas


class TestProjects:
    def _make_project(self, project_id: str) -> Project:
        return Project(
            id=project_id,
            title=f"Project {project_id}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
        )

    def test_save_and_list(self, repo):
        repo.save_project(self._make_project("p1"))
        repo.save_project(self._make_project("p2"))
        projects = repo.list_projects()
        assert {p.id for p in projects} == {"p1", "p2"}

    def test_get_project(self, repo):
        repo.save_project(self._make_project("p1"))
        loaded = repo.get_project("p1")
        assert loaded is not None
        assert loaded.id == "p1"

    def test_get_missing_project(self, repo):
        assert repo.get_project("nope") is None

    def test_delete_project(self, repo):
        repo.save_project(self._make_project("p1"))
        repo.delete_project("p1")
        assert repo.get_project("p1") is None

    def test_delete_missing_project_raises(self, repo):
        with pytest.raises(KeyError):
            repo.delete_project("nope")
