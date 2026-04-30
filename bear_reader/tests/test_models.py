from datetime import UTC, datetime

import pytest

from bear_reader.models import Note, NoteMatch


def make_note(**overrides) -> Note:
    defaults = dict(
        unique_id="abc",
        title="Hello",
        body="world",
        tags=(),
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
        modified_at=datetime(2024, 1, 1, tzinfo=UTC),
        archived=False,
        trashed=False,
        pinned=False,
        encrypted=False,
    )
    defaults.update(overrides)
    return Note(**defaults)


class TestNote:
    def test_is_hashable(self):
        n = make_note()
        assert hash(n) == hash(make_note())

    def test_is_frozen(self):
        n = make_note()
        with pytest.raises((AttributeError, Exception)):
            n.title = "new"  # type: ignore[misc]

    def test_rejects_unknown_fields(self):
        with pytest.raises(TypeError):
            Note(  # type: ignore[call-arg]
                unique_id="abc",
                title="Hello",
                body="world",
                tags=(),
                created_at=datetime(2024, 1, 1, tzinfo=UTC),
                modified_at=datetime(2024, 1, 1, tzinfo=UTC),
                archived=False,
                trashed=False,
                pinned=False,
                encrypted=False,
                bogus="x",
            )

    def test_tags_is_tuple(self):
        n = make_note(tags=("a", "b"))
        assert n.tags == ("a", "b")


class TestNoteMatch:
    def test_carries_note_score_snippet(self):
        n = make_note()
        m = NoteMatch(note=n, score=-1.5, snippet="…<mark>foo</mark>…")
        assert m.note is n
        assert m.score == -1.5
        assert "<mark>" in m.snippet

    def test_is_frozen(self):
        m = NoteMatch(note=make_note(), score=0.0, snippet="")
        with pytest.raises((AttributeError, Exception)):
            m.score = 1.0  # type: ignore[misc]
