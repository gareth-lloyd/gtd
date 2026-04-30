from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .reader import BearReader
from .serializers import (
    NoteMatchSerializer,
    NoteQuerySerializer,
    NoteSerializer,
    SearchQuerySerializer,
)

_reader: BearReader | None = None
_reader_path: Path | None = None


def _reset_reader_for_tests() -> None:
    """Test hook to drop the cached reader (path may have changed)."""
    global _reader, _reader_path
    _reader = None
    _reader_path = None


def _get_reader() -> BearReader | Response:
    global _reader, _reader_path
    path = Path(settings.BEAR_DB_PATH)
    if _reader is None or _reader_path != path:
        try:
            snapshot_dir = getattr(settings, "BEAR_READER_SNAPSHOT_DIR", None)
            _reader = BearReader(
                path,
                snapshot_dir=Path(snapshot_dir) if snapshot_dir else None,
            )
            _reader_path = path
        except FileNotFoundError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
    else:
        _reader.refresh()
    return _reader


@api_view(["GET"])
def list_notes(request: Request) -> Response:
    reader = _get_reader()
    if isinstance(reader, Response):
        return reader

    q = NoteQuerySerializer(data=request.query_params)
    if not q.is_valid():
        return Response(q.errors, status=status.HTTP_400_BAD_REQUEST)

    params = q.validated_data
    notes = reader.find_notes(
        tag=params.get("tag"),
        title_like=params.get("q"),
        include_trashed=params.get("include_trashed", False),
        include_archived=params.get("include_archived", True),
        limit=params.get("limit", 50),
    )
    return Response(NoteSerializer(notes, many=True).data)


@api_view(["GET"])
def get_note(request: Request, unique_id: str) -> Response:
    reader = _get_reader()
    if isinstance(reader, Response):
        return reader
    note = reader.get_note(unique_id)
    if note is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(NoteSerializer(note).data)


@api_view(["GET"])
def search_notes(request: Request) -> Response:
    reader = _get_reader()
    if isinstance(reader, Response):
        return reader

    q = SearchQuerySerializer(data=request.query_params)
    if not q.is_valid():
        return Response(q.errors, status=status.HTTP_400_BAD_REQUEST)

    params = q.validated_data
    matches = reader.search_notes(
        params["q"],
        include_trashed=params.get("include_trashed", False),
        include_archived=params.get("include_archived", True),
        limit=params.get("limit", 50),
    )
    return Response(NoteMatchSerializer(matches, many=True).data)
