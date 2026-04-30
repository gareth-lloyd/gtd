"""Read-only access to a Bear notes SQLite database.

Bear's database is read-only by contract: snapshot it once, open the
copy with ``mode=ro&immutable=1``, and never write back. This module
is the only place in the package that touches SQLite.
"""

from __future__ import annotations

import sqlite3
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .models import Note, NoteMatch

APPLE_EPOCH = datetime(2001, 1, 1, tzinfo=UTC)

_NOTE_COLUMNS = (
    "Z_PK",
    "ZUNIQUEIDENTIFIER",
    "ZTITLE",
    "ZTEXT",
    "ZCREATIONDATE",
    "ZMODIFICATIONDATE",
    "ZARCHIVED",
    "ZTRASHED",
    "ZPINNED",
    "ZENCRYPTED",
)
_NOTE_SELECT = ", ".join(_NOTE_COLUMNS)


def _apple_to_datetime(seconds: float | None) -> datetime:
    if seconds is None:
        return APPLE_EPOCH
    return APPLE_EPOCH + timedelta(seconds=seconds)


class BearReader:
    """Read-only view onto a Bear notes database.

    Construction snapshots the live DB to an isolated file. Subsequent
    reads use the snapshot, so Bear can keep writing without affecting
    in-flight queries. Call :meth:`refresh` to re-snapshot.
    """

    def __init__(self, db_path: Path, snapshot_dir: Path | None = None) -> None:
        if not db_path.exists():
            raise FileNotFoundError(f"Bear database not found at {db_path}")
        self._source = db_path
        if snapshot_dir is None:
            snapshot_dir = Path(tempfile.mkdtemp(prefix="bear_reader_"))
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        self._snapshot = snapshot_dir / "bear.sqlite"
        self.refresh()

    def refresh(self) -> None:
        """Re-snapshot the source DB and rebuild the FTS index.

        WAL-aware via the sqlite3 backup API. The FTS index is built
        once per snapshot, so subsequent searches are sub-millisecond.
        """
        if self._snapshot.exists():
            self._snapshot.unlink()
        src = sqlite3.connect(f"file:{self._source}?mode=ro", uri=True)
        try:
            dst = sqlite3.connect(self._snapshot)
            try:
                src.backup(dst)
                _build_fts_index(dst)
            finally:
                dst.close()
        finally:
            src.close()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(
            f"file:{self._snapshot}?mode=ro&immutable=1", uri=True
        )

    def get_note(self, unique_id: str) -> Note | None:
        with self._connect() as conn:
            row = conn.execute(
                f"SELECT {_NOTE_SELECT} FROM ZSFNOTE WHERE ZUNIQUEIDENTIFIER = ?",
                (unique_id,),
            ).fetchone()
            if row is None:
                return None
            tags = self._tags_for_note_pks(conn, [row[0]]).get(row[0], ())
            return _row_to_note(row, tags)

    def find_notes(
        self,
        *,
        tag: str | None = None,
        title_like: str | None = None,
        include_trashed: bool = False,
        include_archived: bool = True,
        limit: int = 50,
    ) -> list[Note]:
        clauses: list[str] = []
        params: list[object] = []
        if not include_trashed:
            clauses.append("n.ZTRASHED = 0")
        if not include_archived:
            clauses.append("n.ZARCHIVED = 0")
        if title_like is not None:
            clauses.append("LOWER(n.ZTITLE) LIKE LOWER(?)")
            params.append(f"%{title_like}%")

        joins = ""
        if tag is not None:
            joins = (
                " JOIN Z_5TAGS j ON j.Z_5NOTES = n.Z_PK"
                " JOIN ZSFNOTETAG t ON t.Z_PK = j.Z_13TAGS"
            )
            clauses.append("t.ZTITLE = ?")
            params.append(tag)

        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = (
            f"SELECT {', '.join('n.' + c for c in _NOTE_COLUMNS)}"
            f" FROM ZSFNOTE n{joins}{where}"
            " ORDER BY n.ZMODIFICATIONDATE DESC LIMIT ?"
        )
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
            tags_by_pk = self._tags_for_note_pks(conn, [r[0] for r in rows])
            return [_row_to_note(r, tags_by_pk.get(r[0], ())) for r in rows]

    def search_notes(
        self,
        query: str,
        *,
        include_trashed: bool = False,
        include_archived: bool = True,
        limit: int = 50,
    ) -> list[NoteMatch]:
        """Full-text search against title + body, ranked by BM25.

        Query syntax follows SQLite FTS5: bare terms are implicitly ANDed,
        ``OR`` / ``NOT`` are explicit, ``term*`` is a prefix, ``"a b"`` is a
        phrase. See https://www.sqlite.org/fts5.html#full_text_query_syntax.
        """
        clauses = ["notes_fts MATCH ?"]
        params: list[object] = [query]
        if not include_trashed:
            clauses.append("n.ZTRASHED = 0")
        if not include_archived:
            clauses.append("n.ZARCHIVED = 0")

        sql = (
            f"SELECT {', '.join('n.' + c for c in _NOTE_COLUMNS)},"
            " snippet(notes_fts, -1, '<mark>', '</mark>', '…', 32) AS snippet,"
            " bm25(notes_fts) AS score"
            " FROM notes_fts JOIN ZSFNOTE n ON n.Z_PK = notes_fts.rowid"
            f" WHERE {' AND '.join(clauses)}"
            " ORDER BY bm25(notes_fts) LIMIT ?"
        )
        params.append(limit)

        with self._connect() as conn:
            try:
                rows = conn.execute(sql, params).fetchall()
            except sqlite3.OperationalError:
                # Malformed FTS query — return empty rather than 500-ing.
                return []
            tags_by_pk = self._tags_for_note_pks(conn, [r[0] for r in rows])
        return [
            NoteMatch(
                note=_row_to_note(r[: len(_NOTE_COLUMNS)], tags_by_pk.get(r[0], ())),
                snippet=r[len(_NOTE_COLUMNS)],
                score=r[len(_NOTE_COLUMNS) + 1],
            )
            for r in rows
        ]

    def list_tags(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT ZTITLE FROM ZSFNOTETAG WHERE ZTITLE IS NOT NULL"
            ).fetchall()
        return sorted(r[0] for r in rows)

    @staticmethod
    def _tags_for_note_pks(
        conn: sqlite3.Connection, note_pks: list[int]
    ) -> dict[int, tuple[str, ...]]:
        if not note_pks:
            return {}
        placeholders = ",".join("?" * len(note_pks))
        rows = conn.execute(
            f"""
            SELECT j.Z_5NOTES, t.ZTITLE
            FROM Z_5TAGS j
            JOIN ZSFNOTETAG t ON t.Z_PK = j.Z_13TAGS
            WHERE j.Z_5NOTES IN ({placeholders})
            """,
            note_pks,
        ).fetchall()
        out: dict[int, list[str]] = {pk: [] for pk in note_pks}
        for note_pk, tag_title in rows:
            out[note_pk].append(tag_title)
        return {pk: tuple(sorted(tags)) for pk, tags in out.items()}


