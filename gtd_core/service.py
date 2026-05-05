import difflib
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from gtd_core.dates import is_overdue, parse_human_date, parse_human_datetime
from gtd_core.models import Bucket, Energy, EnvConfig, Item, Priority, Project
from gtd_core.repository import EnvRepository

_ENERGY_RANK = {"low": 1, "medium": 2, "high": 3}


def _read_os_local_tz_name() -> str:
    # Item files store naive *local* datetimes, but Django's USE_TZ=True +
    # TIME_ZONE='UTC' makes datetime.now() return naive UTC server-side.
    # Read /etc/localtime directly so the domain clock stays local regardless.
    try:
        path = os.readlink("/etc/localtime")
    except OSError:
        return "UTC"
    marker = "/zoneinfo/"
    i = path.rfind(marker)
    return path[i + len(marker) :] if i >= 0 else "UTC"


_DEFAULT_TZ = ZoneInfo(_read_os_local_tz_name())


def _default_now() -> datetime:
    return datetime.now(_DEFAULT_TZ).replace(tzinfo=None)


# Sort sentinels for next-actions ranking. Project priority is 1-5 (1 = most
# urgent), so picking values outside that range slots items either ahead of
# or behind every rated project without comparing to None.
_ORPHAN_PRIORITY = -1
_UNRATED_PRIORITY = 99

PROJECT_STATUSES = frozenset({"active", "on_hold", "complete", "dropped"})


@dataclass(slots=True)
class AiCaptureOutcome:
    item: Item
    summary: str
    skipped_inbox: bool
    project_title: str | None


