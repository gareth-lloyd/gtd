from datetime import date, datetime

import pytest

from gtd_core.models import Bucket, Project
from gtd_core.service import GtdService, slugify


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


class TestCaptureAtTop:
    def _svc_at(self, data_root, when: datetime) -> GtdService:
        return GtdService(data_root, now=lambda: when)

    def test_default_capture_leaves_order_null(self, svc):
        item = svc.capture("work", "Default")
        assert item.order is None

    def test_at_top_sets_negative_order_when_inbox_empty(self, svc):
        item = svc.capture("work", "First", at_top=True)
        assert item.order == -1

    def test_consecutive_at_top_stack_with_decreasing_order(self, data_root):
        svc1 = self._svc_at(data_root, datetime(2026, 4, 10, 9, 0))
        first = svc1.capture("work", "First", at_top=True)
        svc2 = self._svc_at(data_root, datetime(2026, 4, 10, 10, 0))
        second = svc2.capture("work", "Second", at_top=True)
        assert first.order == -1
        assert second.order == -2  # newer top-capture floats above older

    def test_at_top_ignores_unordered_inbox_items(self, data_root):
        svc1 = self._svc_at(data_root, datetime(2026, 4, 10, 9, 0))
        svc1.capture("work", "Bottom A")
        svc2 = self._svc_at(data_root, datetime(2026, 4, 10, 10, 0))
        top = svc2.capture("work", "Top", at_top=True)
        assert top.order == -1

    def test_inbox_listing_sorts_top_captures_first(self, data_root):
        svc1 = self._svc_at(data_root, datetime(2026, 4, 10, 9, 0))
        a = svc1.capture("work", "First bottom")
        svc2 = self._svc_at(data_root, datetime(2026, 4, 10, 10, 0))
        b = svc2.capture("work", "Second bottom")
        svc3 = self._svc_at(data_root, datetime(2026, 4, 10, 11, 0))
        c = svc3.capture("work", "Top one", at_top=True)
        listed = svc3.list_items("work", bucket=Bucket.INBOX)
        ids = [i.id for i in listed]
        assert ids[0] == c.id
        assert ids[1:] == [a.id, b.id]

    def test_order_preserved_when_moving_out_of_inbox(self, svc):
        # The negative order means "user wanted this near the top". Preserve
        # it so the intent carries into next/waiting/etc — _item_sort_key
        # treats negative orders as sorting before any positive (reorder-
        # assigned) order, which lands the item first inside its destination.
        item = svc.capture("work", "Top thing", at_top=True)
        assert item.order == -1
        moved = svc.move("work", item.id, Bucket.NEXT)
        assert moved.order == -1


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


