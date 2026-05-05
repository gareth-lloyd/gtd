import os
from collections.abc import Callable
from datetime import date, datetime
from io import IOBase
from pathlib import Path
from typing import Any

import frontmatter
import yaml

from gtd_core.models import Bucket, EnvConfig, Item, Project, Template


def _atomic_dump(path: Path, write_fn: Callable[[IOBase], None]) -> None:
    """Write `path` atomically: serialize to a sibling tmp file, then rename.

    A crash mid-`write_fn` leaves the destination's previous content
    intact (or absent, if it never existed) — never partially-written.
    The tmp filename is PID-suffixed so concurrent writers can't collide
    on a shared scratch path. Tmp lives in the same directory as the
    destination so `os.replace` stays within one filesystem and is atomic.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f"{path.suffix}.{os.getpid()}.tmp")
    try:
        with tmp.open("wb") as f:
            write_fn(f)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def dump_item(path: Path, item: Item) -> None:
    post = frontmatter.Post(item.body, **_item_metadata(item))
    _atomic_dump(path, lambda f: frontmatter.dump(post, f))


def load_item(path: Path, status: Bucket) -> Item:
    # Status is passed in by the caller (derived from the parent directory),
    # never read from the file's frontmatter.
    md, body = _read_frontmatter(path)
    return Item(
        id=md["id"],
        title=md["title"],
        body=body,
        created=_as_datetime(md["created"]),
        updated=_as_datetime(md["updated"]),
        status=status,
        contexts=list(md.get("contexts") or []),
        energy=md.get("energy"),
        time_minutes=md.get("time_minutes"),
        project=md.get("project"),
        area=md.get("area"),
        tags=list(md.get("tags") or []),
        due=_as_date(md.get("due")),
        defer_until=_as_optional_datetime(md.get("defer_until")),
        waiting_on=md.get("waiting_on"),
        waiting_since=_as_date(md.get("waiting_since")),
        order=md.get("order"),
        source_id=md.get("source_id"),
        working_on=bool(md.get("working_on", False)),
    )


def dump_project(path: Path, project: Project) -> None:
    post = frontmatter.Post(
        project.body,
        id=project.id,
        title=project.title,
        created=project.created,
        updated=project.updated,
        status=project.status,
        outcome=project.outcome,
        area=project.area,
        tags=project.tags,
        due=project.due,
        priority=project.priority,
        max_next_items=project.max_next_items,
    )
    _atomic_dump(path, lambda f: frontmatter.dump(post, f))


def load_project(path: Path) -> Project:
    md, body = _read_frontmatter(path)
    if "sequential" in md:
        raise ValueError(
            f"{path}: legacy 'sequential' field found — run "
            "scripts/migrate_sequential_to_max_next_items.py to convert"
        )
    return Project(
        id=md["id"],
        title=md["title"],
        body=body,
        created=_as_datetime(md["created"]),
        updated=_as_datetime(md["updated"]),
        status=md.get("status", "active"),
        outcome=md.get("outcome"),
        area=md.get("area"),
        tags=list(md.get("tags") or []),
        due=_as_date(md.get("due")),
        priority=md.get("priority"),
        max_next_items=md.get("max_next_items"),
    )


def dump_env_config(path: Path, config: EnvConfig) -> None:
    data = {
        "name": config.name,
        "contexts": config.contexts,
        "areas": config.areas,
        "default_energy": config.default_energy,
    }
    payload = yaml.safe_dump(data, sort_keys=False).encode("utf-8")

    def write(f: IOBase) -> None:
        f.write(payload)

    _atomic_dump(path, write)


def load_env_config(path: Path) -> EnvConfig:
    with path.open("r") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}
    return EnvConfig(
        name=data["name"],
        contexts=list(data.get("contexts") or []),
        areas=list(data.get("areas") or []),
        default_energy=data.get("default_energy", "medium"),
    )


def dump_template(path: Path, template: Template) -> None:
    post = frontmatter.Post(
        template.body,
        id=template.id,
        title=template.title,
        contexts=template.contexts,
        energy=template.energy,
        time_minutes=template.time_minutes,
        project=template.project,
        area=template.area,
        tags=template.tags,
        recurrence=template.recurrence,
        last_spawned=template.last_spawned,
    )
    _atomic_dump(path, lambda f: frontmatter.dump(post, f))


def load_template(path: Path) -> Template:
    md, body = _read_frontmatter(path)
    return Template(
        id=md["id"],
        title=md["title"],
        body=body,
        contexts=list(md.get("contexts") or []),
        energy=md.get("energy"),
        time_minutes=md.get("time_minutes"),
        project=md.get("project"),
        area=md.get("area"),
        tags=list(md.get("tags") or []),
        recurrence=md.get("recurrence", "monthly"),
        last_spawned=_as_date(md.get("last_spawned")),
    )


def list_item_paths(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.iterdir() if p.is_file() and p.suffix == ".md")


def _read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Load a markdown file's frontmatter metadata + body.

    The metadata is widened to dict[str, Any] — the YAML payload is shaped by
    each load_X function rather than statically typed at this layer.
    """
    post = frontmatter.load(str(path))
    return dict(post.metadata), post.content


def _item_metadata(item: Item) -> dict[str, Any]:
    return {
        "id": item.id,
        "title": item.title,
        "created": item.created,
        "updated": item.updated,
        "contexts": item.contexts,
        "energy": item.energy,
        "time_minutes": item.time_minutes,
        "project": item.project,
        "area": item.area,
        "tags": item.tags,
        "due": item.due,
        "defer_until": item.defer_until,
        "waiting_on": item.waiting_on,
        "waiting_since": item.waiting_since,
        "order": item.order,
        "source_id": item.source_id,
        "working_on": item.working_on,
    }


def _as_datetime(v: Any) -> datetime:
    # PyYAML deserializes "2026-04-10" as a date and
    # "2026-04-10 09:15:00" as a datetime — handle both.
    if isinstance(v, datetime):
        return v
    if isinstance(v, date):
        return datetime.combine(v, datetime.min.time())
    if isinstance(v, str):
        return datetime.fromisoformat(v)
    raise TypeError(f"Cannot coerce {v!r} to datetime")


def _as_date(v: Any) -> date | None:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        return date.fromisoformat(v)
    raise TypeError(f"Cannot coerce {v!r} to date")


def _as_optional_datetime(v: Any) -> datetime | None:
    # Legacy date-only values (e.g. "2026-04-10") promote to midnight so
    # items stored before the hours-granularity change still load cleanly.
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    if isinstance(v, date):
        return datetime.combine(v, datetime.min.time())
    if isinstance(v, str):
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return datetime.combine(date.fromisoformat(v), datetime.min.time())
    raise TypeError(f"Cannot coerce {v!r} to datetime")