class GtdService:
    def __init__(self, root: Path, now: Callable[[], datetime] | None = None):
        self.root = Path(root)
        self._now = now or _default_now

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
        energy: Energy | None = None,
        time_minutes: int | None = None,
        contexts: list[str] | None = None,
        source_id: str | None = None,
        at_top: bool = False,
    ) -> Item:
        repo = self.repo(env)
        if contexts:
            cfg = repo.load_config()
            unknown = set(contexts) - set(cfg.contexts)
            if unknown:
                raise ValueError(f"unknown context(s): {sorted(unknown)}")

        now = self._now()
        item_id = make_item_id(now, title)
        order: int | None = None
        if at_top:
            existing = repo.list_items(bucket=Bucket.INBOX)
            min_order = min(
                (i.order for i in existing if i.order is not None),
                default=0,
            )
            order = min_order - 1
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
            source_id=source_id,
            order=order,
        )
        repo.save(item)
        return item

    def capture_ai(
        self,
        env: str,
        text: str,
        *,
        model: str = "",
    ) -> AiCaptureOutcome:
        """Run unstructured text through the AI extractor, then create the item.

        Imports from `gtd_core.ai` locally so consumers without the optional
        `anthropic` dep can still import `service`.
        """
        from gtd_core.ai import ai_capture, recent_action_titles_by_project

        repo = self.repo(env)
        cfg = repo.load_config()
        projects = self.list_projects(env, include_inactive=False)

        # Newest items first so recent_action_titles_by_project keeps the
        # current-style titles per project as in-prompt examples.
        corpus = sorted(repo.list_items(), key=lambda i: i.created, reverse=True)
        sample_actions = recent_action_titles_by_project(corpus, projects, per_project=3)

        result = ai_capture(
            text=text,
            cfg=cfg,
            projects=projects,
            sample_actions=sample_actions,
            today=self._now().date(),
            model=model,
        )

        contexts = [c for c in (result.contexts or []) if c in cfg.contexts]
        energy: Energy | None = (
            result.energy if result.energy in ("low", "medium", "high") else None
        )
        item = self.capture(
            env,
            title=result.title,
            body=result.body or "",
            energy=energy,
            time_minutes=result.time_minutes,
            contexts=contexts or None,
        )

        matched_project: Project | None = (
            self.find_project_by_title(env, result.project_query) if result.project_query else None
        )
        patch: dict = {}
        if result.area and result.area in cfg.areas:
            patch["area"] = result.area
        if matched_project is not None:
            patch["project"] = matched_project.id
        if result.due:
            patch["due"] = result.due
        if result.defer_until:
            patch["defer_until"] = result.defer_until
        if patch:
            item = self.update(env, item.id, patch)

        skipped_inbox = False
        if matched_project is not None:
            item = self.move(env, item.id, Bucket.NEXT)
            skipped_inbox = True

        return AiCaptureOutcome(
            item=item,
            summary=result.summary,
            skipped_inbox=skipped_inbox,
            project_title=matched_project.title if matched_project else None,
        )

    def move(self, env: str, item_id: str, to: Bucket) -> Item:
        repo = self.repo(env)
        item = repo.get(item_id)
        if item is None:
            raise KeyError(item_id)
        item.updated = self._now()
        if item.status is to:
            repo.save(item)
            return item
        # Working_on is a marker for "actively driving this in next" — it
        # only makes sense in the NEXT bucket. Any move out of NEXT
        # (complete, defer-via-move, re-bucket) clears it.
        if item.status is Bucket.NEXT and to is not Bucket.NEXT:
            item.working_on = False
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
        _coerce_dates(patch, now=self._now)
        for field_name, value in patch.items():
            setattr(item, field_name, value)
        # Setting a future defer_until means "I'll come back to this later" —
        # incompatible with "currently working on it". Past/None defer leaves
        # working_on alone (the user might be un-deferring something they want
        # to keep pinned).
        new_defer = patch.get("defer_until")
        if isinstance(new_defer, datetime) and new_defer > self._now():
            item.working_on = False
        item.updated = self._now()
        repo.save(item)
        return item

    def complete(self, env: str, item_id: str) -> Item:
        return self.move(env, item_id, Bucket.ARCHIVE)

    def list_done(self, env: str, *, page: int = 1, page_size: int = 50) -> tuple[list[Item], int]:
        """Return a page of archived items, most recently completed first.

        Sorted by `(updated, id)` descending — `complete()`/`move()` set
        `updated = now()` on transition, so the head is what just got ticked
        off; `id` (a chronological filename stem) breaks ties when multiple
        items share the same `updated` instant. Returns (page_slice, total).
        """
        if page < 1:
            raise ValueError(f"page must be >= 1, got {page}")
        if page_size < 1:
            raise ValueError(f"page_size must be >= 1, got {page_size}")
        items = self.repo(env).list_items(bucket=Bucket.ARCHIVE)
        items.sort(key=lambda i: (i.updated, i.id), reverse=True)
        total = len(items)
        start = (page - 1) * page_size
        return items[start : start + page_size], total

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
        min_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
        no_project: bool = False,
    ) -> list[Item]:
        """Filter a list of items by GTD-relevant criteria.

        Energy is a ceiling: energy="low" returns only low items;
        energy="high" returns low+medium+high. Items with energy=None
        are excluded when an energy filter is set.

        max_minutes excludes items with time_minutes=None or longer than the
        budget. min_minutes does the mirror — keep only items strictly longer
        than `min_minutes` (and excludes items with no time estimate). Used
        for the ">2h" filter when the user wants long, deep-work items only.

        no_project=True keeps only items with project=None (orphan next
        actions). Takes precedence over `project` if both are set.
        """
        now = self._now()
        results = []
        for item in items:
            if not include_deferred and _is_hidden_by_defer(item, now):
                continue
            if contexts and not (set(item.contexts) & set(contexts)):
                continue
            if max_minutes is not None and (
                item.time_minutes is None or item.time_minutes > max_minutes
            ):
                continue
            if min_minutes is not None and (
                item.time_minutes is None or item.time_minutes <= min_minutes
            ):
                continue
            if energy is not None and (
                item.energy is None or _ENERGY_RANK[item.energy] > _ENERGY_RANK[energy]
            ):
                continue
            if no_project:
                if item.project is not None:
                    continue
            elif project is not None and item.project != project:
                continue
            results.append(item)
        return results

    def filter_next(
        self,
        env: str,
        contexts: list[str] | None = None,
        max_minutes: int | None = None,
        min_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
    ) -> list[Item]:
        return self.list_items(
            env,
            bucket=Bucket.NEXT,
            contexts=contexts,
            max_minutes=max_minutes,
            min_minutes=min_minutes,
            energy=energy,
            project=project,
            include_deferred=include_deferred,
            respect_next_cap=True,
        )

    def actions_for_project(
        self, env: str, project_id: str, include_deferred: bool = False
    ) -> list[Item]:
        now = self._now()
        items = [
            i
            for i in self.repo(env).list_items()
            if i.project == project_id and (include_deferred or not _is_hidden_by_defer(i, now))
        ]
        return sorted(items, key=_item_sort_key)

    def reorder_project_items(self, env: str, project_id: str, item_ids: list[str]) -> list[Item]:
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
                raise ValueError(f"item {item_id} is not in project {project_id}")
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
        min_minutes: int | None = None,
        energy: str | None = None,
        project: str | None = None,
        include_deferred: bool = False,
        respect_next_cap: bool = False,
        include_archive: bool = False,
        include_trash: bool = False,
        no_project: bool = False,
        overdue: bool = False,
    ) -> list[Item]:
        items = self.repo(env).list_items(
            bucket=bucket,
            include_archive=include_archive,
            include_trash=include_trash,
        )
        filtered = self.filter_items(
            items,
            contexts=contexts,
            max_minutes=max_minutes,
            min_minutes=min_minutes,
            energy=energy,
            project=project,
            include_deferred=include_deferred,
            no_project=no_project,
        )
        if overdue:
            today = self._now().date()
            filtered = [i for i in filtered if is_overdue(i.due, today)]
        if respect_next_cap:
            projects_by_id = {p.id: p for p in self.repo(env).list_projects(include_inactive=True)}
            filtered = apply_next_item_cap(filtered, projects_by_id)
            filtered = sort_next_items(filtered, projects_by_id)
        elif bucket is Bucket.INBOX:
            # Items captured "at top" carry a negative `order` so they sort
            # ahead of the natural creation-order tail.
            filtered = sorted(filtered, key=_item_sort_key)
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
        priority: Priority | None = None,
        max_next_items: int | None = None,
    ) -> Project:
        if max_next_items is not None and max_next_items < 1:
            raise ValueError(f"max_next_items must be >= 1, got {max_next_items}")
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
            max_next_items=max_next_items,
        )
        self.repo(env).save_project(project)
        return project

    def save_project(self, env: str, project: Project) -> Project:
        return self.repo(env).save_project(project)

    def get_project(self, env: str, project_id: str) -> Project | None:
        return self.repo(env).get_project(project_id)

    def list_projects(self, env: str, include_inactive: bool = False) -> list[Project]:
        return self.repo(env).list_projects(include_inactive=include_inactive)

    def find_project_by_title(self, env: str, query: str) -> Project | None:
        """Resolve a freeform project title (or id) to a Project.

        Tries, in order: exact id match, exact case-insensitive title match,
        case-insensitive substring match, then difflib fuzzy match with
        cutoff 0.6. Returns None if nothing plausibly matches.
        """
        if not query:
            return None
        candidates = self.list_projects(env, include_inactive=False)
        if not candidates:
            return None

        for p in candidates:
            if p.id == query:
                return p

        q = query.strip().lower()
        for p in candidates:
            if p.title.lower() == q:
                return p

        substring_hits = [p for p in candidates if q in p.title.lower()]
        if len(substring_hits) == 1:
            return substring_hits[0]
        if len(substring_hits) > 1:
            # Ambiguous substring — prefer highest priority (1 = most urgent).
            substring_hits.sort(key=lambda p: (p.priority or _UNRATED_PRIORITY, p.title))
            return substring_hits[0]

        fuzzy = difflib.get_close_matches(q, [p.title.lower() for p in candidates], n=1, cutoff=0.6)
        if fuzzy:
            for p in candidates:
                if p.title.lower() == fuzzy[0]:
                    return p
        return None

    def update_project(self, env: str, project_id: str, patch: dict) -> Project:
        if "id" in patch or "created" in patch:
            raise ValueError("cannot change immutable fields id/created")
        if "status" in patch and patch["status"] not in PROJECT_STATUSES:
            raise ValueError(f"invalid status: {patch['status']}")
        if "due" in patch:
            patch["due"] = parse_human_date(patch["due"])
        if (
            "priority" in patch
            and patch["priority"] is not None
            and patch["priority"] not in (1, 2, 3, 4, 5)
        ):
            raise ValueError(f"priority must be 1-5, got {patch['priority']}")
        if (
            "max_next_items" in patch
            and patch["max_next_items"] is not None
            and patch["max_next_items"] < 1
        ):
            raise ValueError(f"max_next_items must be >= 1 or null, got {patch['max_next_items']}")
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

    # ---- Templates ----

    def list_templates(self, env: str) -> list:
        return self.repo(env).list_templates()