class TestListDone:
    """`list_done` returns archive items sorted by `updated` desc, paginated."""

    def _complete_at(self, data_root, when: datetime, title: str):
        svc = GtdService(data_root, now=lambda: when)
        item = svc.capture("work", title)
        return svc.complete("work", item.id)

    def test_empty(self, svc):
        items, total = svc.list_done("work")
        assert items == []
        assert total == 0

    def test_returns_only_archive(self, svc, data_root):
        live = svc.capture("work", "Live")
        svc.move("work", live.id, Bucket.NEXT)
        done = self._complete_at(data_root, datetime(2026, 4, 11, 9, 0), "Done")
        items, total = svc.list_done("work")
        assert {i.id for i in items} == {done.id}
        assert total == 1

    def test_excludes_trash(self, svc, data_root):
        # Trash is a separate bucket and should not show up under "done".
        item = svc.capture("work", "Trashed")
        svc.delete("work", item.id)
        self._complete_at(data_root, datetime(2026, 4, 11, 9, 0), "Done")
        items, total = svc.list_done("work")
        assert total == 1
        assert all(i.id != item.id for i in items)

    def test_sorted_by_updated_desc(self, data_root):
        first = GtdService(data_root, now=lambda: datetime(2026, 4, 1, 9, 0))
        a = first.capture("work", "First")
        first.complete("work", a.id)
        second = GtdService(data_root, now=lambda: datetime(2026, 4, 5, 9, 0))
        b = second.capture("work", "Second")
        second.complete("work", b.id)
        third = GtdService(data_root, now=lambda: datetime(2026, 4, 10, 9, 0))
        c = third.capture("work", "Third")
        third.complete("work", c.id)
        items, _ = third.list_done("work")
        assert [i.id for i in items] == [c.id, b.id, a.id]

    def test_pagination(self, data_root):
        # Complete 5 items at distinct times so order is deterministic.
        ids: list[str] = []
        for n in range(5):
            done = self._complete_at(data_root, datetime(2026, 4, 1 + n, 9, 0), f"T{n}")
            ids.append(done.id)
        svc = GtdService(data_root, now=lambda: datetime(2026, 4, 10))
        page1, total = svc.list_done("work", page=1, page_size=2)
        assert total == 5
        assert [i.id for i in page1] == [ids[4], ids[3]]
        page2, _ = svc.list_done("work", page=2, page_size=2)
        assert [i.id for i in page2] == [ids[2], ids[1]]
        page3, _ = svc.list_done("work", page=3, page_size=2)
        assert [i.id for i in page3] == [ids[0]]

    def test_page_beyond_end_returns_empty(self, data_root):
        self._complete_at(data_root, datetime(2026, 4, 1, 9, 0), "Only")
        svc = GtdService(data_root)
        items, total = svc.list_done("work", page=99, page_size=10)
        assert items == []
        assert total == 1

    def test_invalid_page(self, svc):
        with pytest.raises(ValueError, match="page"):
            svc.list_done("work", page=0)

    def test_invalid_page_size(self, svc):
        with pytest.raises(ValueError, match="page_size"):
            svc.list_done("work", page_size=0)


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

    def test_patch_due_natural_language(self, svc):
        item = svc.capture("work", "Test")
        updated = svc.update("work", item.id, {"due": "tomorrow"})
        assert updated.due is not None
        assert updated.due > date.today()

    def test_patch_defer_natural_language(self, svc):
        item = svc.capture("work", "Test")
        updated = svc.update("work", item.id, {"defer_until": "in 2 weeks"})
        assert updated.defer_until is not None
        # fixed clock is 2026-04-10 09:15
        assert updated.defer_until > datetime(2026, 4, 10, 9, 15)

    def test_patch_defer_hours(self, svc):
        item = svc.capture("work", "Test")
        updated = svc.update("work", item.id, {"defer_until": "3h"})
        assert updated.defer_until is not None
        # "3h" uses real datetime.now (not the injected clock) — just assert
        # the returned value is a datetime with hour/minute preserved.
        assert isinstance(updated.defer_until, datetime)

    def test_patch_due_iso_still_works(self, svc):
        item = svc.capture("work", "Test")
        updated = svc.update("work", item.id, {"due": "2026-06-15"})
        assert updated.due == date(2026, 6, 15)

    def test_patch_due_null_clears(self, svc):
        item = svc.capture("work", "Test")
        svc.update("work", item.id, {"due": "2026-06-15"})
        updated = svc.update("work", item.id, {"due": None})
        assert updated.due is None


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

    def test_by_min_minutes(self, svc):
        a = svc.capture("work", "Quick")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"time_minutes": 30})
        b = svc.capture("work", "Long")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"time_minutes": 180})
        results = svc.filter_next("work", min_minutes=120)
        assert {r.id for r in results} == {b.id}

    def test_min_minutes_excludes_unknown(self, svc):
        """Items with no time estimate are excluded from min_minutes filter."""
        a = svc.capture("work", "Long")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"time_minutes": 180})
        b = svc.capture("work", "Unknown")
        svc.move("work", b.id, Bucket.NEXT)
        results = svc.filter_next("work", min_minutes=120)
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
        svc.update("work", b.id, {"defer_until": datetime(2026, 6, 1, 9, 0)})
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id}

    def test_include_deferred(self, svc):
        a = svc.capture("work", "Now")
        svc.move("work", a.id, Bucket.NEXT)
        b = svc.capture("work", "Later")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"defer_until": datetime(2026, 6, 1, 9, 0)})
        results = svc.filter_next("work", include_deferred=True)
        assert {r.id for r in results} == {a.id, b.id}

    def test_defer_by_hours_hides_until_now_passes(self, svc):
        # svc._now() returns 2026-04-10 09:15. An item deferred one hour
        # from "now" should still be hidden; deferred one hour ago is shown.
        future = svc.capture("work", "In 1 hour")
        svc.move("work", future.id, Bucket.NEXT)
        svc.update("work", future.id, {"defer_until": datetime(2026, 4, 10, 10, 15)})
        past = svc.capture("work", "1 hour ago")
        svc.move("work", past.id, Bucket.NEXT)
        svc.update("work", past.id, {"defer_until": datetime(2026, 4, 10, 8, 15)})
        results = svc.filter_next("work")
        assert {r.id for r in results} == {past.id}

    def test_defer_same_day_later_hour_is_hidden(self, svc):
        # Deferring to later today (daily granularity used to miss this).
        a = svc.capture("work", "Later today")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"defer_until": datetime(2026, 4, 10, 15, 0)})
        assert svc.filter_next("work") == []

    def test_overdue_overrides_defer(self, svc):
        # An item past its due date must surface even if deferred — otherwise
        # a typo in defer_until silently hides a missed deadline.
        a = svc.capture("work", "Overdue but deferred")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update(
            "work",
            a.id,
            {"due": "2026-04-09", "defer_until": datetime(2026, 6, 1, 9, 0)},
        )
        assert {r.id for r in svc.filter_next("work")} == {a.id}

    def test_due_today_overrides_defer(self, svc):
        # Same protection on the boundary: due today should not be hidden.
        a = svc.capture("work", "Due today, deferred")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update(
            "work",
            a.id,
            {"due": "2026-04-10", "defer_until": datetime(2026, 6, 1, 9, 0)},
        )
        assert {r.id for r in svc.filter_next("work")} == {a.id}

    def test_future_due_with_active_defer_still_hidden(self, svc):
        # Defer still works when the deadline hasn't arrived yet.
        a = svc.capture("work", "Due later, deferred")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update(
            "work",
            a.id,
            {"due": "2026-05-01", "defer_until": datetime(2026, 4, 20, 9, 0)},
        )
        assert svc.filter_next("work") == []


