"""GTD domain models.

Item fields:
  id            str       filename stem, immutable after creation (YYYY-MM-DDTHHMM-slug)
  title         str       human-readable, editable freely
  body          str       markdown notes
  created       datetime  set once at capture
  updated       datetime  bumped on every service-layer mutation
  status        Bucket    derived from parent directory on load, NOT stored in frontmatter
  contexts      list[str] validated against env config.yml
  energy        str|None  "low" | "medium" | "high"
  time_minutes  int|None  estimate in minutes
  project       str|None  id of a linked Project
  area          str|None  responsibility area (validated against config)
  tags          list[str] free-form
  due           date|None hard deadline only
  defer_until   datetime|None GTD tickler — hidden from default lists until this moment
  waiting_on    str|None  who/what (meaningful when status=waiting)
  waiting_since date|None when we started waiting
  source_id     str|None  stable external ref (PR url, Linear ID, Slack permalink) for dedup
  working_on    bool      pin to top of next-actions; auto-cleared when the item leaves NEXT
                          or gets a future defer_until
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from typing import Literal

Energy = Literal["low", "medium", "high"]
ProjectStatus = Literal["active", "on_hold", "complete", "dropped"]


class Bucket(StrEnum):
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
    defer_until: datetime | None = None
    waiting_on: str | None = None
    waiting_since: date | None = None
    order: int | None = None
    source_id: str | None = None
    working_on: bool = False


Priority = Literal[1, 2, 3, 4, 5]


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
    due: date | None = None
    priority: Priority | None = None
    max_next_items: int | None = None


@dataclass(slots=True)
class Template:
    id: str
    title: str
    body: str
    contexts: list[str] = field(default_factory=list)
    energy: Energy | None = None
    time_minutes: int | None = None
    project: str | None = None
    area: str | None = None
    tags: list[str] = field(default_factory=list)
    recurrence: str = "monthly"
    last_spawned: date | None = None


@dataclass(slots=True)
class EnvConfig:
    name: str
    contexts: list[str]
    areas: list[str]
    default_energy: Energy = "medium"