def _build_fts_index(conn: sqlite3.Connection) -> None:
    """Create and populate the FTS5 index over title + body.

    Tokenizer chain: ``porter`` stems English words ("running" → "run")
    and delegates to ``unicode61`` for Unicode-aware case folding and
    diacritic removal. The FTS rowid mirrors ``ZSFNOTE.Z_PK`` so we can
    join straight back to the note row.
    """
    conn.executescript(
        """
        CREATE VIRTUAL TABLE notes_fts USING fts5(
            title, body,
            tokenize = "porter unicode61 remove_diacritics 2"
        );
        INSERT INTO notes_fts(rowid, title, body)
            SELECT Z_PK, COALESCE(ZTITLE, ''), COALESCE(ZTEXT, '')
            FROM ZSFNOTE;
        """
    )
    conn.commit()


def _row_to_note(row: tuple, tags: tuple[str, ...]) -> Note:
    (
        _pk,
        unique_id,
        title,
        text,
        created,
        modified,
        archived,
        trashed,
        pinned,
        encrypted,
    ) = row
    return Note(
        unique_id=unique_id or "",
        title=title or "",
        body=text or "",
        tags=tags,
        created_at=_apple_to_datetime(created),
        modified_at=_apple_to_datetime(modified),
        archived=bool(archived),
        trashed=bool(trashed),
        pinned=bool(pinned),
        encrypted=bool(encrypted),
    )
