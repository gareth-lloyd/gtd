"""Spawn inbox items from recurring templates.

Called before each snapshot (sync). For each template, if enough time
has elapsed since last_spawned, creates a new inbox item and updates
the template's last_spawned date.
"""

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from gtd_core.models import Bucket, Item, Template
from gtd_core.repository import EnvRepository
from gtd_core.service import slugify

RECURRENCE_DELTAS = {
    "daily": lambda: timedelta(days=1),
    "weekly": lambda: timedelta(weeks=1),
    "biweekly": lambda: timedelta(weeks=2),
    "monthly": lambda: relativedelta(months=1),
    "quarterly": lambda: relativedelta(months=3),
    "yearly": lambda: relativedelta(years=1),
}


def next_spawn_date(recurrence: str, last: date) -> date:
    factory = RECURRENCE_DELTAS.get(recurrence)
    if factory:
        return last + factory()
    # "every_N_days" pattern
    if recurrence.startswith("every_") and recurrence.endswith("_days"):
        n = int(recurrence[6:-5])
        return last + timedelta(days=n)
    raise ValueError(f"Unknown recurrence: {recurrence!r}")


def is_due(template: Template, today: date) -> bool:
    if template.last_spawned is None:
        return True
    return next_spawn_date(template.recurrence, template.last_spawned) <= today


def spawn_from_template(template: Template, repo: EnvRepository, today: date) -> Item:
    from datetime import datetime

    now = datetime.combine(today, datetime.min.time())
    item_id = f"{today.strftime('%Y-%m-%dT%H%M')}-{slugify(template.title)}"
    item = Item(
        id=item_id,
        title=template.title,
        body=template.body,
        created=now,
        updated=now,
        status=Bucket.INBOX,
        contexts=list(template.contexts),
        energy=template.energy,
        time_minutes=template.time_minutes,
        project=template.project,
        area=template.area,
        tags=list(template.tags),
    )
    repo.save(item)
    template.last_spawned = today
    repo.save_template(template)
    return item


def spawn_recurring(repo: EnvRepository, today: date | None = None) -> list[Item]:
    if today is None:
        today = date.today()
    spawned = []
    for template in repo.list_templates():
        if is_due(template, today):
            item = spawn_from_template(template, repo, today)
            spawned.append(item)
    return spawned
