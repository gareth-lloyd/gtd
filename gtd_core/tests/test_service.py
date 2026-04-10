from datetime import date, datetime

import pytest

from gtd_core.models import Bucket, Project
from gtd_core.service import GtdService, slugify


@pytest.fixture
def data_root(tmp_path):
    for env in ["work", "home"]:
        env_dir = tmp_path / env
        for bucket in [
            "inbox", "next", "waiting", "someday", "reference", "projects", "archive", "trash",
        ]:
            (env_dir / bucket).mkdir(parents=True)
        (env_dir / "config.yml").write_text(
            f"name: {env}\n"
            "contexts: [calls, computer, errands, office]\n"
            "areas: [engineering, health]\n"
            "default_energy: medium\n"
        )
    return tmp_path


@pytest.fixture
def svc(data_root):
    fixed_now = datetime(2026, 4, 10, 9, 15)
    return GtdService(data_root, now=lambda: fixed_now)


class TestSlugify:
    def test_simple(self):
        assert slugify("Call dentist") == "call-dentist"

    def test_punctuation(self):
        assert slugify("Email Sarah — re: Q2 plans") == "email-sarah-re-q2-plans"

    def test_empty(self):
        assert slugify("") == "untitled"

    def test_truncates(self):
        result = slugify("a" * 100, max_len=10)
        assert len(result) == 10


class TestListEnvs:
    def test_discovers_both(self, svc):
        assert set(svc.list_envs()) == {"work", "home"}

    def test_ignores_dotfiles_and_non_dirs(self, data_root, svc):
        (data_root / ".git").mkdir()
        (data_root / "somefile.txt").write_text("")
        assert set(svc.list_envs()) == {"work", "home"}


class TestCapture:
    def test_creates_in_inbox(self, svc, data_root):
        item = svc.capture("work", "Call dentist")
        assert item.status == Bucket.INBOX
        assert item.title == "Call dentist"
        assert item.id == "2026-04-10T0915-call-dentist"
        assert (data_root / "work" / "inbox" / f"{item.id}.md").exists()

    def test_with_body(self, svc):
        item = svc.capture("work", "Research", body="About the tax code")
        assert item.body == "About the tax code"

    def test_with_defaults(self, svc):
        """Capture can set energy/time/contexts at creation time."""
        item = svc.capture(
            "work",
            "Quick thing",
            energy="low",
            time_minutes=5,
            contexts=["calls"],
        )
        assert item.energy == "low"
        assert item.time_minutes == 5
        assert item.contexts == ["calls"]

    def test_capture_rejects_invalid_context(self, svc):
        with pytest.raises(ValueError, match="unknown context"):
            svc.capture("work", "Test", contexts=["bogus"])


class TestMove:
    def test_move_to_next(self, svc):
        item = svc.capture("work", "Test")
        moved = svc.move("work", item.id, Bucket.NEXT)
        assert moved.status == Bucket.NEXT


class TestComplete:
    def test_moves_to_archive(self, svc):
        item = svc.capture("work", "Done thing")
        svc.move("work", item.id, Bucket.NEXT)
        completed = svc.complete("work", item.id)
        assert completed.status == Bucket.ARCHIVE


class TestDelete:
    def test_delete_moves_to_trash(self, svc, data_root):
        item = svc.capture("work", "Regrettable item")
        deleted = svc.delete("work", item.id)
        assert deleted.status == Bucket.TRASH
        assert not (data_root / "work" / "inbox" / f"{item.id}.md").exists()
        assert (data_root / "work" / "trash" / f"{item.id}.md").exists()

    def test_delete_is_reversible_via_move(self, svc):
        item = svc.capture("work", "Change my mind")
        svc.delete("work", item.id)
        restored = svc.move("work", item.id, Bucket.INBOX)
        assert restored.status == Bucket.INBOX

    def test_default_list_excludes_trash(self, svc):
        item = svc.capture("work", "Gone")
        svc.delete("work", item.id)
        items = svc.repo("work").list_items()
        assert item.id not in {i.id for i in items}


class TestPurge:
    def test_purge_removes_file_hard(self, svc, data_root):
        item = svc.capture("work", "Delete me")
        svc.delete("work", item.id)  # → trash
        svc.purge("work", item.id)
        assert not (data_root / "work" / "trash" / f"{item.id}.md").exists()

    def test_purge_missing_raises(self, svc):
        import pytest
        with pytest.raises(KeyError):
            svc.purge("work", "nope")