def _is_hidden_by_defer(item: Item, now: datetime) -> bool:
    # Defer hides an item until its defer_until — except when its due date has
    # already arrived. A stale defer_until must never swallow a missed deadline.
    if not item.defer_until or item.defer_until <= now:
        return False
    return not (item.due and item.due <= now.date())


def _item_sort_key(item: Item) -> tuple:
    # Items with explicit order come first (sorted by order). Items with no
    # order fall back to their ID, which is chronological by capture time.
    # Using (0, order) vs (1, id) ensures None-order items sort after ordered ones.
    if item.order is not None:
        return (0, item.order, item.id)
    return (1, 0, item.id)


def apply_next_item_cap(items: list[Item], projects_by_id: dict[str, Project]) -> list[Item]:
    """For each project with a `max_next_items` cap, keep only the first N in order.

    Items in uncapped projects (or no project) pass through unchanged.
    `max_next_items=1` gives the classic "sequential" behavior; higher values
    surface several ordered steps at once.

    Items flagged `working_on=True` always pass through, even when past the
    cap — pinning explicitly overrides the per-project visibility limit so the
    thing you're actively driving is never hidden.
    """
    seen_counts: dict[str, int] = {}
    result: list[Item] = []
    # Sort first so the "first" items per project are picked deterministically.
    for item in sorted(items, key=_item_sort_key):
        project = projects_by_id.get(item.project) if item.project else None
        if project is not None and project.max_next_items is not None:
            count = seen_counts.get(project.id, 0)
            if count >= project.max_next_items and not item.working_on:
                continue
            seen_counts[project.id] = count + 1
        result.append(item)
    return result


