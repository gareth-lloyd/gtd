import logging
import os
from datetime import datetime

import pytest

from gtd_core.models import Bucket, Item, Project
from gtd_core.repository import EnvRepository


@pytest.fixture
def repo(data_root):
    return EnvRepository(data_root, "work")


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
    def test_save_creates_file(self, repo, data_root):
        repo.save(_make_item("test1"))
        assert (data_root / "work" / "inbox" / "test1.md").exists()

    def test_get_returns_item(self, repo):
        repo.save(_make_item("test1"))
        loaded = repo.get("test1")
        assert loaded is not None
        assert loaded.id == "test1"
        assert loaded.status == Bucket.INBOX

    def test_get_missing_returns_none(self, repo):
        assert repo.get("nonexistent") is None

    def test_save_in_next_bucket(self, repo, data_root):
        repo.save(_make_item("n1", status=Bucket.NEXT))
        assert (data_root / "work" / "next" / "n1.md").exists()
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
    def test_move_updates_bucket_and_file(self, repo, data_root):
        repo.save(_make_item("m1", Bucket.INBOX))
        moved = repo.move("m1", Bucket.NEXT)
        assert moved.status == Bucket.NEXT
        assert not (data_root / "work" / "inbox" / "m1.md").exists()
        assert (data_root / "work" / "next" / "m1.md").exists()
        reloaded = repo.get("m1")
        assert reloaded is not None
        assert reloaded.status == Bucket.NEXT

    def test_move_to_same_bucket_is_noop(self, repo, data_root):
        repo.save(_make_item("same", Bucket.NEXT))
        repo.move("same", Bucket.NEXT)
        assert (data_root / "work" / "next" / "same.md").exists()

    def test_move_missing_raises(self, repo):
        with pytest.raises(KeyError):
            repo.move("nonexistent", Bucket.NEXT)

    def test_relocate_failure_keeps_item_in_source_bucket(self, repo, data_root, monkeypatch):
        """If `os.replace` raises mid-relocate, the source file must remain
        intact and no orphan must appear in the destination."""
        import gtd_core.repository as repository

        repo.save(_make_item("atomic", Bucket.INBOX))
        item = repo.get("atomic")
        assert item is not None

        def boom(*_args, **_kwargs):
            raise OSError("simulated rename failure")

        monkeypatch.setattr(repository.os, "replace", boom)
        with pytest.raises(OSError, match="simulated"):
            repo.relocate(item, Bucket.NEXT)

        assert (data_root / "work" / "inbox" / "atomic.md").exists()
        assert not (data_root / "work" / "next" / "atomic.md").exists()

    def test_relocate_overwrites_dest_corpse(self, repo, data_root):
        """If a stale file exists at the destination (e.g. from a prior crash),
        relocate uses os.replace which overwrites it cleanly."""
        # Drop a stale corpse directly into the destination.
        corpse_path = data_root / "work" / "next" / "rebirth.md"
        corpse_path.parent.mkdir(parents=True, exist_ok=True)
        corpse_path.write_text(
            "---\nid: rebirth\ntitle: stale\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n"
        )
        # Save the live item in inbox, then relocate it to next.
        repo.save(_make_item("rebirth", Bucket.INBOX))
        live = repo.get("rebirth")
        assert live is not None
        repo.relocate(live, Bucket.NEXT)
        # File now in next, source gone, content is the live one.
        assert not (data_root / "work" / "inbox" / "rebirth.md").exists()
        assert corpse_path.exists()
        loaded = repo.get("rebirth")
        assert loaded is not None
        assert loaded.title == "Title for rebirth"


class TestReserveId:
    def test_no_collision_returns_base(self, repo):
        assert repo.reserve_id("2026-04-10T0915-foo") == "2026-04-10T0915-foo"

    def test_collision_in_inbox_suffixes(self, repo):
        repo.save(_make_item("2026-04-10T0915-foo", Bucket.INBOX))
        assert repo.reserve_id("2026-04-10T0915-foo") == "2026-04-10T0915-foo-2"

    def test_collision_in_archive_still_suffixes(self, repo):
        # Soft-deleted corpses must not be silently overwritten by a fresh capture.
        repo.save(_make_item("2026-04-10T0915-foo", Bucket.ARCHIVE))
        assert repo.reserve_id("2026-04-10T0915-foo") == "2026-04-10T0915-foo-2"

    def test_collision_in_trash_still_suffixes(self, repo):
        repo.save(_make_item("2026-04-10T0915-foo", Bucket.TRASH))
        assert repo.reserve_id("2026-04-10T0915-foo") == "2026-04-10T0915-foo-2"

    def test_chains_to_dash_3(self, repo):
        repo.save(_make_item("2026-04-10T0915-foo", Bucket.INBOX))
        repo.save(_make_item("2026-04-10T0915-foo-2", Bucket.NEXT))
        assert repo.reserve_id("2026-04-10T0915-foo") == "2026-04-10T0915-foo-3"


