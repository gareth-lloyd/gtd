"""Git sync helpers for the cloud (mobile) deployment.

The Render container is an ephemeral clone of this repo. Captures must be
pushed back to GitHub to survive a restart, and reads pull first so the phone
reflects edits made locally. Render runs one worker with a few threads, so a
module-level lock serializes every git operation — concurrent pulls/pushes on
the same working tree would corrupt the index. (That single-worker assumption
is asserted at boot in scripts/gunicorn_config.py.)

Both helpers are best-effort: any git failure — including a missing/invalid
repo — logs and returns rather than 500-ing a request. Reuses ``snapshot()``
for the commit step so the data-only pathspec and unloadable-file guard stay in
one place.
"""

import logging
import time
from pathlib import Path

import git

from gtd_core.snapshot import SnapshotResult, _git_lock, snapshot

logger = logging.getLogger(__name__)

# Reuse the one reentrant lock that guards every working-tree git mutation (see
# gtd_core.snapshot). commit_and_push holds it while calling snapshot(), which
# re-acquires it — safe because it's an RLock on the same thread.

# Reads pull-rebase so the phone sees local edits, but a GET shouldn't trigger a
# GitHub round-trip more than this often — rapid tab-switching would otherwise
# hammer the remote and hold the lock against concurrent reads. Freshness within
# a few seconds is plenty for a single-user tool.
PULL_MIN_INTERVAL_SECONDS = 10.0
_last_pull_monotonic = 0.0


def pull_latest(repo_root: Path) -> None:
    """Rebase the working tree onto the remote (best-effort, throttled)."""
    global _last_pull_monotonic
    with _git_lock:
        now = time.monotonic()
        if now - _last_pull_monotonic < PULL_MIN_INTERVAL_SECONDS:
            return
        _last_pull_monotonic = now
        try:
            git.Repo(repo_root).git.pull("--rebase", "--autostash")
        except git.GitError as exc:
            logger.warning("cloud_sync pull failed: %s", str(exc).strip())


def commit_and_push(repo_root: Path, message: str | None = None) -> SnapshotResult:
    """Commit data/ changes then push to origin.

    Pulls (rebasing) between commit and push so a local push doesn't cause a
    non-fast-forward reject. Inbox files have unique timestamped names, so the
    rebase is effectively conflict-free. Returns the SnapshotResult so callers
    can tell whether the data actually reached GitHub (``pushed`` /
    ``push_error``) — on the ephemeral Render filesystem an un-pushed commit is
    lost on the next restart, so that signal must not be ignored.
    """
    with _git_lock:
        try:
            result = snapshot(repo_root, message=message, push=False)
        except git.GitError as exc:
            logger.warning("cloud_sync commit failed: %s", str(exc).strip())
            return SnapshotResult(committed=False, push_error=str(exc).strip())
        if not result.committed:
            return result

        try:
            repo = git.Repo(repo_root)
            repo.git.pull("--rebase", "--autostash")
            repo.remote("origin").push("HEAD")
            result.pushed = True
        except (git.GitError, ValueError) as exc:
            result.push_error = str(exc).strip() or exc.__class__.__name__
            logger.warning("cloud_sync push failed: %s", result.push_error)
        return result