def sort_next_items(items: list[Item], projects_by_id: dict[str, Project]) -> list[Item]:
    """Order the next-actions list: orphan items → project priority → due → capture order.

    Items with no project surface at the top — they're typically standalone next
    actions that aren't tied to any larger initiative and would otherwise be
    buried under prioritised project work. Items in projects without a priority
    fall into a trailing bucket.
    """

    def key(item: Item) -> tuple:
        project = projects_by_id.get(item.project) if item.project else None
        if item.project is None:
            priority = _ORPHAN_PRIORITY
        elif project and project.priority is not None:
            priority = project.priority
        else:
            priority = _UNRATED_PRIORITY
        # (0, due) < (1,) so undated items sort after dated ones without
        # needing to compare a date to None.
        due_rank: tuple = (0, item.due) if item.due is not None else (1,)
        # Working_on items pin to the very top — False sorts before True.
        return (not item.working_on, priority, due_rank, item.id)

    return sorted(items, key=key)


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


def _coerce_dates(patch: dict, now: Callable[[], datetime] | None = None) -> None:
    """Parse natural-language strings for due (date) and defer_until (datetime).

    `now` anchors relative phrases ("3h", "in 2 hours") on the caller's clock.
    """
    if "due" in patch:
        patch["due"] = parse_human_date(patch["due"])
    if "defer_until" in patch:
        patch["defer_until"] = parse_human_datetime(patch["defer_until"], now=now)
