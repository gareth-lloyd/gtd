from datetime import UTC, datetime

import pytest

from bear_reader.models import Note, NoteMatch
from bear_reader.reader import BearReader

from .conftest import NoteSpec


class TestInit:
    def test_raises_when_db_missing(self, tmp_path, snapshot_dir):
        missing = tmp_path / "nope.sqlite"
        with pytest.raises(FileNotFoundError) as exc:
            BearReader(missing, snapshot_dir=snapshot_dir)
        assert str(missing) in str(exc.value)


class TestGetNote:
    def test_returns_note_by_unique_id(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="abc", title="Hello", body="world"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        note = reader.get_note("abc")
        assert isinstance(note, Note)
        assert note.unique_id == "abc"
        assert note.title == "Hello"
        assert note.body == "world"

    def test_returns_none_when_missing(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory([])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert reader.get_note("missing") is None

    def test_includes_flags(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", archived=True),
                NoteSpec(unique_id="b", trashed=True),
                NoteSpec(unique_id="c", pinned=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        a = reader.get_note("a")
        b = reader.get_note("b")
        c = reader.get_note("c")
        assert a is not None and b is not None and c is not None
        assert a.archived is True
        assert b.trashed is True
        assert c.pinned is True

    def test_includes_tags(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", tags=("foo", "bar/baz")),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        note = reader.get_note("a")
        assert note is not None
        assert set(note.tags) == {"foo", "bar/baz"}


class TestDateConversion:
    def test_apple_epoch_zero_is_2001(self, bear_db_factory, snapshot_dir):
        epoch = datetime(2001, 1, 1, tzinfo=UTC)
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", created_at=epoch, modified_at=epoch),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        note = reader.get_note("a")
        assert note is not None
        assert note.created_at == epoch
        assert note.modified_at == epoch

    def test_arbitrary_date_round_trips(self, bear_db_factory, snapshot_dir):
        ts = datetime(2024, 6, 15, 14, 30, tzinfo=UTC)
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", created_at=ts, modified_at=ts),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        note = reader.get_note("a")
        assert note is not None
        assert note.created_at == ts


class TestFindNotes:
    def test_returns_all_active_notes_by_default(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="Alpha"),
                NoteSpec(unique_id="b", title="Beta"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes()}
        assert ids == {"a", "b"}

    def test_filter_by_tag(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", tags=("foo",)),
                NoteSpec(unique_id="b", tags=("bar",)),
                NoteSpec(unique_id="c", tags=("foo", "bar")),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(tag="foo")}
        assert ids == {"a", "c"}

    def test_filter_by_nested_tag_exact_match(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", tags=("person/ryan-rogers",)),
                NoteSpec(unique_id="b", tags=("person",)),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(tag="person/ryan-rogers")}
        assert ids == {"a"}

    def test_title_like_is_case_insensitive_substring(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="Ryan onboarding notes"),
                NoteSpec(unique_id="b", title="ryan 1:1"),
                NoteSpec(unique_id="c", title="other"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(title_like="ryan")}
        assert ids == {"a", "b"}

    def test_excludes_trashed_by_default(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="kept"),
                NoteSpec(unique_id="b", title="gone", trashed=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes()}
        assert ids == {"a"}

    def test_includes_trashed_when_requested(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a"),
                NoteSpec(unique_id="b", trashed=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(include_trashed=True)}
        assert ids == {"a", "b"}

    def test_includes_archived_by_default(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a"),
                NoteSpec(unique_id="b", archived=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes()}
        assert ids == {"a", "b"}

    def test_excludes_archived_when_requested(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a"),
                NoteSpec(unique_id="b", archived=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(include_archived=False)}
        assert ids == {"a"}

    def test_encrypted_body_is_empty(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="locked", body="should be hidden", encrypted=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        note = reader.find_notes()[0]
        assert note.encrypted is True
        assert note.body == ""
        assert note.title == "locked"

    def test_limit_caps_results(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory([NoteSpec(unique_id=f"n{i}") for i in range(10)])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert len(reader.find_notes(limit=3)) == 3

    def test_combined_tag_and_title_filter(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="Ryan 1:1", tags=("person/ryan",)),
                NoteSpec(unique_id="b", title="Ryan promo", tags=("hr",)),
                NoteSpec(unique_id="c", title="Other", tags=("person/ryan",)),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {n.unique_id for n in reader.find_notes(tag="person/ryan", title_like="ryan")}
        assert ids == {"a"}


class TestSearchNotes:
    def test_returns_match_for_simple_keyword(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="Alpha onboarding", body="welcome to the team"),
                NoteSpec(unique_id="b", title="Beta thoughts", body="something else"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        matches = reader.search_notes("onboarding")
        assert len(matches) == 1
        assert isinstance(matches[0], NoteMatch)
        assert matches[0].note.unique_id == "a"
        assert matches[0].score < 0  # BM25 ranking returns negative scores

    def test_searches_body_content(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="random", body="ryan has been doing great work"),
                NoteSpec(unique_id="b", title="other", body="unrelated content"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        matches = reader.search_notes("ryan")
        assert {m.note.unique_id for m in matches} == {"a"}

    def test_implicit_and_for_multiple_terms(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="ryan onboarding", body=""),
                NoteSpec(unique_id="b", title="ryan", body="random text"),
                NoteSpec(unique_id="c", title="onboarding", body="other person"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("ryan onboarding")}
        assert ids == {"a"}

    def test_or_query(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="alpha"),
                NoteSpec(unique_id="b", title="beta"),
                NoteSpec(unique_id="c", title="gamma"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("alpha OR beta")}
        assert ids == {"a", "b"}

    def test_prefix_query(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="onboarding new hires"),
                NoteSpec(unique_id="b", title="other"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("onboard*")}
        assert ids == {"a"}

    def test_case_insensitive(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="RYAN was here"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("ryan")}
        assert ids == {"a"}

    def test_results_ordered_by_relevance(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="title-hit", title="ryan", body="x"),
                NoteSpec(unique_id="body-hit", title="x", body="ryan ryan ryan"),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        matches = reader.search_notes("ryan")
        assert len(matches) == 2
        assert matches[0].score <= matches[1].score  # best (smallest) first

    def test_limit_caps_results(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [NoteSpec(unique_id=f"n{i}", title="match", body="") for i in range(10)]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert len(reader.search_notes("match", limit=3)) == 3

    def test_excludes_trashed_by_default(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="match"),
                NoteSpec(unique_id="b", title="match", trashed=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("match")}
        assert ids == {"a"}

    def test_includes_trashed_when_requested(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="match"),
                NoteSpec(unique_id="b", title="match", trashed=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("match", include_trashed=True)}
        assert ids == {"a", "b"}

    def test_excludes_archived_when_requested(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="match"),
                NoteSpec(unique_id="b", title="match", archived=True),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        ids = {m.note.unique_id for m in reader.search_notes("match", include_archived=False)}
        assert ids == {"a"}

    def test_returns_empty_for_no_match(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory([NoteSpec(unique_id="a", title="alpha")])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert reader.search_notes("zzzzzz") == []

    def test_snippet_highlights_match(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(
                    unique_id="a",
                    title="meeting",
                    body="Today I spoke with ryan about the project roadmap.",
                ),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        m = reader.search_notes("ryan")[0]
        assert "ryan" in m.snippet.lower()
        assert "<mark>" in m.snippet and "</mark>" in m.snippet

    def test_encrypted_body_not_indexed(self, bear_db_factory, snapshot_dir):
        # encrypted notes have empty body in our reader; body-only searches miss them.
        db = bear_db_factory(
            [
                NoteSpec(
                    unique_id="a",
                    title="locked",
                    body="secret material",  # the conftest stores '' when encrypted=True
                    encrypted=True,
                ),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert reader.search_notes("secret") == []
        assert {m.note.unique_id for m in reader.search_notes("locked")} == {"a"}

    def test_refresh_rebuilds_fts_index(self, bear_db_factory, snapshot_dir):
        from .conftest import make_bear_db

        db = bear_db_factory([NoteSpec(unique_id="a", title="alpha")])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert {m.note.unique_id for m in reader.search_notes("alpha")} == {"a"}

        make_bear_db(
            db,
            [
                NoteSpec(unique_id="a", title="alpha"),
                NoteSpec(unique_id="b", title="bravo"),
            ],
        )
        assert reader.search_notes("bravo") == []

        reader.refresh()
        assert {m.note.unique_id for m in reader.search_notes("bravo")} == {"b"}

    def test_search_results_carry_full_note(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", title="ryan", tags=("person/ryan",)),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        m = reader.search_notes("ryan")[0]
        assert isinstance(m.note, Note)
        assert m.note.tags == ("person/ryan",)


class TestRefresh:
    def test_changes_are_invisible_until_refresh(self, bear_db_factory, snapshot_dir):
        from .conftest import make_bear_db

        db = bear_db_factory([NoteSpec(unique_id="a", title="v1")])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        n = reader.get_note("a")
        assert n is not None and n.title == "v1"

        make_bear_db(db, [NoteSpec(unique_id="a", title="v2")])
        n = reader.get_note("a")
        assert n is not None and n.title == "v1"

        reader.refresh()
        n = reader.get_note("a")
        assert n is not None and n.title == "v2"


class TestListTags:
    def test_returns_sorted_unique_tags(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory(
            [
                NoteSpec(unique_id="a", tags=("zeta", "alpha")),
                NoteSpec(unique_id="b", tags=("alpha", "beta")),
            ]
        )
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert reader.list_tags() == ["alpha", "beta", "zeta"]

    def test_returns_empty_when_no_tags(self, bear_db_factory, snapshot_dir):
        db = bear_db_factory([NoteSpec(unique_id="a")])
        reader = BearReader(db, snapshot_dir=snapshot_dir)
        assert reader.list_tags() == []