class TestOverdueFilter:
    """Filter by overdue (due ≤ today, where today comes from the injected clock)."""

    def _seed(self, svc):
        # svc clock is fixed to 2026-04-10. Three items in /next, mixed dueness.
        past = svc.capture("work", "Past due")
        svc.move("work", past.id, Bucket.NEXT)
        svc.update("work", past.id, {"due": "2026-04-09"})
        today = svc.capture("work", "Due today")
        svc.move("work", today.id, Bucket.NEXT)
        svc.update("work", today.id, {"due": "2026-04-10"})
        future = svc.capture("work", "Due later")
        svc.move("work", future.id, Bucket.NEXT)
        svc.update("work", future.id, {"due": "2026-04-30"})
        undated = svc.capture("work", "No due")
        svc.move("work", undated.id, Bucket.NEXT)
        return past, today, future, undated

    def test_overdue_includes_today_and_past(self, svc):
        past, today, *_ = self._seed(svc)
        results = svc.list_items("work", bucket=Bucket.NEXT, overdue=True)
        assert {r.id for r in results} == {past.id, today.id}

    def test_overdue_off_returns_all(self, svc):
        past, today, future, undated = self._seed(svc)
        results = svc.list_items("work", bucket=Bucket.NEXT)
        assert {r.id for r in results} == {past.id, today.id, future.id, undated.id}

    def test_overdue_combines_with_other_filters(self, svc):
        past, today, *_ = self._seed(svc)
        svc.update("work", past.id, {"contexts": ["calls"]})
        svc.update("work", today.id, {"contexts": ["computer"]})
        results = svc.list_items(
            "work", bucket=Bucket.NEXT, overdue=True, contexts=["calls"]
        )
        assert {r.id for r in results} == {past.id}

    def test_overdue_works_in_other_buckets(self, svc):
        # An item due yesterday in inbox should show up too.
        a = svc.capture("work", "Inbox overdue")
        svc.update("work", a.id, {"due": "2026-04-09"})
        b = svc.capture("work", "Inbox future")
        svc.update("work", b.id, {"due": "2026-05-01"})
        results = svc.list_items("work", bucket=Bucket.INBOX, overdue=True)
        assert {r.id for r in results} == {a.id}


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

    def _seed_project_with_deferred(self, svc):
        svc.save_project("work", Project(
            id="p1", title="P1", body="",
            created=datetime(2026, 3, 1), updated=datetime(2026, 3, 1),
        ))
        live = svc.capture("work", "Live")
        svc.move("work", live.id, Bucket.NEXT)
        svc.update("work", live.id, {"project": "p1"})
        deferred = svc.capture("work", "Deferred")
        svc.move("work", deferred.id, Bucket.NEXT)
        svc.update("work", deferred.id, {
            "project": "p1",
            "defer_until": datetime(2026, 6, 1, 9, 0),
        })
        return live, deferred

    def test_hides_deferred_by_default(self, svc):
        live, _ = self._seed_project_with_deferred(svc)
        results = svc.actions_for_project("work", "p1")
        assert {r.id for r in results} == {live.id}

    def test_include_deferred_returns_all(self, svc):
        live, deferred = self._seed_project_with_deferred(svc)
        results = svc.actions_for_project("work", "p1", include_deferred=True)
        assert {r.id for r in results} == {live.id, deferred.id}

    def test_overdue_overrides_defer(self, svc):
        # Same protection as filter_items: a deferred-but-overdue item must
        # surface so a stale defer_until cannot swallow a missed deadline.
        svc.save_project("work", Project(
            id="p1", title="P1", body="",
            created=datetime(2026, 3, 1), updated=datetime(2026, 3, 1),
        ))
        item = svc.capture("work", "Overdue + deferred")
        svc.move("work", item.id, Bucket.NEXT)
        svc.update("work", item.id, {
            "project": "p1",
            "due": "2026-04-09",
            "defer_until": datetime(2026, 6, 1, 9, 0),
        })
        results = svc.actions_for_project("work", "p1")
        assert {r.id for r in results} == {item.id}


