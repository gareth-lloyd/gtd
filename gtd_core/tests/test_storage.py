from datetime import date, datetime

import pytest

from gtd_core.models import Bucket, EnvConfig, Item, Project
from gtd_core.storage import (
    dump_env_config,
    dump_item,
    dump_project,
    list_item_paths,
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
            defer_until=datetime(2026, 4, 15, 14, 30),
        )
        path = tmp_path / "next" / "full.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.NEXT)
        assert loaded == item

    def test_defer_until_legacy_date_promotes_to_midnight(self, tmp_path):
        """Items written before the hours-granularity change stored defer_until
        as a date; load_item should promote those to midnight so the field
        stays a datetime."""
        path = tmp_path / "inbox" / "legacy.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: 2026-04-10T0900-legacy\n"
            "title: Legacy\n"
            "created: 2026-04-10 09:00:00\n"
            "updated: 2026-04-10 09:00:00\n"
            "defer_until: 2026-04-15\n"
            "---\n"
        )
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.defer_until == datetime(2026, 4, 15, 0, 0)

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

    def test_source_id_round_trip(self, tmp_path):
        item = Item(
            id="2026-04-21T0930-review-pr-40386",
            title="Review PR #40386",
            body="",
            created=datetime(2026, 4, 21, 9, 30),
            updated=datetime(2026, 4, 21, 9, 30),
            status=Bucket.INBOX,
            source_id="https://github.com/canary-technologies-corp/canary/pull/40386",
        )
        path = tmp_path / "inbox" / "pr.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.source_id == item.source_id
        assert loaded == item

    def test_source_id_defaults_to_none_for_legacy_files(self, tmp_path):
        path = tmp_path / "inbox" / "legacy.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: 2026-04-01T0900-legacy\n"
            "title: Legacy item\n"
            "created: 2026-04-01 09:00:00\n"
            "updated: 2026-04-01 09:00:00\n"
            "---\n"
        )
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.source_id is None

    def test_working_on_round_trip(self, tmp_path):
        item = Item(
            id="2026-05-01T0900-pin-me",
            title="Pinned task",
            body="",
            created=datetime(2026, 5, 1, 9, 0),
            updated=datetime(2026, 5, 1, 9, 0),
            status=Bucket.NEXT,
            working_on=True,
        )
        path = tmp_path / "next" / "pin.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.NEXT)
        assert loaded.working_on is True
        assert loaded == item

    def test_working_on_defaults_false_for_legacy_files(self, tmp_path):
        path = tmp_path / "inbox" / "legacy.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: 2026-04-01T0900-legacy\n"
            "title: Legacy item\n"
            "created: 2026-04-01 09:00:00\n"
            "updated: 2026-04-01 09:00:00\n"
            "---\n"
        )
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.working_on is False

    def test_output_round_trip(self, tmp_path):
        item = Item(
            id="2026-05-06T0900-with-output",
            title="Has agent log",
            body="",
            created=datetime(2026, 5, 6, 9, 0),
            updated=datetime(2026, 5, 6, 9, 0),
            status=Bucket.NEXT,
            output="## Agent run 2026-05-06\n\nReviewed PR. LGTM.",
        )
        path = tmp_path / "next" / "out.md"
        dump_item(path, item)
        loaded = load_item(path, Bucket.NEXT)
        assert loaded.output == "## Agent run 2026-05-06\n\nReviewed PR. LGTM."
        assert loaded == item

    def test_output_defaults_empty_for_legacy_files(self, tmp_path):
        path = tmp_path / "inbox" / "legacy.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "id: 2026-04-01T0900-legacy\n"
            "title: Legacy item\n"
            "created: 2026-04-01 09:00:00\n"
            "updated: 2026-04-01 09:00:00\n"
            "---\n"
        )
        loaded = load_item(path, Bucket.INBOX)
        assert loaded.output == ""

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
            max_next_items=2,
            working_dir="~/projects/blog",
        )
        path = tmp_path / "blog.md"
        dump_project(path, p)
        loaded = load_project(path)
        assert loaded == p

    def test_legacy_sequential_field_raises(self, tmp_path):
        path = tmp_path / "old.md"
        path.write_text(
            "---\n"
            "id: old\n"
            "title: Old\n"
            "created: 2026-01-01\n"
            "updated: 2026-01-01\n"
            "sequential: true\n"
            "---\n"
        )
        with pytest.raises(ValueError, match="legacy 'sequential'"):
            load_project(path)


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
        assert "deep" in cfg.contexts
        assert "engineering" in cfg.areas


class TestAtomicDump:
    """`dump_*` writes through a tmp file + os.replace so a crash mid-write
    cannot corrupt or truncate the destination."""

    def _make_item(self, body: str) -> Item:
        return Item(
            id="2026-04-10T0915-atomic",
            title="Atomic test",
            body=body,
            created=datetime(2026, 4, 10, 9, 15),
            updated=datetime(2026, 4, 10, 9, 15),
            status=Bucket.INBOX,
        )

    def test_dump_failure_preserves_original_content(self, tmp_path, monkeypatch):
        path = tmp_path / "inbox" / "atomic.md"
        original = self._make_item("original body")
        dump_item(path, original)
        before = path.read_bytes()

        # frontmatter.dump raises on second call → tmp must not replace dest.
        import gtd_core.storage as storage

        real_dump = storage.frontmatter.dump

        def boom(*_args, **_kwargs):
            raise OSError("simulated mid-write crash")

        monkeypatch.setattr(storage.frontmatter, "dump", boom)
        try:
            with pytest.raises(OSError, match="simulated"):
                dump_item(path, self._make_item("would-be replacement"))
        finally:
            monkeypatch.setattr(storage.frontmatter, "dump", real_dump)

        # Original content intact and no .tmp leak in the directory.
        assert path.read_bytes() == before
        leftovers = [p.name for p in path.parent.iterdir() if p.suffix == ".tmp"]
        assert leftovers == []

    def test_tmp_files_invisible_to_list_item_paths(self, tmp_path):
        path = tmp_path / "real.md"
        dump_item(path, self._make_item("real"))
        # Manually drop a tmp orphan as if a previous crash had left one.
        (tmp_path / f"orphan.md.{12345}.tmp").write_bytes(b"junk")
        listed = list_item_paths(tmp_path)
        assert listed == [path]
