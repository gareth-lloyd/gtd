"""CLI entrypoint for searching Bear notes from outside Django.

Used by the user-global Claude Code skill ``bear-search``. Emits one
JSON object per matching note on stdout (newline-delimited). Errors go
to stderr as a single JSON object and exit non-zero.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .reader import BearReader

DEFAULT_DB_PATH = Path(
    "~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/"
    "Application Data/database.sqlite"
).expanduser()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bear_reader.cli",
        description="Read-only search over Bear notes (FTS5).",
    )
    parser.add_argument("query", help="FTS5 search query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH)
    parser.add_argument(
        "--include-trashed", action="store_true", default=False
    )
    parser.add_argument(
        "--include-archived",
        dest="include_archived",
        action="store_false",
        default=True,
        help="Exclude archived notes (included by default).",
    )
    args = parser.parse_args(argv)

    try:
        reader = BearReader(args.db_path)
    except FileNotFoundError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    matches = reader.search_notes(
        args.query,
        limit=args.limit,
        include_trashed=args.include_trashed,
        include_archived=args.include_archived,
    )
    for m in matches:
        print(
            json.dumps(
                {
                    "id": m.note.unique_id,
                    "title": m.note.title,
                    "tags": list(m.note.tags),
                    "snippet": m.snippet,
                    "modified": m.note.modified_at.isoformat(),
                    "score": m.score,
                }
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