class TestUpdate:
    def test_patch_fields(self, svc):
        item = svc.capture("work", "Test")
        updated = svc.update(
            "work",
            item.id,
            {"contexts": ["calls"], "energy": "low", "time_minutes": 5},
        )
        assert updated.contexts == ["calls"]
        assert updated.energy == "low"
        assert updated.time_minutes == 5

    def test_patch_rejects_invalid_context(self, svc):
        item = svc.capture("work", "Test")
        with pytest.raises(ValueError, match="unknown context"):
            svc.update("work", item.id, {"contexts": ["invalid"]})

    def test_patch_rejects_invalid_area(self, svc):
        item = svc.capture("work", "Test")
        with pytest.raises(ValueError, match="unknown area"):
            svc.update("work", item.id, {"area": "bogus"})

    def test_patch_cannot_change_status(self, svc):
        item = svc.capture("work", "Test")
        with pytest.raises(ValueError, match="status"):
            svc.update("work", item.id, {"status": "next"})

    def test_patch_cannot_change_id(self, svc):
        item = svc.capture("work", "Test")
        with pytest.raises(ValueError, match="immutable"):
            svc.update("work", item.id, {"id": "hacked"})

    def test_patch_bumps_updated(self, svc):
        item = svc.capture("work", "Test")
        original_updated = item.updated
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        updated = svc.update("work", item.id, {"title": "New"})
        assert updated.updated > original_updated


class TestFilterNext:
    def test_empty(self, svc):
        assert svc.filter_next("work") == []

    def test_by_context(self, svc):
        a = svc.capture("work", "Item A")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"contexts": ["calls"]})
        b = svc.capture("work", "Item B")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"contexts": ["computer"]})
        results = svc.filter_next("work", contexts=["calls"])
        assert {r.id for r in results} == {a.id}

    def test_by_contexts_or(self, svc):
        a = svc.capture("work", "A")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"contexts": ["calls"]})
        b = svc.capture("work", "B")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"contexts": ["computer"]})
        results = svc.filter_next("work", contexts=["calls", "computer"])
        assert {r.id for r in results} == {a.id, b.id}

    def test_by_max_minutes(self, svc):
        a = svc.capture("work", "Quick")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"time_minutes": 5})
        b = svc.capture("work", "Long")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"time_minutes": 60})
        results = svc.filter_next("work", max_minutes=15)
        assert {r.id for r in results} == {a.id}

    def test_max_minutes_excludes_unknown(self, svc):
        """Items with no time estimate are excluded from max_minutes filter."""
        a = svc.capture("work", "Quick")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"time_minutes": 5})
        b = svc.capture("work", "Unknown")
        svc.move("work", b.id, Bucket.NEXT)
        results = svc.filter_next("work", max_minutes=15)
        assert {r.id for r in results} == {a.id}

    def test_by_energy_ceiling(self, svc):
        a = svc.capture("work", "Low")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"energy": "low"})
        b = svc.capture("work", "High")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"energy": "high"})
        results = svc.filter_next("work", energy="low")
        assert {r.id for r in results} == {a.id}
        results = svc.filter_next("work", energy="high")
        assert {r.id for r in results} == {a.id, b.id}

    def test_hides_deferred(self, svc):
        a = svc.capture("work", "Now")
        svc.move("work", a.id, Bucket.NEXT)
        b = svc.capture("work", "Later")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"defer_until": date(2026, 6, 1)})
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id}

    def test_include_deferred(self, svc):
        a = svc.capture("work", "Now")
        svc.move("work", a.id, Bucket.NEXT)
        b = svc.capture("work", "Later")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"defer_until": date(2026, 6, 1)})
        results = svc.filter_next("work", include_deferred=True)
        assert {r.id for r in results} == {a.id, b.id}


class TestActionsForProject:
    def test_returns_linked_items(self, svc):
        svc.save_project("work", Project(
            id="p1", title="P1", body="",
            created=datetime(2026, 3, 1), updated=datetime(2026, 3, 1),
        ))
        a = svc.capture("work", "Action A")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"project": "p1"})
        unrelated = svc.capture("work", "Other")
        svc.move("work", unrelated.id, Bucket.NEXT)
        results = svc.actions_for_project("work", "p1")
        assert {r.id for r in results} == {a.id}


class TestEnvIsolation:
    def test_capture_in_different_envs(self, svc, data_root):
        w = svc.capture("work", "Work item")
        h = svc.capture("home", "Home item")
        assert (data_root / "work" / "inbox" / f"{w.id}.md").exists()
        assert (data_root / "home" / "inbox" / f"{h.id}.md").exists()
        assert svc.filter_next("work") == []
        assert svc.filter_next("home") == []
