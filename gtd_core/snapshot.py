from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import git

DATA_PATHSPEC = "data"


@dataclass(slots=True)
class SnapshotResult:
    committed: bool
    sha: str | None = None
    files_changed: int = 0
    message: str = ""
    pushed: bool = False


@dataclass(slots=True)
class SnapshotStatus:
    dirty_count: int
    dirty_files: list[str] = field(default_factory=list)


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
    if push:
        try:
            repo.remote("origin").push("HEAD")
            pushed = True
        except (git.GitCommandError, ValueError):
            pushed = False

    return SnapshotResult(
        committed=True,
        sha=sha,
        files_changed=files_changed,
        message=message,
        pushed=pushed,
    )


def snapshot_status(repo_root: Path) -> SnapshotStatus:
    repo = git.Repo(repo_root)
    dirty: list[str] = []

    changed = repo.git.diff("--name-only", "--", DATA_PATHSPEC)
    dirty.extend(line for line in changed.splitlines() if line)

    for f in repo.untracked_files:
        if f.startswith(f"{DATA_PATHSPEC}/"):
            dirty.append(f)

    return SnapshotStatus(dirty_count=len(dirty), dirty_files=sorted(set(dirty)))
