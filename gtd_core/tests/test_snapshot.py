import git
import pytest

from gtd_core.snapshot import snapshot, snapshot_status


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


class TestSnapshot:
    def test_no_changes_returns_noop(self, repo_root):
        result = snapshot(repo_root)
        assert result.committed is False
        assert result.files_changed == 0

    def test_creates_commit_for_new_data_file(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        result = snapshot(repo_root)
        assert result.committed is True
        assert result.files_changed == 1
        assert result.sha is not None

        repo = git.Repo(repo_root)
        for f in repo.head.commit.stats.files:
            assert str(f).startswith("data/")

    def test_only_stages_data_dir(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        (repo_root / "new_code.py").write_text("x = 1\n")
        snapshot(repo_root)
        repo = git.Repo(repo_root)
        assert "new_code.py" in list(repo.untracked_files)

    def test_ignores_modified_code_files(self, repo_root):
        """Modifications to code files are not swept into data snapshots."""
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        (repo_root / "code.py").write_text("print('modified')\n")
        result = snapshot(repo_root)
        assert result.committed is True

        repo = git.Repo(repo_root)
        for f in repo.head.commit.stats.files:
            assert str(f).startswith("data/")
        # code.py should still be modified (not staged, not committed)
        assert repo.is_dirty()

    def test_custom_message(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        snapshot(repo_root, message="weekly review")
        repo = git.Repo(repo_root)
        assert str(repo.head.commit.message).startswith("weekly review")

    def test_generated_message_format(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "a.md").write_text("a")
        (repo_root / "data" / "work" / "inbox" / "b.md").write_text("b")
        snapshot(repo_root)
        repo = git.Repo(repo_root)
        msg = str(repo.head.commit.message)
        assert "snapshot" in msg
        assert "2 files" in msg

    def test_modified_file_counted(self, repo_root):
        path = repo_root / "data" / "work" / "inbox" / "item1.md"
        path.write_text("original")
        snapshot(repo_root)
        path.write_text("modified")
        result = snapshot(repo_root)
        assert result.committed is True
        assert result.files_changed == 1

    def test_deleted_file_counted(self, repo_root):
        path = repo_root / "data" / "work" / "inbox" / "item1.md"
        path.write_text("content")
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

        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        result = snapshot(repo_root, push=True)

        assert result.committed is True
        assert result.pushed is True
        assert result.push_error is None

    def test_push_failure_captures_error_message(self, repo_root, tmp_path):
        repo = git.Repo(repo_root)
        repo.create_remote("origin", str(tmp_path / "does-not-exist"))

        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        result = snapshot(repo_root, push=True)

        assert result.committed is True
        assert result.pushed is False
        assert result.push_error is not None
        assert result.push_error != ""

    def test_no_push_requested_leaves_error_none(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
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
