import json
import subprocess
import sys
from pathlib import Path

import pytest

from .conftest import NoteSpec, make_bear_db


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "bear_reader.cli", *args],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def populated_db(tmp_path):
    db = tmp_path / "bear.sqlite"
    make_bear_db(
        db,
        [
            NoteSpec(unique_id="a", title="Alpha onboarding", body="welcome ryan"),
            NoteSpec(unique_id="b", title="Beta", body="other content"),
            NoteSpec(unique_id="c", title="Gamma", body="ryan again"),
        ],
    )
    return db


class TestCli:
    def test_emits_json_lines(self, populated_db: Path):
        r = _run_cli(["ryan", "--db-path", str(populated_db)])
        assert r.returncode == 0, r.stderr
        lines = [json.loads(line) for line in r.stdout.strip().split("\n") if line]
        assert len(lines) == 2
        ids = {hit["id"] for hit in lines}
        assert ids == {"a", "c"}

    def test_each_line_has_required_fields(self, populated_db: Path):
        r = _run_cli(["ryan", "--db-path", str(populated_db)])
        hit = json.loads(r.stdout.strip().split("\n")[0])
        assert {"id", "title", "tags", "snippet", "modified", "score"} <= set(hit)

    def test_limit_caps_results(self, populated_db: Path):
        r = _run_cli(["ryan", "--limit", "1", "--db-path", str(populated_db)])
        lines = [line for line in r.stdout.strip().split("\n") if line]
        assert len(lines) == 1

    def test_no_match_emits_nothing(self, populated_db: Path):
        r = _run_cli(["zzzzzzz", "--db-path", str(populated_db)])
        assert r.returncode == 0
        assert r.stdout.strip() == ""

    def test_missing_db_exits_nonzero_with_error_json(self, tmp_path: Path):
        r = _run_cli(["anything", "--db-path", str(tmp_path / "nope.sqlite")])
        assert r.returncode != 0
        err = json.loads(r.stderr.strip())
        assert "error" in err
