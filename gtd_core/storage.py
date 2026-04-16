from datetime import date, datetime
from pathlib import Path
from typing import Any

import frontmatter
import yaml

from gtd_core.models import Bucket, EnvConfig, Item, Project, Template


def dump_item(path: Path, item: Item) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    post = frontmatter.Post(item.body, **_item_metadata(item))
    with path.open("wb") as f:
        frontmatter.dump(post, f)


def load_item(path: Path, status: Bucket) -> Item:
    # Status is passed in by the caller (derived from the parent directory),
    # never read from the file's frontmatter.
    post = frontmatter.load(str(path))
    md = post.metadata
    return Item(
        id=md["id"],
        title=md["title"],
        body=post.content,
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
        defer_until=_as_date(md.get("defer_until")),
        waiting_on=md.get("waiting_on"),
        waiting_since=_as_date(md.get("waiting_since")),
        order=md.get("order"),
    )


def dump_project(path: Path, project: Project) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
        sequential=project.sequential,
    )
    with path.open("wb") as f:
        frontmatter.dump(post, f)


def load_project(path: Path) -> Project:
    post = frontmatter.load(str(path))
    md = post.metadata
    return Project(
        id=md["id"],
        title=md["title"],
        body=post.content,
        created=_as_datetime(md["created"]),
        updated=_as_datetime(md["updated"]),
        status=md.get("status", "active"),
        outcome=md.get("outcome"),
        area=md.get("area"),
        tags=list(md.get("tags") or []),
        due=_as_date(md.get("due")),
        priority=md.get("priority"),
        sequential=bool(md.get("sequential", False)),
    )


def dump_env_config(path: Path, config: EnvConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "name": config.name,
        "contexts": config.contexts,
        "areas": config.areas,
        "default_energy": config.default_energy,
    }
    with path.open("w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def load_env_config(path: Path) -> EnvConfig:
    with path.open("r") as f:
        data = yaml.safe_load(f) or {}
    return EnvConfig(
        name=data["name"],
        contexts=list(data.get("contexts") or []),
        areas=list(data.get("areas") or []),
        default_energy=data.get("default_energy", "medium"),
    )


def dump_template(path: Path, template: Template) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    with path.open("wb") as f:
        frontmatter.dump(post, f)


def load_template(path: Path) -> Template:
    post = frontmatter.load(str(path))
    md = post.metadata
    return Template(
        id=md["id"],
        title=md["title"],
        body=post.content,
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
