from datetime import date, datetime

from gtd_core.models import Bucket, EnvConfig, Item, Project
from gtd_core.storage import (
    dump_env_config,
    dump_item,
    dump_project,
    load_env_config,
    load_item,
    load_project,
)


class TestItemRoundTrip:
    def test_minimal_item(self, tmp_path):
        item = Item(
            id="2026-04-10T0915-test",
            title="Test",
            body="",
            created=datetime(2026, 4, 10, 9, 15),
            updated=datetime(2026, 4, 10, 9, 15),
            status=Bucket.INBOX,
        )
        path = tmp_path / "inbox" / "test.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.INBOX)
        assert loaded == item

    def test_full_item(self, tmp_path):
        item = Item(
            id="2026-04-10T0915-full",
            title="Full item",
            body="Body text with\nmultiple lines.",
            created=datetime(2026, 4, 10, 9, 15),
            updated=datetime(2026, 4, 10, 10, 0),
            status=Bucket.NEXT,
            contexts=["calls", "errands"],
            energy="low",
            time_minutes=5,
            project="2026-03-01-launch-blog",
            area="health",
            tags=["dentist", "urgent"],
            due=date(2026, 5, 1),
            defer_until=date(2026, 4, 15),
        )
        path = tmp_path / "next" / "full.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.NEXT)
        assert loaded == item

    def test_waiting_item(self, tmp_path):
        item = Item(
            id="2026-04-10T1500-legal-review",
            title="Awaiting legal review",
            body="",
            created=datetime(2026, 4, 10, 15, 0),
            updated=datetime(2026, 4, 10, 15, 0),
            status=Bucket.WAITING,
            waiting_on="legal team",
            waiting_since=date(2026, 4, 5),
        )
        path = tmp_path / "waiting" / "legal.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.WAITING)
        assert loaded.waiting_on == "legal team"
        assert loaded.waiting_since == date(2026, 4, 5)

    def test_status_not_stored_in_frontmatter(self, tmp_path):
        """Status is derived from path, never serialized."""
        item = Item(
            id="test",
            title="T",
            body="",
            created=datetime(2026, 1, 1),
            updated=datetime(2026, 1, 1),
            status=Bucket.INBOX,
        )
        path = tmp_path / "x.md"
        dump_item(path, item)
        raw = path.read_text()
        assert "status:" not in raw

    def test_body_preserved(self, tmp_path):
        body = "# Heading\n\nSome **bold** markdown.\n\n- list\n- items\n"
        item = Item(
            id="test",
            title="T",
            body=body,
            created=datetime(2026, 1, 1),
            updated=datetime(2026, 1, 1),
            status=Bucket.INBOX,
        )
        path = tmp_path / "x.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.body.strip() == body.strip()


class TestProjectRoundTrip:
    def test_minimal(self, tmp_path):
        p = Project(
            id="2026-03-01-launch-blog",
            title="Launch blog",
            body="Some notes",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 3, 1),
        )
        path = tmp_path / "blog.md"
        dump_project(path, p)
        loaded = load_project(path)
        assert loaded == p

    def test_full(self, tmp_path):
        p = Project(
            id="2026-03-01-launch-blog",
            title="Launch blog",
            body="Outcome notes",
            created=datetime(2026, 3, 1),
            updated=datetime(2026, 4, 1),
            status="on_hold",
            outcome="Blog live with 3 posts",
            area="writing",
            tags=["personal"],
        )
        path = tmp_path / "blog.md"
        dump_project(path, p)
        loaded = load_project(path)
        assert loaded == p


class TestEnvConfigRoundTrip:
    def test_load_and_dump(self, tmp_path):
        cfg = EnvConfig(
            name="work",
            contexts=["calls", "computer"],
            areas=["engineering", "management"],
            default_energy="medium",
        )
        path = tmp_path / "config.yml"
        dump_env_config(path, cfg)
        loaded = load_env_config(path)
        assert loaded == cfg

    def test_load_existing_work_config(self):
        from django.conf import settings

        cfg = load_env_config(settings.GTD_DATA_ROOT / "work" / "config.yml")
        assert cfg.name == "work"
        assert "calls" in cfg.contexts
        assert "engineering" in cfg.areas
