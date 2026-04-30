"""Synthetic Bear-shaped SQLite fixtures.

The real Bear DB schema is far larger than what we read; this fixture
mirrors only the columns and tables the reader touches. If the real
schema diverges from these assumptions, the smoke step against the live
DB will catch it.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pytest

from bear_reader.reader import APPLE_EPOCH

DEFAULT_TS = datetime(2024, 1, 1, tzinfo=UTC)


@dataclass
class NoteSpec:
    unique_id: str
    title: str = ""
    body: str = ""
    tags: tuple[str, ...] = ()
    created_at: datetime = DEFAULT_TS
    modified_at: datetime = DEFAULT_TS
    archived: bool = False
    trashed: bool = False
    pinned: bool = False
    encrypted: bool = False


def _to_apple(ts: datetime) -> float:
    return (ts - APPLE_EPOCH).total_seconds()


def make_bear_db(path: Path, notes: list[NoteSpec]) -> Path:
    """Build a synthetic Bear-shaped DB at `path`. Returns `path`."""
    import sqlite3

    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE ZSFNOTE (
                Z_PK INTEGER PRIMARY KEY,
                ZUNIQUEIDENTIFIER TEXT,
                ZTITLE TEXT,
                ZTEXT TEXT,
                ZCREATIONDATE REAL,
                ZMODIFICATIONDATE REAL,
                ZARCHIVED INTEGER,
                ZTRASHED INTEGER,
                ZPINNED INTEGER,
                ZENCRYPTED INTEGER
            );
            CREATE TABLE ZSFNOTETAG (
                Z_PK INTEGER PRIMARY KEY,
                ZTITLE TEXT
            );
            CREATE TABLE Z_5TAGS (
                Z_5NOTES INTEGER,
                Z_13TAGS INTEGER
            );
            """
        )

        tag_ids: dict[str, int] = {}
        for note_pk, spec in enumerate(notes, start=1):
            conn.execute(
                """
                INSERT INTO ZSFNOTE (
                    Z_PK, ZUNIQUEIDENTIFIER, ZTITLE, ZTEXT,
                    ZCREATIONDATE, ZMODIFICATIONDATE,
                    ZARCHIVED, ZTRASHED, ZPINNED, ZENCRYPTED
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    note_pk,
                    spec.unique_id,
                    spec.title,
                    "" if spec.encrypted else spec.body,
                    _to_apple(spec.created_at),
                    _to_apple(spec.modified_at),
                    int(spec.archived),
                    int(spec.trashed),
                    int(spec.pinned),
                    int(spec.encrypted),
                ),
            )
            for tag in spec.tags:
                if tag not in tag_ids:
                    cur = conn.execute(
                        "INSERT INTO ZSFNOTETAG (ZTITLE) VALUES (?)", (tag,)
                    )
                    tag_ids[tag] = cur.lastrowid  # type: ignore[assignment]
                conn.execute(
                    "INSERT INTO Z_5TAGS (Z_5NOTES, Z_13TAGS) VALUES (?, ?)",
                    (note_pk, tag_ids[tag]),
                )
        conn.commit()
    finally:
        conn.close()
    return path


@pytest.fixture
def bear_db_factory(tmp_path):
    """Returns a callable that builds a synthetic Bear DB."""
    counter = {"n": 0}

    def _build(notes: list[NoteSpec]) -> Path:
        counter["n"] += 1
        return make_bear_db(tmp_path / f"bear_{counter['n']}.sqlite", notes)

    return _build


@pytest.fixture
def snapshot_dir(tmp_path) -> Path:
    d = tmp_path / "snapshots"
    d.mkdir()
    return d
