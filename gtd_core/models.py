from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Literal

Energy = Literal["low", "medium", "high"]
ProjectStatus = Literal["active", "on_hold", "complete", "dropped"]


class Bucket(str, Enum):
    INBOX = "inbox"
    NEXT = "next"
    WAITING = "waiting"
    SOMEDAY = "someday"
    REFERENCE = "reference"
    ARCHIVE = "archive"
    TRASH = "trash"


@dataclass(slots=True)
class Item:
    id: str
    title: str
    body: str
    created: datetime
    updated: datetime
    status: Bucket
    contexts: list[str] = field(default_factory=list)
    energy: Energy | None = None
    time_minutes: int | None = None
    project: str | None = None
    area: str | None = None
    tags: list[str] = field(default_factory=list)
    due: date | None = None
    defer_until: date | None = None
    waiting_on: str | None = None
    waiting_since: date | None = None


@dataclass(slots=True)
class Project:
    id: str
    title: str
    body: str
    created: datetime
    updated: datetime
    status: ProjectStatus = "active"
    outcome: str | None = None
    area: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EnvConfig:
    name: str
    contexts: list[str]
    areas: list[str]
    default_energy: Energy = "medium"