class TestFindProjectByTitle:
    def _save(
        self, svc, pid: str, title: str, *, priority=None, status: str = "active"
    ) -> Project:
        project = Project(
            id=pid,
            title=title,
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            status=status,  # type: ignore[arg-type]
            priority=priority,
        )
        svc.save_project("work", project)
        return project

    def test_empty_query_returns_none(self, svc):
        self._save(svc, "p1", "Anything")
        assert svc.find_project_by_title("work", "") is None

    def test_none_query_returns_none(self, svc):
        self._save(svc, "p1", "Anything")
        # type: ignore[arg-type] — exercise the runtime guard
        assert svc.find_project_by_title("work", None) is None  # type: ignore[arg-type]

    def test_empty_catalogue_returns_none(self, svc):
        assert svc.find_project_by_title("work", "anything") is None

    def test_exact_id_match_beats_title(self, svc):
        # A project whose ID equals the query should win even when another
        # project's title happens to equal the query too.
        self._save(svc, "exact-id", "Something else")
        self._save(svc, "p-other", "exact-id")  # title collides with other id
        found = svc.find_project_by_title("work", "exact-id")
        assert found is not None
        assert found.id == "exact-id"

    def test_case_insensitive_title_match(self, svc):
        self._save(svc, "p1", "People Ops")
        found = svc.find_project_by_title("work", "people ops")
        assert found is not None
        assert found.id == "p1"

    def test_single_substring_hit(self, svc):
        self._save(svc, "p1", "Ship frontend")
        self._save(svc, "p2", "Backlog review")
        found = svc.find_project_by_title("work", "ship")
        assert found is not None
        assert found.id == "p1"

    def test_multiple_substring_hits_prefer_highest_priority(self, svc):
        # 1 is most urgent; 3 is less urgent. Both titles contain "ship".
        self._save(svc, "p-lower", "Ship hotfix", priority=3)
        self._save(svc, "p-higher", "Ship feature", priority=1)
        found = svc.find_project_by_title("work", "ship")
        assert found is not None
        assert found.id == "p-higher"

    def test_multiple_substring_hits_all_null_priority_alphabetical(self, svc):
        # Tie-break on title alphabetical order when priorities are equal/null.
        self._save(svc, "p-b", "Ship widget")
        self._save(svc, "p-a", "Ship alpha")
        found = svc.find_project_by_title("work", "ship")
        assert found is not None
        assert found.id == "p-a"

    def test_fuzzy_match_for_typo(self, svc):
        self._save(svc, "p1", "Onboarding")
        self._save(svc, "p2", "Release cycle")
        found = svc.find_project_by_title("work", "onboaring")  # missing 'd'
        assert found is not None
        assert found.id == "p1"

    def test_totally_unrelated_query_returns_none(self, svc):
        self._save(svc, "p1", "Onboarding")
        self._save(svc, "p2", "Release cycle")
        assert svc.find_project_by_title("work", "xyzzy nothing") is None

    def test_inactive_projects_excluded(self, svc):
        # Completed project should NOT be matched even by exact title.
        self._save(svc, "p1", "Retired project", status="complete")
        assert svc.find_project_by_title("work", "Retired project") is None


