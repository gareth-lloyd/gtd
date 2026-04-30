from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Note:
    """A Bear note. Read-only snapshot — never written back."""

    unique_id: str
    title: str
    body: str
    tags: tuple[str, ...]
    created_at: datetime
    modified_at: datetime
    archived: bool
    trashed: bool
    pinned: bool
    encrypted: bool


@dataclass(frozen=True, slots=True)
class NoteMatch:
    """A search hit: the note plus its BM25 score and a highlighted snippet.

    BM25 scores are negative — closer to 0 is more relevant.
    """

    note: Note
    score: float
    snippet: str
