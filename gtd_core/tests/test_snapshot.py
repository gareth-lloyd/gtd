import git
import pytest

from gtd_core.snapshot import PullResult, pull, snapshot, snapshot_status


def _item_md(slug: str, body: str = "") -> str:
    """Minimal valid frontmatter so snapshot()'s unloadable-guard accepts it."""
    return (
        "---\n"
        f"id: {slug}\n"
        f"title: {slug}\n"
        "created: 2026-04-10 09:00:00\n"
        "updated: 2026-04-10 09:00:00\n"
        "---\n"
        f"{body}\n"
    )


@pytest.fixture
def repo_root(tmp_path):
    repo = git.Repo.init(tmp_path)
    with repo.config_writer() as cw:
        cw.set_value("user", "email", "test@example.com")
        cw.set_value("user", "name", "Test")
    (tmp_path / "data" / "work" / "inbox").mkdir(parents=True)
    code = tmp_path / "code.py"
    code.write_text("print('hello')\n")
    repo.index.add([str(code)])
    repo.index.commit("initial")
    return tmp_path


def _configure(repo: git.Repo, email: str = "test@example.com", name: str = "Test") -> None:
    with repo.config_writer() as cw:
        cw.set_value("user", "email", email)
        cw.set_value("user", "name", name)


@pytest.fixture
def remote_and_clone(tmp_path):
    """A bare 'origin' plus a working clone tracking origin/main."""
    origin = tmp_path / "origin.git"
    # Pin the initial branch so the fixture doesn't depend on the host's
    # init.defaultBranch (CI runners default to "master", not "main").
    git.Repo.init(origin, bare=True, initial_branch="main")
    work = tmp_path / "work"
    repo = git.Repo.clone_from(origin, work)
    _configure(repo)
    (work / "data" / "home" / "inbox").mkdir(parents=True)
    (work / "README.md").write_text("seed\n")
    repo.index.add(["README.md"])
    repo.index.commit("initial")
    repo.git.branch("-M", "main")
    repo.remote("origin").push("main", set_upstream=True)
    return origin, work


def _push_from_second_clone(origin, slug: str) -> None:
    """Simulate a phone capture: a second clone pushes a new inbox file."""
    other = origin.parent / f"other-{slug}"
    other_repo = git.Repo.clone_from(origin, other)
    _configure(other_repo, email="phone@example.com", name="Phone")
    inbox = other / "data" / "home" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / f"{slug}.md").write_text(_item_md(slug))
    other_repo.index.add([f"data/home/inbox/{slug}.md"])
    other_repo.index.commit(f"capture {slug}")
    other_repo.remote("origin").push("main")
    other_repo.close()