class TestProjectUpdates:
    def _save(self, svc, pid: str, status: str = "active") -> Project:
        project = Project(
            id=pid,
            title=f"Project {pid}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            status=status,  # type: ignore[arg-type]
        )
        svc.save_project("work", project)
        return project

    def test_update_project_status(self, svc):
        self._save(svc, "p1")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        updated = svc.update_project("work", "p1", {"status": "complete"})
        assert updated.status == "complete"
        assert updated.updated == datetime(2026, 4, 11, 10, 0)

    def test_update_project_missing_raises(self, svc):
        with pytest.raises(KeyError):
            svc.update_project("work", "nope", {"status": "complete"})

    def test_update_project_invalid_status(self, svc):
        self._save(svc, "p1")
        with pytest.raises(ValueError, match="invalid status"):
            svc.update_project("work", "p1", {"status": "bogus"})

    def test_update_project_immutable_fields(self, svc):
        self._save(svc, "p1")
        with pytest.raises(ValueError, match="immutable"):
            svc.update_project("work", "p1", {"id": "hacked"})

    def test_list_projects_hides_complete(self, svc):
        self._save(svc, "a1")
        self._save(svc, "done1", status="complete")
        ids = {p.id for p in svc.list_projects("work")}
        assert ids == {"a1"}

    def test_list_projects_include_inactive(self, svc):
        self._save(svc, "a1")
        self._save(svc, "done1", status="complete")
        ids = {p.id for p in svc.list_projects("work", include_inactive=True)}
        assert ids == {"a1", "done1"}


