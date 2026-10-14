"""Grab bags: temporary, named collections of items viewed in one place.

A bag file lists item ids; items themselves are never touched by grabbing
or emptying. A bag disappears when emptied, or automatically once every
item in it is terminal (archive/trash/purged).
"""

from datetime import datetime, timedelta

import pytest

from gtd_core.models import Bucket
from gtd_core.service import GtdService


class Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 10, 14, 9, 0)

    def __call__(self) -> datetime:
        return self.now

    def tick(self, minutes: int = 1) -> None:
        self.now += timedelta(minutes=minutes)


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def svc(data_root, clock):
    return GtdService(data_root, now=clock)


def test_create_bag_persists_name_and_timestamps(svc, clock):
    bag = svc.create_grab_bag("work", "Offsite prep")
    assert bag.name == "Offsite prep"
    assert bag.created == clock.now
    assert bag.items == []
    assert bag.id.startswith("2026-10-14T0900-offsite-prep")
    reloaded = svc.repo("work").get_grab_bag(bag.id)
    assert reloaded == bag


def test_create_bag_with_item_grabs_it(svc):
    item = svc.capture("work", "Call Bob")
    bag = svc.create_grab_bag("work", "Calls", item_id=item.id)
    assert bag.items == [item.id]


def test_create_bag_with_unknown_item_raises_and_creates_nothing(svc):
    with pytest.raises(KeyError):
        svc.create_grab_bag("work", "Calls", item_id="nope")
    assert svc.repo("work").list_grab_bags() == []


def test_freshly_created_empty_bag_is_not_pruned(svc):
    bag = svc.create_grab_bag("work", "Empty for now")
    assert [b.id for b in svc.list_grab_bags("work")] == [bag.id]


def test_create_bag_rejects_blank_name(svc):
    with pytest.raises(ValueError):
        svc.create_grab_bag("work", "   ")


def test_create_bag_ids_do_not_collide(svc):
    a = svc.create_grab_bag("work", "Same")
    b = svc.create_grab_bag("work", "Same")
    assert a.id != b.id


def test_grab_adds_item_without_touching_it(svc, clock):
    item = svc.capture("work", "Call Bob")
    bag = svc.create_grab_bag("work", "Calls")
    before = svc.get_item("work", item.id)
    clock.tick()
    bag = svc.grab("work", bag.id, item.id)
    assert bag.items == [item.id]
    assert bag.updated == clock.now
    assert svc.get_item("work", item.id) == before


def test_grab_is_idempotent(svc):
    item = svc.capture("work", "Call Bob")
    bag = svc.create_grab_bag("work", "Calls")
    svc.grab("work", bag.id, item.id)
    bag = svc.grab("work", bag.id, item.id)
    assert bag.items == [item.id]


def test_grab_unknown_bag_or_item_raises_keyerror(svc):
    item = svc.capture("work", "Call Bob")
    bag = svc.create_grab_bag("work", "Calls")
    with pytest.raises(KeyError):
        svc.grab("work", "nope", item.id)
    with pytest.raises(KeyError):
        svc.grab("work", bag.id, "nope")


def test_item_can_be_in_several_bags(svc):
    item = svc.capture("work", "Call Bob")
    a = svc.create_grab_bag("work", "A")
    b = svc.create_grab_bag("work", "B")
    svc.grab("work", a.id, item.id)
    svc.grab("work", b.id, item.id)
    assert {x.id for x in svc.list_grab_bags("work")} == {a.id, b.id}


def test_list_bags_most_recently_touched_first(svc, clock):
    item = svc.capture("work", "Call Bob")
    old = svc.create_grab_bag("work", "Old")
    svc.grab("work", old.id, item.id)
    clock.tick()
    new = svc.create_grab_bag("work", "New")
    svc.grab("work", new.id, item.id)
    clock.tick()
    svc.grab("work", old.id, svc.capture("work", "Another").id)
    assert [b.name for b in svc.list_grab_bags("work")] == ["Old", "New"]


