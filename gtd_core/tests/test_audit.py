"""Tests for the irreversible-action audit log."""

import json
from datetime import datetime

from gtd_core.audit import log_purge


def _read_records(path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class TestLogPurge:
    def test_writes_record_to_audit_dir(self, tmp_path):
        log_purge(tmp_path, env="work", kind="item", target_id="2026-04-10T0900-foo")

        path = tmp_path / ".audit" / "purges.ndjson"
        assert path.exists()
        records = _read_records(path)
        assert len(records) == 1
        assert records[0]["env"] == "work"
        assert records[0]["kind"] == "item"
        assert records[0]["id"] == "2026-04-10T0900-foo"
        # ISO timestamp parses cleanly.
        datetime.fromisoformat(records[0]["ts"])

    def test_appends_rather_than_overwrites(self, tmp_path):
        log_purge(tmp_path, env="work", kind="item", target_id="a")
        log_purge(tmp_path, env="work", kind="project", target_id="b")
        records = _read_records(tmp_path / ".audit" / "purges.ndjson")
        assert [r["id"] for r in records] == ["a", "b"]

    def test_creates_audit_dir_if_missing(self, tmp_path):
        assert not (tmp_path / ".audit").exists()
        log_purge(tmp_path, env="home", kind="item", target_id="x")
        assert (tmp_path / ".audit" / "purges.ndjson").exists()
