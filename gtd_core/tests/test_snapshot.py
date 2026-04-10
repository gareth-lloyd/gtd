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
            assert f.startswith("data/")

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
            assert f.startswith("data/")
        # code.py should still be modified (not staged, not committed)
        assert repo.is_dirty()

    def test_custom_message(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "item1.md").write_text("content")
        snapshot(repo_root, message="weekly review")
        repo = git.Repo(repo_root)
        assert repo.head.commit.message.startswith("weekly review")

    def test_generated_message_format(self, repo_root):
        (repo_root / "data" / "work" / "inbox" / "a.md").write_text("a")
        (repo_root / "data" / "work" / "inbox" / "b.md").write_text("b")
        snapshot(repo_root)
        repo = git.Repo(repo_root)
        msg = repo.head.commit.message
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