def test_get_bag_returns_items_in_grab_order(svc):
    first = svc.capture("work", "First")
    second = svc.capture("work", "Second")
    bag = svc.create_grab_bag("work", "Mix")
    svc.grab("work", bag.id, second.id)
    svc.grab("work", bag.id, first.id)
    result = svc.get_grab_bag("work", bag.id)
    assert result is not None
    got_bag, items = result
    assert got_bag.id == bag.id
    assert [i.id for i in items] == [second.id, first.id]


def test_get_bag_unknown_returns_none(svc):
    assert svc.get_grab_bag("work", "nope") is None


def test_get_bag_skips_purged_items(svc):
    keep = svc.capture("work", "Keep")
    gone = svc.capture("work", "Gone")
    bag = svc.create_grab_bag("work", "Mix")
    svc.grab("work", bag.id, keep.id)
    svc.grab("work", bag.id, gone.id)
    svc.purge("work", gone.id)
    result = svc.get_grab_bag("work", bag.id)
    assert result is not None
    assert [i.id for i in result[1]] == [keep.id]


def test_get_bag_includes_completed_items_while_others_live(svc):
    done = svc.capture("work", "Done")
    live = svc.capture("work", "Live")
    bag = svc.create_grab_bag("work", "Mix")
    svc.grab("work", bag.id, done.id)
    svc.grab("work", bag.id, live.id)
    svc.complete("work", done.id)
    result = svc.get_grab_bag("work", bag.id)
    assert result is not None
    assert [(i.id, i.status) for i in result[1]] == [
        (done.id, Bucket.ARCHIVE),
        (live.id, Bucket.INBOX),
    ]


def test_empty_bag_deletes_it_and_leaves_items_alone(svc):
    item = svc.capture("work", "Call Bob")
    svc.move("work", item.id, Bucket.NEXT)
    bag = svc.create_grab_bag("work", "Calls")
    svc.grab("work", bag.id, item.id)
    before = svc.get_item("work", item.id)
    svc.empty_grab_bag("work", bag.id)
    assert svc.get_grab_bag("work", bag.id) is None
    assert svc.list_grab_bags("work") == []
    assert svc.get_item("work", item.id) == before


def test_empty_unknown_bag_raises_keyerror(svc):
    with pytest.raises(KeyError):
        svc.empty_grab_bag("work", "nope")


@pytest.mark.parametrize("terminal", [Bucket.ARCHIVE, Bucket.TRASH])
def test_bag_auto_deleted_when_every_item_terminal(svc, terminal):
    a = svc.capture("work", "A")
    b = svc.capture("work", "B")
    bag = svc.create_grab_bag("work", "Both")
    svc.grab("work", bag.id, a.id)
    svc.grab("work", bag.id, b.id)
    svc.move("work", a.id, terminal)
    assert [x.id for x in svc.list_grab_bags("work")] == [bag.id]
    svc.move("work", b.id, terminal)
    assert svc.list_grab_bags("work") == []
    assert svc.get_grab_bag("work", bag.id) is None
    assert svc.repo("work").get_grab_bag(bag.id) is None


def test_bag_auto_deleted_when_remaining_items_purged(svc):
    a = svc.capture("work", "A")
    bag = svc.create_grab_bag("work", "One")
    svc.grab("work", bag.id, a.id)
    svc.purge("work", a.id)
    assert svc.list_grab_bags("work") == []


def test_reference_is_not_terminal_for_bags(svc):
    # Grabbing reference material to look at together is a legitimate use;
    # filing as reference must not make the bag vanish.
    item = svc.capture("work", "Spec")
    bag = svc.create_grab_bag("work", "Reading")
    svc.grab("work", bag.id, item.id)
    svc.move("work", item.id, Bucket.REFERENCE)
    assert [x.id for x in svc.list_grab_bags("work")] == [bag.id]


def test_bags_are_per_env(svc):
    svc.create_grab_bag("work", "Work bag")
    svc.grab("work", svc.list_grab_bags("work")[0].id, svc.capture("work", "x").id)
    assert svc.list_grab_bags("home") == []
