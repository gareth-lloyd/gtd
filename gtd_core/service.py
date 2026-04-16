import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from gtd_core.dates import parse_human_date
from gtd_core.models import Bucket, EnvConfig, Item, Project
from gtd_core.repository import EnvRepository

_ENERGY_RANK = {"low": 1, "medium": 2, "high": 3}

PROJECT_STATUSES = frozenset({"active", "on_hold", "complete", "dropped"})


class GtdService:
    def __init__(self, root: Path, now: Callable[[], datetime] | None = None):
        self.root = Path(root)
        self._now = now or datetime.now

    def list_envs(self) -> list[str]:
        if not self.root.exists():
            return []
        return sorted(
            p.name
            for p in self.root.iterdir()
            if p.is_dir() and not p.name.startswith(".") and (p / "config.yml").exists()
        )

    def repo(self, env: str) -> EnvRepository:
        return EnvRepository(self.root, env)

    def config(self, env: str) -> EnvConfig:
        return self.repo(env).load_config()

    # ---- Items ----

    def capture(
        self,
        env: str,
        title: str,
        body: str = "",
        energy: str | None = None,
        time_minutes: int | None = None,
        contexts: list[str] | None = None,
    ) -> Item:
        repo = self.repo(env)
        if contexts:
            cfg = repo.load_config()
            unknown = set(contexts) - set(cfg.contexts)
            if unknown:
                raise ValueError(f"unknown context(s): {sorted(unknown)}")

        now = self._now()
        item_id = make_item_id(now, title)
        item = Item(
            id=item_id,
            title=title,
            body=body,
            created=now,
            updated=now,
            status=Bucket.INBOX,
            energy=energy,
            time_minutes=time_minutes,
            contexts=list(contexts) if contexts else [],
        )
        repo.save(item)
        return item

    def move(self, env: str, item_id: str, to: Bucket) -> Item:
        repo = self.repo(env)
        item = repo.get(item_id)
        if item is None:
            raise KeyError(item_id)
        item.updated = self._now()
        if item.status is to:
            repo.save(item)
            return item
        old_path = repo.env_root / item.status.value / f"{item.id}.md"
        item.status = to
        repo.save(item)
        old_path.unlink()
        return item

    def update(self, env: str, item_id: str, patch: dict) -> Item:
        if "status" in patch:
            raise ValueError("cannot change status via update(); use move()")
        if "id" in patch or "created" in patch:
            raise ValueError("cannot change immutable fields id/created")
        repo = self.repo(env)
        cfg = repo.load_config()
        item = repo.get(item_id)
        if item is None:
            raise KeyError(item_id)
        _validate_patch(patch, cfg)
        _coerce_dates(patch)
        for field_name, value in patch.items():
            setattr(item, field_name, value)
        item.updated = self._now()
        repo.save(item)
        return item

    def complete(self, env: str, item_id: str) -> Item:
        return self.move(env, item_id, Bucket.ARCHIVE)

    def delete(self, env: str, item_id: str) -> Item:
        """Soft delete: move the item to the trash bucket."""
        return self.move(env, item_id, Bucket.TRASH)

    def purge(self, env: str, item_id: str) -> None:
        """Hard delete: remove the file from disk. Irreversible."""
        self.repo(env).delete(item_id)

    def filter_items(
        self,
        items: list[Item],
        contexts: list[str] | None = None,
        max_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
    ) -> list[Item]:
        """Filter a list of items by GTD-relevant criteria.

        Energy is a ceiling: energy="low" returns only low items;
        energy="high" returns low+medium+high. Items with energy=None
        are excluded when an energy filter is set.

        max_minutes excludes items with time_minutes=None (unknown
        duration doesn't fit a time budget).
        """
        today = self._now().date()
        results = []
        for item in items:
            if not include_deferred and item.defer_until and item.defer_until > today:
                continue
            if contexts and not (set(item.contexts) & set(contexts)):
                continue
            if max_minutes is not None:
                if item.time_minutes is None or item.time_minutes > max_minutes:
                    continue
            if energy is not None:
                if item.energy is None or _ENERGY_RANK[item.energy] > _ENERGY_RANK[energy]:
                    continue
            if project is not None and item.project != project:
                continue
            results.append(item)
        return results

    def filter_next(
        self,
        env: str,
        contexts: list[str] | None = None,
        max_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
    ) -> list[Item]:
        return self.list_items(
            env,
            bucket=Bucket.NEXT,
            contexts=contexts,
            max_minutes=max_minutes,
            energy=energy,
            project=project,
            include_deferred=include_deferred,
            respect_sequential=True,
        )

    def actions_for_project(self, env: str, project_id: str) -> list[Item]:
        items = [i for i in self.repo(env).list_items() if i.project == project_id]
        return sorted(items, key=_item_sort_key)

    def reorder_project_items(
        self, env: str, project_id: str, item_ids: list[str]
    ) -> list[Item]:
        """Assign order 1..N to the given items in the given sequence.

        Items not listed are not touched — callers are responsible for passing
        the complete intended ordering when reordering a full project.
        """
        repo = self.repo(env)
        now = self._now()
        updated: list[Item] = []
        for i, item_id in enumerate(item_ids, start=1):
            item = repo.get(item_id)
            if item is None:
                raise KeyError(item_id)
            if item.project != project_id:
                raise ValueError(
                    f"item {item_id} is not in project {project_id}"
                )
            if item.order != i:
                item.order = i
                item.updated = now
                repo.save(item)
            updated.append(item)
        return updated

    def list_items(
        self,
        env: str,
        bucket: Bucket | None = None,
        contexts: list[str] | None = None,
        max_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
        respect_sequential: bool = False,
    ) -> list[Item]:
        items = self.repo(env).list_items(bucket=bucket)
        filtered = self.filter_items(
            items,
            contexts=contexts,
            max_minutes=max_minutes,
            energy=energy,
            project=project,
            include_deferred=include_deferred,
        )
        if respect_sequential:
            projects_by_id = {p.id: p for p in self.repo(env).list_projects(include_inactive=True)}
            filtered = apply_sequential_hiding(filtered, projects_by_id)
        return filtered

    # ---- Projects ----

    def create_project(
        self,
        env: str,
        title: str,
        project_id: str,
        body: str = "",
        outcome: str | None = None,
        area: str | None = None,
        tags: list[str] | None = None,
        due: str | None = None,
        priority: int | None = None,
        sequential: bool = False,
    ) -> Project:
        now = self._now()
        project = Project(
            id=project_id,
            title=title,
            body=body,
            created=now,
            updated=now,
            outcome=outcome,
            area=area,
            tags=list(tags) if tags else [],
            due=parse_human_date(due),
            priority=priority,
            sequential=sequential,
        )
        self.repo(env).save_project(project)
        return project

    def save_project(self, env: str, project: Project) -> Project:
        return self.repo(env).save_project(project)

    def get_project(self, env: str, project_id: str) -> Project | None:
        return self.repo(env).get_project(project_id)

    def list_projects(self, env: str, include_inactive: bool = False) -> list[Project]:
        return self.repo(env).list_projects(include_inactive=include_inactive)

    def update_project(self, env: str, project_id: str, patch: dict) -> Project:
        if "id" in patch or "created" in patch:
            raise ValueError("cannot change immutable fields id/created")
        if "status" in patch and patch["status"] not in PROJECT_STATUSES:
            raise ValueError(f"invalid status: {patch['status']}")
        if "due" in patch:
            patch["due"] = parse_human_date(patch["due"])
        if "priority" in patch and patch["priority"] is not None:
            if patch["priority"] not in (1, 2, 3, 4, 5):
                raise ValueError(f"priority must be 1-5, got {patch['priority']}")
        repo = self.repo(env)
        project = repo.get_project(project_id)
        if project is None:
            raise KeyError(project_id)
        for field_name, value in patch.items():
            setattr(project, field_name, value)
        project.updated = self._now()
        repo.save_project(project)
        return project

    def delete_project(self, env: str, project_id: str) -> None:
        self.repo(env).delete_project(project_id)


