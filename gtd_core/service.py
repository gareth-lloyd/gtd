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
        item_id = f"{now.strftime('%Y-%m-%dT%H%M')}-{slugify(title)}"
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
        item = repo.move(item_id, to)
        item.updated = self._now()
        repo.save(item)
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
        items = self.repo(env).list_items(bucket=Bucket.NEXT)
        return self.filter_items(
            items,
            contexts=contexts,
            max_minutes=max_minutes,
            energy=energy,
            project=project,
            include_deferred=include_deferred,
        )

    def actions_for_project(self, env: str, project_id: str) -> list[Item]:
        return [i for i in self.repo(env).list_items() if i.project == project_id]

    # ---- Projects ----

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


def slugify(text: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = s[:max_len].rstrip("-")
    return s or "untitled"


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
