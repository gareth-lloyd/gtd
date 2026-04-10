from datetime import date, datetime

from gtd_core.models import Bucket, EnvConfig, Item, Project


class TestBucket:
    def test_values(self):
        assert Bucket.INBOX.value == "inbox"
        assert Bucket.NEXT.value == "next"
        assert Bucket.WAITING.value == "waiting"
        assert Bucket.SOMEDAY.value == "someday"
        assert Bucket.REFERENCE.value == "reference"
        assert Bucket.PROJECTS.value == "projects"
        assert Bucket.ARCHIVE.value == "archive"

    def test_from_value(self):
        assert Bucket("inbox") is Bucket.INBOX


class TestItem:
    def test_minimal(self):
        item = Item(
            id="2026-04-10T0915-test",
            title="Test item",
            body="",
            created=datetime(2026, 4, 10, 9, 15),
            updated=datetime(2026, 4, 10, 9, 15),
            status=Bucket.INBOX,
        )
        assert item.id == "2026-04-10T0915-test"
        assert item.contexts == []
        assert item.tags == []
        assert item.energy is None
        assert item.time_minutes is None
        assert item.project is None
        assert item.area is None
        assert item.due is None
        assert item.defer_until is None
        assert item.waiting_on is None
        assert item.waiting_since is None

    def test_full(self):
        item = Item(
            id="2026-04-10T0915-full",
            title="Full item",
            body="Body text.",
            created=datetime(2026, 4, 10, 9, 15),
            updated=datetime(2026, 4, 10, 9, 15),
            status=Bucket.NEXT,
            contexts=["calls", "errands"],
            energy="low",
            time_minutes=5,
            project="2026-03-01-launch-blog",
            area="health",
            tags=["dentist"],
            due=date(2026, 5, 1),
            defer_until=date(2026, 4, 15),
            waiting_on=None,
        )
        assert item.contexts == ["calls", "errands"]
        assert item.energy == "low"
        assert item.time_minutes == 5
        assert item.due == date(2026, 5, 1)
        assert item.defer_until == date(2026, 4, 15)
        assert item.project == "2026-03-01-launch-blog"

    def test_independent_default_lists(self):
        """Default factories must give each instance its own list."""
        a = Item(
            id="a", title="", body="", created=datetime(2026, 1, 1),
            updated=datetime(2026, 1, 1), status=Bucket.INBOX,
        )
        b = Item(
            id="b", title="", body="", created=datetime(2026, 1, 1),
            updated=datetime(2026, 1, 1), status=Bucket.INBOX,
        )
        a.contexts.append("calls")
        assert b.contexts == []


class TestProject:
    def test_minimal(self):
        p = Project(
            id="2026-03-01-launch-blog",
            title="Launch personal blog",
            body="",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
        )
        assert p.status == "active"
        assert p.outcome is None
        assert p.area is None
        assert p.tags == []


class TestEnvConfig:
    def test_defaults(self):
        cfg = EnvConfig(name="work", contexts=["calls"], areas=["engineering"])
        assert cfg.default_energy == "medium"
        assert cfg.name == "work"
