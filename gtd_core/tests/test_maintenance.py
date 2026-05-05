from datetime import date, datetime

import pytest

from gtd_core.maintenance import clear_expired_defers
from gtd_core.models import Bucket, Item
from gtd_core.repository import EnvRepository

NOW = datetime(2026, 4, 10, 9, 15)


@pytest.fixture
def repo(data_root):
    return EnvRepository(data_root, "work")


def _clock(now=NOW):
    return lambda: now


def _save(repo, item_id: str, defer_until: datetime | None) -> Item:
    item = Item(
        id=item_id,
        title=item_id,
        body="",
        created=datetime(2026, 4, 1, 9, 0),
        updated=datetime(2026, 4, 1, 9, 0),
        status=Bucket.NEXT,
        defer_until=defer_until,
    )
    repo.save(item)
    return item


class TestClearExpiredDefers:
    def test_clears_past_defer(self, repo):
        item = _save(repo, "past-defer", defer_until=datetime(2026, 4, 9, 23, 59))
        assert clear_expired_defers(repo, now=_clock()) == 1
        assert repo.get(item.id).defer_until is None  # type: ignore[union-attr]

    def test_leaves_future_defer(self, repo):
        item = _save(repo, "future-defer", defer_until=datetime(2026, 6, 1, 9, 0))
        assert clear_expired_defers(repo, now=_clock()) == 0
        assert repo.get(item.id).defer_until == datetime(2026, 6, 1, 9, 0)  # type: ignore[union-attr]

    def test_boundary_now_clears(self, repo):
        item = _save(repo, "now-defer", defer_until=NOW)
        assert clear_expired_defers(repo, now=_clock()) == 1
        assert repo.get(item.id).defer_until is None  # type: ignore[union-attr]

    def test_leaves_items_without_defer_alone(self, repo):
        item = _save(repo, "no-defer", defer_until=None)
        assert clear_expired_defers(repo, now=_clock()) == 0
        assert repo.get(item.id).defer_until is None  # type: ignore[union-attr]

    def test_idempotent_second_call(self, repo):
        _save(repo, "expired", defer_until=datetime(2026, 4, 1, 0, 0))
        assert clear_expired_defers(repo, now=_clock()) == 1
        assert clear_expired_defers(repo, now=_clock()) == 0

    def test_returns_count_across_buckets(self, repo):
        a = Item(
            id="inbox-expired",
            title="x",
            body="",
            created=datetime(2026, 4, 1),
            updated=datetime(2026, 4, 1),
            status=Bucket.INBOX,
            defer_until=datetime(2026, 4, 9, 9, 0),
        )
        b = Item(
            id="someday-expired",
            title="y",
            body="",
            created=datetime(2026, 4, 1),
            updated=datetime(2026, 4, 1),
            status=Bucket.SOMEDAY,
            defer_until=datetime(2026, 4, 9, 9, 0),
        )
        c = Item(
            id="next-future",
            title="z",
            body="",
            created=datetime(2026, 4, 1),
            updated=datetime(2026, 4, 1),
            status=Bucket.NEXT,
            defer_until=datetime(2026, 6, 1, 9, 0),
        )
        for item in (a, b, c):
            repo.save(item)
        assert clear_expired_defers(repo, now=_clock()) == 2
        assert repo.get(a.id).defer_until is None  # type: ignore[union-attr]
        assert repo.get(b.id).defer_until is None  # type: ignore[union-attr]
        assert repo.get(c.id).defer_until == datetime(2026, 6, 1, 9, 0)  # type: ignore[union-attr]

    def test_default_clock_used_when_now_omitted(self, repo):
        far_future = datetime.combine(
            date.today().replace(year=date.today().year + 5), datetime.min.time()
        )
        item = _save(repo, "far-future", defer_until=far_future)
        assert clear_expired_defers(repo) == 0
        assert repo.get(item.id).defer_until == far_future  # type: ignore[union-attr]