def _item_sort_key(item: Item) -> tuple:
    # Items with explicit order come first (sorted by order). Items with no
    # order fall back to their ID, which is chronological by capture time.
    # Using (0, order) vs (1, id) ensures None-order items sort after ordered ones.
    if item.order is not None:
        return (0, item.order, item.id)
    return (1, 0, item.id)


def apply_sequential_hiding(
    items: list[Item], projects_by_id: dict[str, Project]
) -> list[Item]:
    """For each sequential project, keep only the first item in order.

    Items belonging to non-sequential projects (or no project) pass through
    unchanged. Sequential hiding is what lets `sequential=True` projects
    surface just one action at a time on the next list.
    """
    seen_sequential: set[str] = set()
    result: list[Item] = []
    # Sort first so the "first" item per project is picked deterministically.
    for item in sorted(items, key=_item_sort_key):
        project = projects_by_id.get(item.project) if item.project else None
        if project is not None and project.sequential:
            if project.id in seen_sequential:
                continue
            seen_sequential.add(project.id)
        result.append(item)
    return result


def slugify(text: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = s[:max_len].rstrip("-")
    return s or "untitled"


def make_item_id(when: datetime, title: str, max_slug: int = 50) -> str:
    return f"{when.strftime('%Y-%m-%dT%H%M')}-{slugify(title, max_slug)}"


def _validate_patch(patch: dict, cfg: EnvConfig) -> None:
    if "contexts" in patch:
        unknown = set(patch["contexts"] or []) - set(cfg.contexts)
        if unknown:
            raise ValueError(f"unknown context(s): {sorted(unknown)}")
    if "area" in patch and patch["area"] is not None and patch["area"] not in cfg.areas:
        raise ValueError(f"unknown area: {patch['area']}")


def _coerce_dates(patch: dict) -> None:
    """Parse natural-language date strings in due/defer_until fields."""
    for field in ("due", "defer_until"):
        if field in patch:
            patch[field] = parse_human_date(patch[field])
