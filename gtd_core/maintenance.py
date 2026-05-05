"""Item-level state maintenance, called from the manual sync.

Mirrors `recurring.spawn_recurring`: a single repo argument plus an
injectable clock. Returns a count of items touched.
"""

from collections.abc import Callable
from datetime import datetime

from gtd_core.dates import defer_expired
from gtd_core.repository import EnvRepository


def clear_expired_defers(repo: EnvRepository, *, now: Callable[[], datetime] | None = None) -> int:
    """Strip `defer_until` from items whose deferment has elapsed.

    Cleanup only — `_is_hidden_by_defer` already treats expired defers as
    no longer hiding the item.
    """
    current = now() if now else datetime.now()
    cleared = 0
    for item in repo.list_items():
        if defer_expired(item.defer_until, current):
            item.defer_until = None
            repo.save(item)
            cleared += 1
    return cleared
