import os
from pathlib import Path

from gtd_core.models import Bucket, EnvConfig, Item, Project, Template
from gtd_core.storage import (
    dump_item,
    dump_project,
    dump_template,
    list_item_paths,
    load_env_config,
    load_item,
    load_project,
    load_template,
)


class EnvRepository:
    def __init__(self, root: Path, env: str):
        self.root = Path(root)
        self.env = env
        self.env_root = self.root / env

    # ---- Items ----

    def list_items(
        self,
        bucket: Bucket | None = None,
        include_archive: bool = False,
        include_trash: bool = False,
    ) -> list[Item]:
        if bucket is not None:
            return self._list_bucket(bucket)
        buckets = list(Bucket)
        if not include_archive:
            buckets = [b for b in buckets if b is not Bucket.ARCHIVE]
        if not include_trash:
            buckets = [b for b in buckets if b is not Bucket.TRASH]
        items: list[Item] = []
        for b in buckets:
            items.extend(self._list_bucket(b))
        return items

    def _list_bucket(self, bucket: Bucket) -> list[Item]:
        return [load_item(p, bucket) for p in list_item_paths(self.env_root / bucket.value)]

    def get(self, item_id: str) -> Item | None:
        for bucket in Bucket:
            path = self.env_root / bucket.value / f"{item_id}.md"
            if path.exists():
                return load_item(path, bucket)
        return None

    def reserve_id(self, base_id: str) -> str:
        """Return `base_id`, or `base_id-2`/`-3`/... if already taken anywhere.

        Scans every bucket — including archive and trash — so a fresh capture
        can never collide with a corpse left over from soft-deletion. Callers
        should reserve immediately before saving; there is a TOCTOU window
        between reserve and save that is acceptable for single-user use.
        """
        if not self._id_exists(base_id):
            return base_id
        n = 2
        while self._id_exists(f"{base_id}-{n}"):
            n += 1
        return f"{base_id}-{n}"

    def _id_exists(self, item_id: str) -> bool:
        return any((self.env_root / b.value / f"{item_id}.md").exists() for b in Bucket)

    def save(self, item: Item) -> Item:
        path = self.env_root / item.status.value / f"{item.id}.md"
        dump_item(path, item)
        return item

    def move(self, item_id: str, new_bucket: Bucket) -> Item:
        item = self.get(item_id)
        if item is None:
            raise KeyError(item_id)
        return self.relocate(item, new_bucket)

    def relocate(self, item: Item, new_bucket: Bucket) -> Item:
        """Atomically move `item`'s file from its current bucket to `new_bucket`.

        Precondition: the file at `env_root/item.status.value/<id>.md` already
        contains the up-to-date serialized form of `item`. This primitive
        performs only the directory change — callers that need to mutate
        fields (e.g. `updated`, `working_on`) must `repo.save(item)` *before*
        calling relocate so the on-disk content is current.

        The atomic primitive is `os.replace`, which on POSIX is a single
        rename syscall and on the same filesystem is atomic. There is never
        a window in which the file exists in both buckets or in neither.
        """
        if item.status is new_bucket:
            return item
        old_path = self.env_root / item.status.value / f"{item.id}.md"
        new_path = self.env_root / new_bucket.value / f"{item.id}.md"
        new_path.parent.mkdir(parents=True, exist_ok=True)
        os.replace(old_path, new_path)
        item.status = new_bucket
        return item

    def delete(self, item_id: str) -> None:
        for bucket in Bucket:
            path = self.env_root / bucket.value / f"{item_id}.md"
            if path.exists():
                path.unlink()
                return
        raise KeyError(item_id)

    # ---- Projects ----

    def list_projects(self, include_inactive: bool = False) -> list[Project]:
        all_projects = [load_project(p) for p in list_item_paths(self.env_root / "projects")]
        if include_inactive:
            return all_projects
        return [p for p in all_projects if p.status in ("active", "on_hold")]

    def get_project(self, project_id: str) -> Project | None:
        path = self.env_root / "projects" / f"{project_id}.md"
        if path.exists():
            return load_project(path)
        return None

    def save_project(self, project: Project) -> Project:
        path = self.env_root / "projects" / f"{project.id}.md"
        dump_project(path, project)
        return project

    def delete_project(self, project_id: str) -> None:
        path = self.env_root / "projects" / f"{project_id}.md"
        if not path.exists():
            raise KeyError(project_id)
        path.unlink()

    # ---- Templates ----

    def list_templates(self) -> list[Template]:
        return [load_template(p) for p in list_item_paths(self.env_root / "templates")]

    def save_template(self, template: Template) -> Template:
        path = self.env_root / "templates" / f"{template.id}.md"
        dump_template(path, template)
        return template

    # ---- Config ----

    def load_config(self) -> EnvConfig:
        return load_env_config(self.env_root / "config.yml")
