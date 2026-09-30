"""Join historical `/gtd` breadth blobs to what happened to each item.

One row per `source_id`. Labels, strongest first:

  promoted       captured with the `from-awareness` tag: `/gtd` left it in the
                 report and the user pulled it into the inbox (human label)
  overcaptured   captured by `/gtd`, later trashed (human label)
  acted          captured by `/gtd` (`morning-gtd` tag), not trashed
  aware          listed in an awareness index, never captured
  dropped        seen in a blob, in neither

Only `promoted` and `overcaptured` are human judgments. `acted`, `aware` and
`dropped` are `/gtd`'s own LLM calls, so agreeing with them shows consistency,
not correctness.

Usage: uv run python -m gtd_triage.labels
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

from gtd_core.models import Bucket
from gtd_core.service import GtdService
from gtd_triage.paths import DATA_ROOT, GTD_SKILL_OUTPUT, LABELS_PATH

CAPTURED_TAG = "morning-gtd"
PROMOTED_TAG = "from-awareness"
ACTED_ON_LABELS = frozenset({"promoted", "acted"})
HUMAN_LABELS = frozenset({"promoted", "overcaptured"})

# Fallback join keys, for captures whose source_id was written differently from
# the blob's (thread query string dropped, Linear slug dropped, Gmail fragment).
JOIN_KEY_RES = (
    re.compile(r"slack\.com/archives/(\w+/p\d+)"),
    re.compile(r"github\.com/([^/\s]+/[^/\s]+/pull/\d+)"),
    re.compile(r"linear\.app/[^/]+/issue/([A-Z]{2,5}-\d+)"),
    re.compile(r"mail\.google\.com/.*[#/]([0-9a-f]{12,})$"),
)

BLOB_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-\d{4}-breadth\.json$")
INDEX_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-awareness-index\.json$")


@dataclass
class LabelRow:
    source_id: str
    label: str
    blob_date: str
    first_seen: str
    section: str | None
    item: dict[str, Any]


@dataclass
class Outcome:
    label: str
    created: date


def join_key(source_id: str) -> str:
    for pattern in JOIN_KEY_RES:
        match = pattern.search(source_id)
        if match:
            return match.group(1)
    return source_id


def iter_blobs(output_dir: Path) -> list[tuple[date, dict[str, Any]]]:
    blobs = []
    for path in sorted(output_dir.iterdir()):
        match = BLOB_NAME_RE.match(path.name)
        if not match or path.is_symlink():
            continue
        blobs.append((date.fromisoformat(match.group(1)), json.loads(path.read_text())))
    return blobs


def load_sections(output_dir: Path) -> dict[str, str]:
    """join key -> section of its first awareness-index appearance."""
    sections: dict[str, str] = {}
    for path in sorted(output_dir.iterdir()):
        if not INDEX_NAME_RE.match(path.name):
            continue
        loaded = json.loads(path.read_text())
        # Two historical shapes: a bare list, or {"date", "index": [...]}.
        entries = loaded["index"] if isinstance(loaded, dict) else loaded
        for entry in entries:
            source_id = entry.get("source_id")
            if source_id and join_key(source_id) not in sections:
                sections[join_key(source_id)] = entry.get("section") or ""
    return sections


def load_outcomes(svc: GtdService, env: str) -> dict[str, Outcome]:
    """join key -> strongest outcome among the GTD items carrying it."""
    rank = {"promoted": 3, "overcaptured": 2, "acted": 1}
    outcomes: dict[str, Outcome] = {}
    for item in svc.list_items(env, bucket=None, include_archive=True, include_trash=True):
        if not item.source_id or CAPTURED_TAG not in item.tags:
            continue
        if PROMOTED_TAG in item.tags:
            label = "promoted"
        elif item.status == Bucket.TRASH:
            label = "overcaptured"
        else:
            label = "acted"
        key = join_key(item.source_id)
        current = outcomes.get(key)
        if current is None or rank[label] > rank[current.label]:
            outcomes[key] = Outcome(label=label, created=item.created.date())
    return outcomes


def build_rows(
    blobs: list[tuple[date, dict[str, Any]]],
    outcomes: dict[str, Outcome],
    sections: dict[str, str],
) -> list[LabelRow]:
    appearances: dict[str, list[tuple[date, dict[str, Any]]]] = {}
    for blob_date, blob in blobs:
        for item in blob.get("items") or []:
            source_id = item.get("source_id")
            if source_id:
                appearances.setdefault(join_key(source_id), []).append((blob_date, item))

    rows = []
    for key, seen in appearances.items():
        first_date, first_item = seen[0]
        outcome = outcomes.get(key)
        chosen_date, chosen_item = first_date, first_item
        if outcome is not None:
            # Judge the item as it looked on the morning it was captured.
            before = [(d, i) for d, i in seen if d <= outcome.created]
            if before:
                chosen_date, chosen_item = before[-1]
            label = outcome.label
        elif key in sections:
            label = "aware"
        else:
            label = "dropped"
        rows.append(
            LabelRow(
                source_id=chosen_item["source_id"],
                label=label,
                blob_date=chosen_date.isoformat(),
                first_seen=first_date.isoformat(),
                section=sections.get(key),
                item=chosen_item,
            )
        )
    return rows


def load_rows(path: Path = LABELS_PATH) -> list[LabelRow]:
    return [LabelRow(**json.loads(line)) for line in path.read_text().splitlines() if line]


def main() -> int:
    svc = GtdService(DATA_ROOT)
    blobs = iter_blobs(GTD_SKILL_OUTPUT)
    outcomes = load_outcomes(svc, "work")
    sections = load_sections(GTD_SKILL_OUTPUT)
    rows = build_rows(blobs, outcomes, sections)

    LABELS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LABELS_PATH.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")

    joined = {join_key(row.source_id) for row in rows}
    unjoined = Counter(o.label for sid, o in outcomes.items() if sid not in joined)
    by_label = Counter(row.label for row in rows)
    by_kind = Counter((row.item.get("kind"), row.label) for row in rows)
    print(f"blobs: {len(blobs)}  rows: {len(rows)}", file=sys.stderr)
    print(f"outcomes with a source_id: {len(outcomes)}", file=sys.stderr)
    print(f"labels: {dict(by_label)}", file=sys.stderr)
    print(f"outcomes never seen in a blob: {dict(unjoined)}", file=sys.stderr)
    for (kind, label), n in sorted(by_kind.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        print(f"  {kind!s:24} {label:13} {n}", file=sys.stderr)
    print(f"wrote {LABELS_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