class TestPull:
    def test_applies_remote_commit_and_reports_changed(self, remote_and_clone):
        origin, work = remote_and_clone
        _push_from_second_clone(origin, "fromphone")

        assert not (work / "data" / "home" / "inbox" / "fromphone.md").exists()
        result = pull(work)

        assert result.pulled is True
        assert result.changed is True
        assert result.error is None
        assert (work / "data" / "home" / "inbox" / "fromphone.md").exists()

    def test_nothing_new_reports_unchanged(self, remote_and_clone):
        _origin, work = remote_and_clone
        result = pull(work)
        assert result.pulled is True
        assert result.changed is False

    def test_autostashes_local_edits(self, remote_and_clone):
        """An uncommitted local edit survives a pull that brings remote commits."""
        origin, work = remote_and_clone
        (work / "README.md").write_text("local edit not yet committed\n")
        _push_from_second_clone(origin, "phoneitem")

        result = pull(work)

        assert result.changed is True
        assert (work / "data" / "home" / "inbox" / "phoneitem.md").exists()
        assert (work / "README.md").read_text() == "local edit not yet committed\n"

    def test_no_remote_is_noop(self, repo_root):
        result = pull(repo_root)
        assert result.pulled is False
        assert result.changed is False
        assert result.error is None

    def test_invalid_repo_returns_error_not_raises(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        result = pull(plain)  # must not raise
        assert result.pulled is False
        assert result.error is not None

    def test_unborn_head_with_remote_does_not_raise(self, tmp_path):
        """A remote configured before the first commit must not crash pull().

        repo.head.commit raises ValueError (not GitError) on an unborn branch;
        the best-effort contract requires a PullResult, never an exception.
        """
        work = tmp_path / "unborn"
        repo = git.Repo.init(work)
        _configure(repo)
        origin = tmp_path / "empty-origin.git"
        git.Repo.init(origin, bare=True)
        repo.create_remote("origin", str(origin))

        result = pull(work)  # would raise ValueError before the is_valid() guard
        assert isinstance(result, PullResult)


def test_git_lock_shared_and_reentrant():
    """commit_and_push holds the lock and calls snapshot(), which re-acquires it.

    That only works if (a) both use the same lock object and (b) it is reentrant.
    """
    import gtd_core.cloud_sync as cloud_sync
    from gtd_core import snapshot as snap

    assert cloud_sync._git_lock is snap._git_lock
    with snap._git_lock, snap._git_lock:  # RLock: same-thread re-entry must not deadlock
        pass


class TestSnapshot:
    def test_no_changes_returns_noop(self, repo_root):
        result = snapshot(repo_root)
        assert result.committed is False
        assert result.files_changed == 0

    def test_creates_commit_for_new_data_file(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        result = snapshot(repo_root)
        assert result.committed is True
        assert result.files_changed == 1
        assert result.sha is not None

        repo = git.Repo(repo_root)
        for f in repo.head.commit.stats.files:
            assert str(f).startswith("data/")

    def test_only_stages_data_dir(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        (repo_root / "new_code.py").write_text("x = 1\n")
        snapshot(repo_root)
        repo = git.Repo(repo_root)
        assert "new_code.py" in list(repo.untracked_files)

    def test_ignores_modified_code_files(self, repo_root):
        """Modifications to code files are not swept into data snapshots."""
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        (repo_root / "code.py").write_text("print('modified')\n")
        result = snapshot(repo_root)
        assert result.committed is True

        repo = git.Repo(repo_root)
        for f in repo.head.commit.stats.files:
            assert str(f).startswith("data/")
        # code.py should still be modified (not staged, not committed)
        assert repo.is_dirty()

    def test_custom_message(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        snapshot(repo_root, message="weekly review")
        repo = git.Repo(repo_root)
        assert str(repo.head.commit.message).startswith("weekly review")

    def test_generated_message_format(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "a.md").write_text(_item_md("a"))
        (repo_root / "data" / "work" / "inbox" / "b.md").write_text(_item_md("b"))
        snapshot(repo_root)
        repo = git.Repo(repo_root)
        msg = str(repo.head.commit.message)
        assert "snapshot" in msg
        assert "2 files" in msg

    def test_modified_file_counted(self, repo_root):
        path = repo_root / "data" / "work" / "inbox" / "item1.md"
        path.write_text(_item_md("item1", "original"))
        snapshot(repo_root)
        path.write_text(_item_md("item1", "modified"))
        result = snapshot(repo_root)
        assert result.committed is True
        assert result.files_changed == 1

    def test_deleted_file_counted(self, repo_root):
        path = repo_root / "data" / "work" / "inbox" / "item1.md"
        path.write_text(_item_md("item1"))
        snapshot(repo_root)
        path.unlink()
        result = snapshot(repo_root)
        assert result.committed is True
        assert result.files_changed == 1


class TestSnapshotPush:
    def test_successful_push_clears_error(self, repo_root, tmp_path):
        bare = tmp_path / "origin.git"
        git.Repo.init(bare, bare=True)
        repo = git.Repo(repo_root)
        repo.create_remote("origin", str(bare))

        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        result = snapshot(repo_root, push=True)

        assert result.committed is True
        assert result.pushed is True
        assert result.push_error is None

    def test_push_failure_captures_error_message(self, repo_root, tmp_path):
        repo = git.Repo(repo_root)
        repo.create_remote("origin", str(tmp_path / "does-not-exist"))

        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        result = snapshot(repo_root, push=True)

        assert result.committed is True
        assert result.pushed is False
        assert result.push_error is not None
        assert result.push_error != ""

    def test_no_push_requested_leaves_error_none(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text(_item_md("item1"))
        result = snapshot(repo_root, push=False)

        assert result.committed is True
        assert result.pushed is False
        assert result.push_error is None


class TestSnapshotStatus:
    def test_clean(self, repo_root):
        status = snapshot_status(repo_root)
        assert status.dirty_count == 0
        assert status.dirty_files == []

    def test_untracked_data_file(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "new.md").write_text("x")
        status = snapshot_status(repo_root)
        assert status.dirty_count == 1
        assert any("new.md" in f for f in status.dirty_files)

    def test_ignores_non_data_changes(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "new.md").write_text("x")
        (repo_root / "unrelated.py").write_text("y")
        status = snapshot_status(repo_root)
        assert status.dirty_count == 1
        assert not any("unrelated" in f for f in status.dirty_files)


class TestSnapshotStatusUnloadableFiles:
    """A corrupt YAML in any bucket must surface so the user sees it in the UI.

    `unloadable_files` lists relative paths under `data/` that exist as `.md`
    files but fail to load. Empty list when everything parses.
    """

    def test_no_unloadable_files_when_clean(self, repo_root):
        (repo_root / "data" / "work" / "inbox").mkdir(parents=True, exist_ok=True)
        status = snapshot_status(repo_root)
        assert status.unloadable_files == []

    def test_lists_unloadable_item_file(self, repo_root):
        broken = repo_root / "data" / "work" / "inbox" / "broken.md"
        broken.parent.mkdir(parents=True, exist_ok=True)
        broken.write_text('---\nid: broken\ntitle: "unbalanced\ncreated: 2026-04-10\n---\nbody\n')
        status = snapshot_status(repo_root)
        assert any("broken.md" in f for f in status.unloadable_files)

    def test_unloadable_paths_are_relative_to_repo_root(self, repo_root):
        broken = repo_root / "data" / "work" / "inbox" / "broken.md"
        broken.parent.mkdir(parents=True, exist_ok=True)
        broken.write_text('---\nid: broken\ntitle: "unbalanced\ncreated: 2026-04-10\n---\nbody\n')
        status = snapshot_status(repo_root)
        for f in status.unloadable_files:
            assert not f.startswith("/")
            assert f.startswith("data/")

    def test_unchanged_files_are_not_reparsed_on_repeat_call(self, repo_root, monkeypatch):
        """Polled every 10s by the UI — unchanged files must not re-open + re-parse."""
        from gtd_core import snapshot as snapshot_mod

        good = repo_root / "data" / "work" / "inbox" / "good.md"
        good.parent.mkdir(parents=True, exist_ok=True)
        good.write_text("---\nid: good\ntitle: ok\ncreated: 2026-04-10\nupdated: 2026-04-10\n---\n")

        snapshot_mod._unloadable_cache.clear()
        calls = {"n": 0}
        real_load_item = snapshot_mod.load_item

        def counting_load(*args, **kwargs):
            calls["n"] += 1
            return real_load_item(*args, **kwargs)

        monkeypatch.setattr(snapshot_mod, "load_item", counting_load)

        snapshot_status(repo_root)
        first = calls["n"]
        snapshot_status(repo_root)
        # Second call hits the cache — no further loads for unchanged files.
        assert calls["n"] == first


class TestSnapshotRefusesUnloadable:
    """`snapshot()` must refuse to commit if any item/project/template is unloadable.

    Baking a broken file into git silently strands it (the UI hides it, the
    service can't update it). Better to surface the breakage and require a
    fix before commit.
    """

    def test_refuses_commit_with_unloadable_file(self, repo_root):
        from gtd_core import snapshot as snapshot_mod

        snapshot_mod._unloadable_cache.clear()
        (repo_root / "data" / "work" / "inbox" / "good.md").write_text(
            "---\nid: good\ntitle: ok\ncreated: 2026-04-10\nupdated: 2026-04-10\n---\n"
        )
        broken = repo_root / "data" / "work" / "inbox" / "broken.md"
        broken.write_text('---\nid: broken\ntitle: "unbalanced\ncreated: 2026-04-10\n---\nbody\n')

        result = snapshot(repo_root)

        assert result.committed is False
        assert result.sha is None
        assert any("broken.md" in f for f in result.unloadable_files)
        # The good file must NOT be committed either — refuse-all-or-nothing.
        repo = git.Repo(repo_root)
        assert not any("good.md" in str(f) for f in repo.head.commit.stats.files), (
            "snapshot committed despite unloadable sibling"
        )