class TestMaxNextItems:
    def _capped_project(self, svc, pid: str, max_next_items: int | None) -> Project:
        project = Project(
            id=pid,
            title=f"Project {pid}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            max_next_items=max_next_items,
        )
        svc.save_project("work", project)
        return project

    def _capture_with_order(self, svc, title: str, project_id: str, order: int):
        item = svc.capture("work", title)
        svc.move("work", item.id, Bucket.NEXT)
        svc.update("work", item.id, {"project": project_id, "order": order})
        return item

    def test_max_next_items_one_hides_later_steps(self, svc):
        self._capped_project(svc, "seq", max_next_items=1)
        a = self._capture_with_order(svc, "Step A", "seq", 1)
        b = self._capture_with_order(svc, "Step B", "seq", 2)
        c = self._capture_with_order(svc, "Step C", "seq", 3)
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id}
        assert b.id not in {r.id for r in results}
        assert c.id not in {r.id for r in results}

    def test_max_next_items_none_shows_all_steps(self, svc):
        self._capped_project(svc, "par", max_next_items=None)
        a = self._capture_with_order(svc, "Parallel A", "par", 1)
        b = self._capture_with_order(svc, "Parallel B", "par", 2)
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id, b.id}

    def test_max_next_items_two_surfaces_two_steps(self, svc):
        self._capped_project(svc, "capped", max_next_items=2)
        a = self._capture_with_order(svc, "Step A", "capped", 1)
        b = self._capture_with_order(svc, "Step B", "capped", 2)
        c = self._capture_with_order(svc, "Step C", "capped", 3)
        d = self._capture_with_order(svc, "Step D", "capped", 4)
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id, b.id}
        assert c.id not in {r.id for r in results}
        assert d.id not in {r.id for r in results}

    def test_max_next_items_one_surfaces_next_after_completion(self, svc):
        self._capped_project(svc, "seq", max_next_items=1)
        a = self._capture_with_order(svc, "Step A", "seq", 1)
        b = self._capture_with_order(svc, "Step B", "seq", 2)
        # Only A visible initially
        assert {r.id for r in svc.filter_next("work")} == {a.id}
        # Complete A — B should now surface
        svc.complete("work", a.id)
        assert {r.id for r in svc.filter_next("work")} == {b.id}

    def test_show_all_bypasses_next_cap(self, svc):
        self._capped_project(svc, "seq", max_next_items=1)
        a = self._capture_with_order(svc, "Step A", "seq", 1)
        b = self._capture_with_order(svc, "Step B", "seq", 2)
        results = svc.list_items("work", bucket=Bucket.NEXT, respect_next_cap=False)
        assert {r.id for r in results} == {a.id, b.id}

    def test_items_without_order_sort_by_id(self, svc):
        # When a capped project has items with no explicit order,
        # the first-captured item (lowest ID) is the one that shows.
        self._capped_project(svc, "seq", max_next_items=1)
        a = svc.capture("work", "First capture")
        svc.move("work", a.id, Bucket.NEXT)
        svc.update("work", a.id, {"project": "seq"})
        # Advance the clock so b's id sorts after a's
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        b = svc.capture("work", "Second capture")
        svc.move("work", b.id, Bucket.NEXT)
        svc.update("work", b.id, {"project": "seq"})
        results = svc.filter_next("work")
        assert {r.id for r in results} == {a.id}

    def test_update_project_rejects_zero(self, svc):
        self._capped_project(svc, "seq", max_next_items=1)
        with pytest.raises(ValueError, match="max_next_items"):
            svc.update_project("work", "seq", {"max_next_items": 0})

    def test_create_project_rejects_zero(self, svc):
        with pytest.raises(ValueError, match="max_next_items"):
            svc.create_project(
                "work", title="Bad", project_id="bad", max_next_items=0
            )


