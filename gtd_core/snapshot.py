import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import git

from gtd_core.models import Bucket
from gtd_core.storage import list_item_paths, load_item, load_project, load_template

DATA_PATHSPEC = "data"

# Serializes every working-tree git mutation (commit / pull / status) so
# concurrent requests can't collide on `.git/index.lock`. The desktop runs on
# Django's threaded dev server, where a focus-triggered pull can overlap a Sync
# commit+push; on the cloud the single gunicorn worker still benefits. Reentrant
# so cloud_sync.commit_and_push (which holds the lock) can call snapshot()
# (which re-acquires it) on the same thread without deadlocking.
_git_lock = threading.RLock()


@dataclass(slots=True)
class SnapshotResult:
    committed: bool
    sha: str | None = None
    files_changed: int = 0
    message: str = ""
    pushed: bool = False
    push_error: str | None = None
    unloadable_files: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SnapshotStatus:
    dirty_count: int
    dirty_files: list[str] = field(default_factory=list)
    unloadable_files: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PullResult:
    pulled: bool  # a pull was attempted against a configured remote
    changed: bool  # HEAD moved — new commits (e.g. phone captures) came in
    error: str | None = None


def pull(repo_root: Path) -> PullResult:
    """Rebase the working tree onto its remote, surfacing whether anything new
    arrived.

    Used by the desktop to fetch captures pushed from the mobile app. Best-
    effort: a missing remote, an unborn branch (no commits yet), a transient
    network failure, or a non-repo path returns a result rather than raising — a
    failed background sync must never break the UI. ``--autostash`` preserves
    uncommitted local edits across the rebase; phone captures are always new
    uniquely-named files, so the rebase is effectively conflict-free.

    Takes the shared git lock so a focus-triggered pull can't collide with a
    concurrent commit/push on the same working tree.
    """
    try:
        with _git_lock:
            repo = git.Repo(repo_root)
            if not repo.remotes:
                return PullResult(pulled=False, changed=False)
            # An unborn HEAD (remote configured before the first commit) has no
            # commit to read — head.commit would raise ValueError, which is not
            # a GitError. Guard it so the best-effort contract holds.
            before = repo.head.commit.hexsha if repo.head.is_valid() else None
            repo.git.pull("--rebase", "--autostash")
            after = repo.head.commit.hexsha if repo.head.is_valid() else None
            return PullResult(pulled=True, changed=after != before)
    except git.GitError as exc:
        detail = str(exc).strip() or exc.__class__.__name__
        return PullResult(pulled=False, changed=False, error=detail)


def snapshot(
    repo_root: Path,
    message: str | None = None,
    push: bool = False,
) -> SnapshotResult:
    # Serialize against concurrent pull/status on the same working tree.
    with _git_lock:
        return _snapshot_locked(repo_root, message, push)


def _snapshot_locked(
    repo_root: Path,
    message: str | None,
    push: bool,
) -> SnapshotResult:
    repo = git.Repo(repo_root)

    # Refuse to commit if any item/project/template file fails to parse.
    # Baking an unloadable file into git silently strands it (the UI hides
    # it, the service can't update it, only direct file editing can recover)
    # — better to surface the breakage and let the caller fix it first.
    unloadable = _scan_unloadable(repo_root)
    if unloadable:
        return SnapshotResult(committed=False, unloadable_files=unloadable)

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
    # Read the index under the lock so a concurrent pull/commit (which rewrites
    # it) can't surface a transient git error during the 10s status poll.
    with _git_lock:
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