class TestDelete:
    def test_delete_removes_file(self, repo, data_root):
        repo.save(_make_item("d1"))
        repo.delete("d1")
        assert not (data_root / "work" / "inbox" / "d1.md").exists()

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
    def _make_project(self, project_id: str, status: str = "active") -> Project:
        return Project(
            id=project_id,
            title=f"Project {project_id}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            status=status,  # type: ignore[arg-type]
        )

    def test_save_and_list(self, repo):
        repo.save_project(self._make_project("p1"))
        repo.save_project(self._make_project("p2"))
        projects = repo.list_projects()
        assert {p.id for p in projects} == {"p1", "p2"}

    def test_list_excludes_complete_by_default(self, repo):
        repo.save_project(self._make_project("active1"))
        repo.save_project(self._make_project("hold1", status="on_hold"))
        repo.save_project(self._make_project("done1", status="complete"))
        repo.save_project(self._make_project("drop1", status="dropped"))
        ids = {p.id for p in repo.list_projects()}
        assert ids == {"active1", "hold1"}

    def test_list_include_inactive(self, repo):
        repo.save_project(self._make_project("a1"))
        repo.save_project(self._make_project("done1", status="complete"))
        repo.save_project(self._make_project("drop1", status="dropped"))
        ids = {p.id for p in repo.list_projects(include_inactive=True)}
        assert ids == {"a1", "done1", "drop1"}

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


class TestUnloadableFilesAreSkipped:
    """A single broken YAML file must not 500 every list endpoint.

    Storage parses YAML on load — a quote, tab, or hand-edit mistake in one
    file would otherwise raise straight out of the list comprehension and
    take the whole bucket (and the API) down with it.
    """

    def _write_broken(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Unbalanced quote in the title — yaml will refuse to parse this.
        path.write_text('---\nid: broken\ntitle: "unbalanced\ncreated: 2026-04-10\n---\nbody\n')

    def test_list_items_skips_unloadable_file(self, repo, data_root, caplog):
        repo.save(_make_item("good", Bucket.INBOX))
        self._write_broken(data_root / "work" / "inbox" / "broken.md")

        with caplog.at_level(logging.WARNING, logger="gtd_core.repository"):
            items = repo.list_items(bucket=Bucket.INBOX)

        assert {i.id for i in items} == {"good"}
        assert any("broken.md" in rec.message for rec in caplog.records)

    def test_list_items_all_buckets_skips_unloadable(self, repo, data_root):
        repo.save(_make_item("good_inbox", Bucket.INBOX))
        repo.save(_make_item("good_next", Bucket.NEXT))
        self._write_broken(data_root / "work" / "inbox" / "broken.md")

        items = repo.list_items()
        assert {i.id for i in items} == {"good_inbox", "good_next"}

    def test_list_projects_skips_unloadable(self, repo, data_root, caplog):
        from gtd_core.models import Project

        good = Project(
            id="goodproj",
            title="Good",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
        )
        repo.save_project(good)
        self._write_broken(data_root / "work" / "projects" / "bad.md")

        with caplog.at_level(logging.WARNING, logger="gtd_core.repository"):
            projects = repo.list_projects()

        assert {p.id for p in projects} == {"goodproj"}
        assert any("bad.md" in rec.message for rec in caplog.records)

    def test_list_templates_skips_unloadable(self, repo, data_root, caplog):
        from gtd_core.models import Template

        good = Template(
            id="goodtpl",
            title="Good template",
            body="",
            recurrence="weekly",
        )
        repo.save_template(good)
        self._write_broken(data_root / "work" / "templates" / "bad.md")

        with caplog.at_level(logging.WARNING, logger="gtd_core.repository"):
            templates = repo.list_templates()

        assert {t.id for t in templates} == {"goodtpl"}
        assert any("bad.md" in rec.message for rec in caplog.records)


class TestIdIndexCache:
    """`get` is on the hot path of every PATCH/move — used to scan all 7
    buckets calling `path.exists()`. The index drops it to O(1) for the
    common case."""

    def test_get_after_save_finds_item(self, repo):
        repo.save(_make_item("indexed", Bucket.INBOX))
        loaded = repo.get("indexed")
        assert loaded is not None
        assert loaded.status == Bucket.INBOX

    def test_get_after_relocate_returns_correct_bucket(self, repo):
        repo.save(_make_item("hops", Bucket.INBOX))
        item = repo.get("hops")
        assert item is not None
        repo.relocate(item, Bucket.NEXT)
        loaded = repo.get("hops")
        assert loaded is not None
        assert loaded.status == Bucket.NEXT

    def test_get_after_delete_returns_none(self, repo):
        repo.save(_make_item("doomed", Bucket.INBOX))
        repo.delete("doomed")
        assert repo.get("doomed") is None

    def test_get_uses_index_does_not_rescan_filesystem(self, repo, monkeypatch):
        """Once the index is populated, `get` must not rescan bucket dirs."""
        repo.save(_make_item("cached", Bucket.NEXT))
        assert repo.get("cached") is not None

        from gtd_core import repository as repo_mod

        called = {"n": 0}
        original = repo_mod.list_item_paths

        def counted(directory):
            called["n"] += 1
            return original(directory)

        monkeypatch.setattr(repo_mod, "list_item_paths", counted)
        repo.get("cached")
        assert called["n"] == 0

    def test_get_after_index_drift_falls_back_and_recovers(self, repo, data_root):
        """If the index says bucket X but the file is in Y (e.g. external mv),
        `get` should not return None — it must invalidate and rediscover."""
        repo.save(_make_item("drifted", Bucket.INBOX))
        # Prime cache.
        assert repo.get("drifted") is not None
        # Bypass the API and move the file directly on disk.
        os.rename(
            data_root / "work" / "inbox" / "drifted.md",
            data_root / "work" / "next" / "drifted.md",
        )
        loaded = repo.get("drifted")
        assert loaded is not None
        assert loaded.status == Bucket.NEXT
