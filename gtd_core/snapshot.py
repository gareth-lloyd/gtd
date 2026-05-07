from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import git

from gtd_core.models import Bucket
from gtd_core.storage import list_item_paths, load_item, load_project, load_template

DATA_PATHSPEC = "data"


@dataclass(slots=True)
class SnapshotResult:
    committed: bool
    sha: str | None = None
    files_changed: int = 0
    message: str = ""
    pushed: bool = False
    push_error: str | None = None


@dataclass(slots=True)
class SnapshotStatus:
    dirty_count: int
    dirty_files: list[str] = field(default_factory=list)
    unloadable_files: list[str] = field(default_factory=list)


def snapshot(
    repo_root: Path,
    message: str | None = None,
    push: bool = False,
) -> SnapshotResult:
    repo = git.Repo(repo_root)
    # Stage all changes (additions, modifications, deletions) under data/ only.
    # The "-- data" pathspec in the commit below ensures code files that happen
    # to be staged are NOT included in the snapshot commit.
    repo.git.add("-A", "--", DATA_PATHSPEC)

    staged = repo.git.diff("--cached", "--name-only", "--", DATA_PATHSPEC)
    staged_files = [line for line in staged.splitlines() if line]
    if not staged_files:
        return SnapshotResult(committed=False)

    files_changed = len(staged_files)
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        suffix = "file" if files_changed == 1 else "files"
        message = f"snapshot: {timestamp} — {files_changed} {suffix} changed"

    repo.git.commit("-m", message, "--", DATA_PATHSPEC)
    sha = repo.head.commit.hexsha

    pushed = False
    push_error: str | None = None
    if push:
        try:
            repo.remote("origin").push("HEAD")
            pushed = True
        except (git.GitCommandError, ValueError) as exc:
            push_error = str(exc).strip() or exc.__class__.__name__

    return SnapshotResult(
        committed=True,
        sha=sha,
        files_changed=files_changed,
        message=message,
        pushed=pushed,
        push_error=push_error,
    )


def snapshot_status(repo_root: Path) -> SnapshotStatus:
    repo = git.Repo(repo_root)
    dirty: list[str] = []

    changed = repo.git.diff("--name-only", "--", DATA_PATHSPEC)
    dirty.extend(line for line in changed.splitlines() if line)

    for f in repo.untracked_files:
        if f.startswith(f"{DATA_PATHSPEC}/"):
            dirty.append(f)

    return SnapshotStatus(
        dirty_count=len(dirty),
        dirty_files=sorted(set(dirty)),
        unloadable_files=_scan_unloadable(repo_root),
    )


def _scan_unloadable(repo_root: Path) -> list[str]:
    """Repo-root-relative paths of `.md` files that fail to parse.

    The frontend polls `snapshot_status` every 10s. Re-parsing every file in
    every bucket on every poll would dominate CPU as the archive grows, so
    results are memoized per `(path, mtime_ns)` and only changed files re-load.
    """
    data_dir = repo_root / DATA_PATHSPEC
    if not data_dir.is_dir():
        return []
    bad: list[str] = []
    envs = sorted(p for p in data_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    for env_dir in envs:
        for bucket in Bucket:
            _collect_unloadable(
                env_dir / bucket.value, lambda p, b=bucket: load_item(p, b), repo_root, bad
            )
        _collect_unloadable(env_dir / "projects", load_project, repo_root, bad)
        _collect_unloadable(env_dir / "templates", load_template, repo_root, bad)
    return sorted(set(bad))


_unloadable_cache: dict[tuple[str, int], bool] = {}


def _collect_unloadable(
    directory: Path,
    loader: Callable[[Path], object],
    repo_root: Path,
    bad: list[str],
) -> None:
    for path in list_item_paths(directory):
        try:
            mtime = path.stat().st_mtime_ns
        except OSError:
            continue
        key = (str(path), mtime)
        cached = _unloadable_cache.get(key)
        if cached is None:
            try:
                loader(path)
                cached = False
            except Exception:
                cached = True
            _unloadable_cache[key] = cached
        if cached:
            bad.append(str(path.relative_to(repo_root)))
