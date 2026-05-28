import git
import pytest

import gtd_core.cloud_sync as cloud_sync
from gtd_core.cloud_sync import commit_and_push, pull_latest


@pytest.fixture(autouse=True)
def _reset_pull_throttle():
    """The pull throttle uses module-level state; reset it between tests."""
    cloud_sync._last_pull_monotonic = 0.0
    yield


def _item_md(slug: str) -> str:
    return (
        "---\n"
        f"id: {slug}\n"
        f"title: {slug}\n"
        "created: 2026-04-10 09:00:00\n"
        "updated: 2026-04-10 09:00:00\n"
        "---\n\n"
    )


def _configure(repo: git.Repo) -> None:
    with repo.config_writer() as cw:
        cw.set_value("user", "email", "test@example.com")
        cw.set_value("user", "name", "Test")


@pytest.fixture
def remote_and_clone(tmp_path):
    """A bare 'origin' plus a working clone with a committed data/ tree."""
    origin = tmp_path / "origin.git"
    git.Repo.init(origin, bare=True)

    work = tmp_path / "work"
    repo = git.Repo.clone_from(origin, work)
    _configure(repo)
    (work / "data" / "home" / "inbox").mkdir(parents=True)
    (work / "README.md").write_text("seed\n")
    repo.index.add(["README.md"])
    repo.index.commit("initial")
    repo.git.branch("-M", "main")
    repo.remote("origin").push("main", set_upstream=True)
    return origin, work, repo


class TestCommitAndPush:
    def test_pushes_new_inbox_file_to_remote(self, remote_and_clone):
        origin, work, repo = remote_and_clone
        (work / "data" / "home" / "inbox" / "task1.md").write_text(_item_md("task1"))

        result = commit_and_push(work)
        assert result.committed is True
        assert result.pushed is True

        # A fresh clone of the bare remote should see the file.
        verify = git.Repo.clone_from(origin, origin.parent / "verify")
        assert (origin.parent / "verify" / "data" / "home" / "inbox" / "task1.md").exists()
        verify.close()

    def test_noop_when_nothing_changed(self, remote_and_clone):
        _origin, work, _repo = remote_and_clone
        result = commit_and_push(work)
        assert result.committed is False
        assert result.pushed is False


class TestPullLatest:
    def test_picks_up_remote_commit(self, remote_and_clone):
        origin, work, _repo = remote_and_clone

        # A second clone pushes a new file to the remote.
        other = origin.parent / "other"
        other_repo = git.Repo.clone_from(origin, other)
        _configure(other_repo)
        (other / "data" / "home" / "inbox").mkdir(parents=True, exist_ok=True)
        (other / "data" / "home" / "inbox" / "fromphone.md").write_text(_item_md("fromphone"))
        other_repo.index.add(["data/home/inbox/fromphone.md"])
        other_repo.index.commit("from other")
        other_repo.remote("origin").push("main")
        other_repo.close()

        assert not (work / "data" / "home" / "inbox" / "fromphone.md").exists()
        pull_latest(work)
        assert (work / "data" / "home" / "inbox" / "fromphone.md").exists()

    def test_invalid_repo_does_not_raise(self, tmp_path):
        """best-effort contract: a non-repo path logs and returns, never raises."""
        not_a_repo = tmp_path / "plain"
        not_a_repo.mkdir()
        pull_latest(not_a_repo)  # would raise InvalidGitRepositoryError if uncaught

    def test_throttled_within_interval(self, remote_and_clone, monkeypatch):
        origin, work, _repo = remote_and_clone
        # First pull is allowed and picks up nothing new.
        pull_latest(work)

        # Second clone pushes a new commit.
        other = origin.parent / "other2"
        other_repo = git.Repo.clone_from(origin, other)
        _configure(other_repo)
        (other / "data" / "home" / "inbox").mkdir(parents=True, exist_ok=True)
        (other / "data" / "home" / "inbox" / "late.md").write_text(_item_md("late"))
        other_repo.index.add(["data/home/inbox/late.md"])
        other_repo.index.commit("late")
        other_repo.remote("origin").push("main")
        other_repo.close()

        # Immediately after the first pull, a second pull is throttled (no-op).
        pull_latest(work)
        assert not (work / "data" / "home" / "inbox" / "late.md").exists()

        # Once the throttle window passes, the next pull fetches it.
        monkeypatch.setattr(cloud_sync, "_last_pull_monotonic", 0.0)
        pull_latest(work)
        assert (work / "data" / "home" / "inbox" / "late.md").exists()
