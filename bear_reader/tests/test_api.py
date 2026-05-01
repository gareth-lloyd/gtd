import pytest
from rest_framework.test import APIClient

from bear_reader import views

from .conftest import NoteSpec


@pytest.fixture(autouse=True)
def _reset_reader_cache():
    """Drop the module-level reader cache between tests."""
    views._reset_reader_for_tests()
    yield
    views._reset_reader_for_tests()


@pytest.fixture
def api(settings, bear_db_factory, snapshot_dir):
    db = bear_db_factory(
        [
            NoteSpec(unique_id="a", title="Alpha", body="alpha body", tags=("foo",)),
            NoteSpec(unique_id="b", title="Beta", body="beta body", tags=("bar",)),
            NoteSpec(unique_id="c", title="Gamma", body="gamma body", tags=("foo", "bar")),
            NoteSpec(unique_id="t", title="Trashed", trashed=True),
        ]
    )
    settings.BEAR_DB_PATH = db
    settings.BEAR_READER_SNAPSHOT_DIR = snapshot_dir
    return APIClient()


class TestListNotes:
    def test_returns_active_notes(self, api):
        r = api.get("/bear-api/notes/")
        assert r.status_code == 200
        data = r.json()
        ids = {n["unique_id"] for n in data}
        assert ids == {"a", "b", "c"}

    def test_filter_by_tag(self, api):
        r = api.get("/bear-api/notes/?tag=foo")
        assert r.status_code == 200
        ids = {n["unique_id"] for n in r.json()}
        assert ids == {"a", "c"}

    def test_filter_by_title(self, api):
        r = api.get("/bear-api/notes/?q=alpha")
        assert r.status_code == 200
        ids = {n["unique_id"] for n in r.json()}
        assert ids == {"a"}

    def test_include_trashed(self, api):
        r = api.get("/bear-api/notes/?include_trashed=true")
        assert r.status_code == 200
        ids = {n["unique_id"] for n in r.json()}
        assert ids == {"a", "b", "c", "t"}

    def test_limit(self, api):
        r = api.get("/bear-api/notes/?limit=2")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_bad_limit_returns_400(self, api):
        r = api.get("/bear-api/notes/?limit=abc")
        assert r.status_code == 400


class TestGetNote:
    def test_returns_full_note(self, api):
        r = api.get("/bear-api/notes/a/")
        assert r.status_code == 200
        data = r.json()
        assert data["unique_id"] == "a"
        assert data["title"] == "Alpha"
        assert data["body"] == "alpha body"
        assert data["tags"] == ["foo"]
        assert "created_at" in data
        assert "modified_at" in data
        assert data["archived"] is False
        assert data["trashed"] is False
        assert data["pinned"] is False
        assert data["encrypted"] is False

    def test_unknown_id_returns_404(self, api):
        r = api.get("/bear-api/notes/missing/")
        assert r.status_code == 404


class TestSearch:
    def test_returns_match_with_snippet_and_score(self, api):
        r = api.get("/bear-api/notes/search/?q=alpha+body")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        hit = data[0]
        assert hit["note"]["unique_id"] == "a"
        assert "<mark>" in hit["snippet"]
        assert isinstance(hit["score"], float)

    def test_results_ranked_by_relevance(self, api):
        r = api.get("/bear-api/notes/search/?q=body")
        assert r.status_code == 200
        scores = [hit["score"] for hit in r.json()]
        assert scores == sorted(scores)  # ascending = best first (negative BM25)

    def test_limit(self, api):
        r = api.get("/bear-api/notes/search/?q=body&limit=2")
        assert r.status_code == 200
        assert len(r.json()) <= 2

    def test_missing_query_returns_400(self, api):
        r = api.get("/bear-api/notes/search/")
        assert r.status_code == 400

    def test_no_match_returns_empty(self, api):
        r = api.get("/bear-api/notes/search/?q=zzzzzzz")
        assert r.status_code == 200
        assert r.json() == []

    def test_returns_503_when_db_missing(self, settings, tmp_path):
        settings.BEAR_DB_PATH = tmp_path / "nope.sqlite"
        client = APIClient()
        r = client.get("/bear-api/notes/search/?q=anything")
        assert r.status_code == 503


class TestMissingDatabase:
    def test_returns_503_when_db_missing(self, settings, tmp_path):
        settings.BEAR_DB_PATH = tmp_path / "nope.sqlite"
        client = APIClient()
        r = client.get("/bear-api/notes/")
        assert r.status_code == 503
        assert "bear database not found" in r.data["error"].lower()  # type: ignore[attr-defined]
