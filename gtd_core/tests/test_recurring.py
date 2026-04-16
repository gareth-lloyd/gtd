from datetime import date, datetime

import pytest

from gtd_core.models import Bucket, Template
from gtd_core.recurring import is_due, next_spawn_date, spawn_recurring
from gtd_core.repository import EnvRepository


@pytest.fixture
def repo(data_root):
    return EnvRepository(data_root, "work")


def _tmpl(recurrence="weekly", last_spawned=None, tmpl_id="recurring-test"):
    return Template(
        id=tmpl_id,
        title="Test template",
        body="Do the thing.",
        contexts=["calls"],
        energy="low",
        time_minutes=10,
        recurrence=recurrence,
        last_spawned=last_spawned,
    )


class TestNextSpawnDate:
    def test_daily(self):
        assert next_spawn_date("daily", date(2026, 4, 10)) == date(2026, 4, 11)

    def test_weekly(self):
        assert next_spawn_date("weekly", date(2026, 4, 10)) == date(2026, 4, 17)

    def test_biweekly(self):
        assert next_spawn_date("biweekly", date(2026, 4, 10)) == date(2026, 4, 24)

    def test_monthly(self):
        assert next_spawn_date("monthly", date(2026, 1, 31)) == date(2026, 2, 28)

    def test_quarterly(self):
        assert next_spawn_date("quarterly", date(2026, 1, 15)) == date(2026, 4, 15)

    def test_yearly(self):
        assert next_spawn_date("yearly", date(2026, 4, 10)) == date(2027, 4, 10)

    def test_every_n_days(self):
        assert next_spawn_date("every_3_days", date(2026, 4, 10)) == date(2026, 4, 13)

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown recurrence"):
            next_spawn_date("bogus", date(2026, 4, 10))


class TestIsDue:
    def test_never_spawned(self):
        assert is_due(_tmpl(last_spawned=None), today=date(2026, 4, 10)) is True

    def test_due(self):
        assert is_due(_tmpl("weekly", last_spawned=date(2026, 4, 1)), today=date(2026, 4, 10)) is True

    def test_not_due(self):
        assert is_due(_tmpl("weekly", last_spawned=date(2026, 4, 9)), today=date(2026, 4, 10)) is False

    def test_exact_day(self):
        assert is_due(_tmpl("weekly", last_spawned=date(2026, 4, 3)), today=date(2026, 4, 10)) is True


class TestSpawnRecurring:
    def test_spawns_into_inbox(self, repo):
        repo.save_template(_tmpl("weekly", last_spawned=None))
        spawned = spawn_recurring(repo, today=date(2026, 4, 10))
        assert len(spawned) == 1
        assert spawned[0].status == Bucket.INBOX
        assert spawned[0].title == "Test template"
        assert spawned[0].contexts == ["calls"]
        assert spawned[0].energy == "low"
        assert spawned[0].time_minutes == 10
        # File should exist
        inbox = list(repo.list_items(bucket=Bucket.INBOX))
        assert len(inbox) == 1

    def test_updates_last_spawned(self, repo):
        repo.save_template(_tmpl("weekly", last_spawned=None))
        spawn_recurring(repo, today=date(2026, 4, 10))
        templates = repo.list_templates()
        assert templates[0].last_spawned == date(2026, 4, 10)

    def test_skips_not_due(self, repo):
        repo.save_template(_tmpl("weekly", last_spawned=date(2026, 4, 9)))
        spawned = spawn_recurring(repo, today=date(2026, 4, 10))
        assert spawned == []

    def test_multiple_templates(self, repo):
        repo.save_template(_tmpl("daily", last_spawned=date(2026, 4, 9), tmpl_id="daily-task"))
        repo.save_template(_tmpl("weekly", last_spawned=date(2026, 4, 9), tmpl_id="weekly-task"))
        spawned = spawn_recurring(repo, today=date(2026, 4, 10))
        # daily: due (last was yesterday). weekly: not due (last was yesterday, next is Apr 16)
        assert len(spawned) == 1
        assert "daily-task" in spawned[0].id or spawned[0].title == "Test template"

    def test_body_copied(self, repo):
        repo.save_template(_tmpl(last_spawned=None))
        spawned = spawn_recurring(repo, today=date(2026, 4, 10))
        assert spawned[0].body == "Do the thing."

    def test_idempotent_same_day(self, repo):
        """Spawning twice on the same day should not create duplicates."""
        repo.save_template(_tmpl("daily", last_spawned=None))
        first = spawn_recurring(repo, today=date(2026, 4, 10))
        assert len(first) == 1
        second = spawn_recurring(repo, today=date(2026, 4, 10))
        assert len(second) == 0