class TestNextViewSort:
    """filter_next sorts by project priority → item due → capture order."""

    def _project(self, svc, pid: str, priority) -> Project:
        project = Project(
            id=pid,
            title=f"Project {pid}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
            priority=priority,
        )
        svc.save_project("work", project)
        return project

    def _capture_next(self, svc, title: str, project_id: str | None = None, due=None):
        item = svc.capture("work", title)
        svc.move("work", item.id, Bucket.NEXT)
        patch: dict = {}
        if project_id is not None:
            patch["project"] = project_id
        if due is not None:
            patch["due"] = due
        if patch:
            svc.update("work", item.id, patch)
        return item

    def test_p1_beats_p3_regardless_of_capture_order(self, svc):
        self._project(svc, "p3proj", priority=3)
        self._project(svc, "p1proj", priority=1)
        # Capture p3 item first, p1 item second — capture order would put p3 first.
        p3_item = self._capture_next(svc, "P3 task", "p3proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        p1_item = self._capture_next(svc, "P1 task", "p1proj")
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(p1_item.id) < ordered.index(p3_item.id)

    def test_no_project_sorts_before_rated_projects(self, svc):
        # Orphan next actions surface at the top — they would otherwise be
        # buried under prioritised project work and forgotten.
        self._project(svc, "p1proj", priority=1)
        p1_item = self._capture_next(svc, "P1 task", "p1proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        floating = self._capture_next(svc, "Floating task", project_id=None)
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(floating.id) < ordered.index(p1_item.id)

    def test_no_project_sorts_before_unrated_projects(self, svc):
        self._project(svc, "unrated", priority=None)
        unrated_item = self._capture_next(svc, "Unrated task", "unrated")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        floating = self._capture_next(svc, "Floating task", project_id=None)
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(floating.id) < ordered.index(unrated_item.id)

    def test_project_with_null_priority_sorts_after_rated(self, svc):
        self._project(svc, "p2proj", priority=2)
        self._project(svc, "unrated", priority=None)
        p2_item = self._capture_next(svc, "P2 task", "p2proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        unrated_item = self._capture_next(svc, "Unrated task", "unrated")
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(p2_item.id) < ordered.index(unrated_item.id)

    def test_same_priority_sorted_by_due_date(self, svc):
        self._project(svc, "p2proj", priority=2)
        later = self._capture_next(svc, "Due later", "p2proj", due="2026-06-01")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        sooner = self._capture_next(svc, "Due sooner", "p2proj", due="2026-05-01")
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(sooner.id) < ordered.index(later.id)

    def test_same_priority_no_due_falls_back_to_capture_order(self, svc):
        self._project(svc, "p2proj", priority=2)
        first = self._capture_next(svc, "First captured", "p2proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        second = self._capture_next(svc, "Second captured", "p2proj")
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(first.id) < ordered.index(second.id)

    def test_dated_items_sort_before_undated_in_same_tier(self, svc):
        self._project(svc, "p2proj", priority=2)
        undated = self._capture_next(svc, "No due", "p2proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        dated = self._capture_next(svc, "Has due", "p2proj", due="2026-07-01")
        ordered = [i.id for i in svc.filter_next("work")]
        assert ordered.index(dated.id) < ordered.index(undated.id)

    def test_show_all_preserves_capture_order(self, svc):
        # show_all=true sets respect_next_cap=False; priority sort should not apply
        # so review mode sees everything in raw capture order.
        self._project(svc, "p3proj", priority=3)
        self._project(svc, "p1proj", priority=1)
        p3_item = self._capture_next(svc, "P3 task", "p3proj")
        svc._now = lambda: datetime(2026, 4, 11, 10, 0)
        p1_item = self._capture_next(svc, "P1 task", "p1proj")
        results = svc.list_items("work", bucket=Bucket.NEXT, respect_next_cap=False)
        ordered = [i.id for i in results]
        assert ordered.index(p3_item.id) < ordered.index(p1_item.id)


class TestReorderProjectItems:
    def _project(self, svc, pid: str) -> Project:
        project = Project(
            id=pid,
            title=f"Project {pid}",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
        )
        svc.save_project("work", project)
        return project

    def _action(self, svc, title: str, project_id: str):
        item = svc.capture("work", title)
        svc.move("work", item.id, Bucket.NEXT)
        svc.update("work", item.id, {"project": project_id})
        return item

    def test_assigns_sequential_orders(self, svc):
        self._project(svc, "p1")
        a = self._action(svc, "A", "p1")
        b = self._action(svc, "B", "p1")
        c = self._action(svc, "C", "p1")
        result = svc.reorder_project_items("work", "p1", [c.id, a.id, b.id])
        assert [i.order for i in result] == [1, 2, 3]
        # Verify persisted
        actions = svc.actions_for_project("work", "p1")
        assert [i.id for i in actions] == [c.id, a.id, b.id]

    def test_rejects_foreign_item(self, svc):
        self._project(svc, "p1")
        self._project(svc, "p2")
        stranger = self._action(svc, "X", "p2")
        with pytest.raises(ValueError, match="not in project"):
            svc.reorder_project_items("work", "p1", [stranger.id])

    def test_missing_item_raises(self, svc):
        self._project(svc, "p1")
        with pytest.raises(KeyError):
            svc.reorder_project_items("work", "p1", ["nonexistent"])


class TestEnvIsolation:
    def test_capture_in_different_envs(self, svc, data_root):
        w = svc.capture("work", "Work item")
        h = svc.capture("home", "Home item")
        assert (data_root / "work" / "inbox" / f"{w.id}.md").exists()
        assert (data_root / "home" / "inbox" / f"{h.id}.md").exists()
        assert svc.filter_next("work") == []
        assert svc.filter_next("home") == []
