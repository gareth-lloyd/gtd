"""Score `/gtd` against `/gtd2` for every morning both ran.

Stateless: each run rebuilds `scoreboard.md` from the two skills' output
directories and the GTD data, so truth that arrives later is back-filled
without bookkeeping. Truth comes only from what the user did afterwards:

  promoted   an item later captured with `from-awareness`. A miss for whichever
             version left it in awareness, a hit for whichever would have
             captured it.
  trashed    a `morning-gtd` capture later moved to trash. An over-capture for
             whichever version captured (or would have captured) it.

Usage: uv run python -m gtd_triage.compare
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from gtd_core.models import Bucket, Item
from gtd_core.service import GtdService
from gtd_triage import render
from gtd_triage.labels import CAPTURED_TAG, PROMOTED_TAG, join_key
from gtd_triage.paths import DATA_ROOT, GTD2_OUTPUT, GTD_SKILL_OUTPUT

TRIAGE_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-triage\.json$")
SCOREBOARD = "scoreboard.md"


@dataclass
class Day:
    day: str
    gtd_captured: set[str] = field(default_factory=set)
    gtd2_captured: set[str] = field(default_factory=set)
    gtd_aware: dict[str, str] = field(default_factory=dict)
    gtd2_aware: dict[str, str] = field(default_factory=dict)
    gtd2_rank: dict[str, int] = field(default_factory=dict)
    gtd_dives: set[str] = field(default_factory=set)
    gtd2_dives: set[str] = field(default_factory=set)
    gtd_context_chars: int = 0
    gtd2_context_chars: int = 0
    jev_status: str = ""
    promoted: set[str] = field(default_factory=set)
    trashed: set[str] = field(default_factory=set)


def _load(path: Path) -> Any:
    return json.loads(path.read_text()) if path.exists() else None


def _index_entries(loaded: Any) -> list[dict[str, Any]]:
    if loaded is None:
        return []
    return loaded["index"] if isinstance(loaded, dict) else loaded


def _gtd_blob_for(day: str) -> dict[str, Any] | None:
    blobs = sorted(GTD_SKILL_OUTPUT.glob(f"{day}-*-breadth.json"))
    return json.loads(blobs[-1].read_text()) if blobs else None


def load_day(day: str, gtd_items: list[Item]) -> Day:
    result = Day(day=day)
    triage: dict[str, Any] = _load(GTD2_OUTPUT / f"{day}-triage.json") or {"entries": []}
    result.jev_status = (triage.get("jev") or {}).get("status", "")
    result.gtd2_context_chars = len(render.llm_view(triage)) if triage.get("date") else 0
    ranked = [e for e in triage["entries"] if not e.get("folded_into")]
    ranked.sort(key=lambda e: -(e.get("attention") or 0.0))
    result.gtd2_rank = {join_key(e["source_id"]): n for n, e in enumerate(ranked, start=1)}
    result.gtd2_dives = {join_key(d["source_id"]) for d in triage.get("dives") or []}

    would = _load(GTD2_OUTPUT / f"{day}-would-capture.json") or {"items": []}
    result.gtd2_captured = {join_key(i["source_id"]) for i in would["items"]}
    for entry in _index_entries(_load(GTD2_OUTPUT / f"{day}-awareness-index.json")):
        result.gtd2_aware[join_key(entry["source_id"])] = entry.get("section") or ""
    for entry in _index_entries(_load(GTD_SKILL_OUTPUT / f"{day}-awareness-index.json")):
        if entry.get("source_id"):
            result.gtd_aware[join_key(entry["source_id"])] = entry.get("section") or ""

    blob = _gtd_blob_for(day)
    if blob:
        slim = {k: v for k, v in blob.items() if k not in ("by_source", "dives")}
        result.gtd_context_chars = len(json.dumps(slim, ensure_ascii=False, separators=(",", ":")))
        result.gtd_dives = {join_key(d["source_id"]) for d in blob.get("dives") or []}

    seen = set(result.gtd_aware) | set(result.gtd2_aware) | result.gtd2_captured
    for item in gtd_items:
        if not item.source_id or CAPTURED_TAG not in item.tags:
            continue
        key = join_key(item.source_id)
        created = item.created.date().isoformat()
        if PROMOTED_TAG in item.tags:
            if created >= day and key in seen:
                result.promoted.add(key)
            continue
        if created == day:
            result.gtd_captured.add(key)
        if item.status == Bucket.TRASH and key in (result.gtd_captured | result.gtd2_captured):
            result.trashed.add(key)
    return result


def day_section(d: Day) -> list[str]:
    both = d.gtd_captured & d.gtd2_captured
    only_gtd = d.gtd_captured - d.gtd2_captured
    only_gtd2 = d.gtd2_captured - d.gtd_captured
    moved = {k for k in set(d.gtd_aware) & set(d.gtd2_aware) if d.gtd_aware[k] != d.gtd2_aware[k]}
    ranks = sorted(d.gtd2_rank[k] for k in d.gtd_captured if k in d.gtd2_rank)
    lines = [
        f"## {d.day}",
        "",
        f"- Jev: {d.jev_status or 'no gtd2 run'}",
        f"- Captured by both: {len(both)} · only `/gtd`: {len(only_gtd)} · "
        f"only `/gtd2`: {len(only_gtd2)}",
        f"- Awareness entries: `/gtd` {len(d.gtd_aware)} · `/gtd2` {len(d.gtd2_aware)} · "
        f"section differs on {len(moved)}",
        f"- `/gtd` captures ranked by `/gtd2` attention (of {len(d.gtd2_rank)}): {ranks or 'n/a'}",
        f"- Context injected: `/gtd` {d.gtd_context_chars:,} chars · "
        f"`/gtd2` {d.gtd2_context_chars:,} chars",
        f"- Dives: `/gtd` {len(d.gtd_dives)} · `/gtd2` {len(d.gtd2_dives)} · "
        f"same target {len(d.gtd_dives & d.gtd2_dives)}",
        f"- Promoted later: {len(d.promoted)} "
        f"(missed by `/gtd` {len(d.promoted - d.gtd_captured)}, "
        f"missed by `/gtd2` {len(d.promoted - d.gtd2_captured)})",
        f"- Trashed later: {len(d.trashed)} "
        f"(`/gtd` captured {len(d.trashed & d.gtd_captured)}, "
        f"`/gtd2` would have {len(d.trashed & d.gtd2_captured)})",
    ]
    for label, keys in (("Only `/gtd`", only_gtd), ("Only `/gtd2`", only_gtd2)):
        lines += [f"  - {label}: {key}" for key in sorted(keys)]
    return lines + [""]


def scoreboard(days: list[Day]) -> str:
    def total(pick: Any) -> int:
        return sum(len(pick(d)) for d in days)

    lines = [
        "# /gtd vs /gtd2 scoreboard",
        "",
        f"Mornings compared: {len(days)} · rebuilt {date.today().isoformat()}",
        "",
        "| | `/gtd` | `/gtd2` |",
        "|---|---|---|",
        f"| Captures | {total(lambda d: d.gtd_captured)} | {total(lambda d: d.gtd2_captured)} |",
        f"| Missed (you promoted it later) | {total(lambda d: d.promoted - d.gtd_captured)} "
        f"| {total(lambda d: d.promoted - d.gtd2_captured)} |",
        f"| Over-captured (you trashed it) | {total(lambda d: d.trashed & d.gtd_captured)} "
        f"| {total(lambda d: d.trashed & d.gtd2_captured)} |",
        f"| Context injected (chars) | {sum(d.gtd_context_chars for d in days):,} "
        f"| {sum(d.gtd2_context_chars for d in days):,} |",
        "",
        "Wall time is not recorded by either skill, so it is not compared here.",
        "",
    ]
    for d in reversed(days):
        lines += day_section(d)
    return "\n".join(lines)


def main() -> int:
    svc = GtdService(DATA_ROOT)
    items = svc.list_items("work", bucket=None, include_archive=True, include_trash=True)
    day_names = sorted(
        m.group(1) for p in GTD2_OUTPUT.glob("*-triage.json") if (m := TRIAGE_NAME_RE.match(p.name))
    )
    days = [load_day(day, items) for day in day_names]
    GTD2_OUTPUT.mkdir(parents=True, exist_ok=True)
    out = GTD2_OUTPUT / SCOREBOARD
    out.write_text(scoreboard(days))
    print(f"{len(days)} mornings -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
