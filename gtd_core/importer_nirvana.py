"""Import a Nirvana CSV export into an EnvRepository.

Nirvana's columns: TYPE, PARENT, STATE, COMPLETED, FOCUS, NAME, TAGS, TIME,
ENERGY, WAITINGFOR, STARTDATE, DUEDATE, NOTES.
"""

import csv
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from gtd_core.models import Bucket, EnvConfig, Item, Project
from gtd_core.repository import EnvRepository

STATE_TO_BUCKET: dict[str, Bucket | None] = {
    "Logbook": Bucket.ARCHIVE,
    "Next": Bucket.NEXT,
    "Inbox": Bucket.INBOX,
    "Someday": Bucket.SOMEDAY,
    "Reference": Bucket.REFERENCE,
    "Scheduled/Repeating": Bucket.NEXT,
    "Waiting": Bucket.WAITING,
    "Trash": None,
    "Active": None,
}

ENERGY_MAP = {"High": "high", "Medium": "medium", "Low": "low"}

PROJECT_STATE_MAP = {
    "Active": "active",
    "Next": "active",
    "Inbox": "active",
    "Someday": "on_hold",
    "Logbook": "complete",
    "Trash": "dropped",
}

PROJECT_TYPES = {"Project", "Reference List"}


@dataclass(slots=True)
class ImportStats:
    projects: int = 0
    tasks: int = 0
    skipped: int = 0
    unknown_states: dict[str, int] = field(default_factory=dict)
    unknown_tag_tokens: set[str] = field(default_factory=set)


def import_csv(
    csv_path: Path,
    repo: EnvRepository,
    env_name: str,
    cfg: EnvConfig,
    dry_run: bool = False,
    skip_archive: bool = False,
) -> ImportStats:
    with csv_path.open() as f:
        rows = list(csv.DictReader(f))

    stats = ImportStats()
    project_map: dict[str, str] = {}  # NAME → project id
    used_ids: set[str] = set()

    project_rows = [r for r in rows if r["TYPE"] in PROJECT_TYPES]
    for row in project_rows:
        name = row.get("NAME", "").strip()
        if not name:
            stats.skipped += 1
            continue
        when = pick_timestamp(row) or datetime.now()
        pid = gen_id(when, name, used_ids)
        used_ids.add(pid)
        project_map[name] = pid

        _, tags = split_tags(row, cfg, env_name)
        project = Project(
            id=pid,
            title=name,
            body=clean_notes(row.get("NOTES")),
            created=when,
            updated=when,
            status=PROJECT_STATE_MAP.get(row["STATE"], "active"),
            outcome=None,
            tags=tags,
        )
        if not dry_run:
            repo.save_project(project)
        stats.projects += 1

    task_rows = [r for r in rows if r["TYPE"] not in PROJECT_TYPES]
    for row in task_rows:
        state = row["STATE"]
        bucket = STATE_TO_BUCKET.get(state, "missing")
        if bucket == "missing":
            stats.unknown_states[state] = stats.unknown_states.get(state, 0) + 1
            stats.skipped += 1
            continue
        if bucket is None:
            stats.skipped += 1
            continue
        if skip_archive and bucket is Bucket.ARCHIVE:
            stats.skipped += 1
            continue

        name = (row.get("NAME") or "").strip() or "(untitled)"
        when = pick_timestamp(row) or datetime.now()
        item_id = gen_id(when, name, used_ids)
        used_ids.add(item_id)

        contexts, tags = split_tags(row, cfg, env_name)
        if row.get("FOCUS"):
            tags = [*tags, "focus"]

        parent = row.get("PARENT") or ""
        project_ref = project_map.get(parent) if parent and parent != "Standalone" else None

        waiting_on = None
        if bucket is Bucket.WAITING or row.get("WAITINGFOR"):
            waiting_on = row.get("WAITINGFOR") or None

        item = Item(
            id=item_id,
            title=name,
            body=clean_notes(row.get("NOTES")),
            created=when,
            updated=when,
            status=bucket,
            contexts=contexts,
            energy=ENERGY_MAP.get(row.get("ENERGY", "")),
            time_minutes=parse_int(row.get("TIME")),
            project=project_ref,
            area=None,
            tags=tags,
            due=parse_date(row.get("DUEDATE")),
            defer_until=parse_date(row.get("STARTDATE")),
            waiting_on=waiting_on,
            waiting_since=None,
        )
        if not dry_run:
            repo.save(item)
        stats.tasks += 1

    return stats


# ---- helpers ----


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        parts = s.split("-")
        if len(parts) != 3:
            return None
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


def parse_int(s: str | None) -> int | None:
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def pick_timestamp(row: dict) -> datetime | None:
    for field_name in ("COMPLETED", "DUEDATE", "STARTDATE"):
        d = parse_date(row.get(field_name))
        if d:
            return datetime.combine(d, datetime.min.time())
    return None


def slugify_for_id(text: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = s[:max_len].rstrip("-")
    return s or "untitled"


def gen_id(when: datetime, name: str, used: set[str]) -> str:
    base = f"{when.strftime('%Y-%m-%dT%H%M')}-{slugify_for_id(name)}"
    if base not in used:
        return base
    i = 2
    while f"{base}-{i}" in used:
        i += 1
    return f"{base}-{i}"


def split_tags(
    row: dict, cfg: EnvConfig, env_name: str
) -> tuple[list[str], list[str]]:
    raw = row.get("TAGS") or ""
    if not raw:
        return [], []
    tokens = [t.strip() for t in raw.split(",") if t.strip()]
    canonical_by_lower = {c.lower(): c for c in cfg.contexts}
    env_name_lower = env_name.lower()
    contexts: list[str] = []
    tags: list[str] = []
    for t in tokens:
        t_lower = t.lower()
        if t_lower in canonical_by_lower:
            canonical = canonical_by_lower[t_lower]
            if canonical not in contexts:
                contexts.append(canonical)
        elif t_lower == env_name_lower:
            continue
        elif t not in tags:
            tags.append(t)
    return contexts, tags


def clean_notes(s: str | None) -> str:
    if not s:
        return ""
    return s.replace("\r\n", "\n").replace("\r", "\n").strip()
