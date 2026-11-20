---
area: null
completed_at: 2026-11-19 19:17:40.053431
contexts: []
created: 2026-11-19 16:42:27.304017
defer_until: null
due: null
energy: low
id: 2026-11-19T1642-i-don-t-love-teh-date-picker-behavior
order: 2
output: |
  ## Agent run 2026-11-19
  Investigated only, no code changed.

  Where it lives: one shared component, frontend/src/components/form/DateRangePicker.tsx (UncontrolledDateRangePicker wraps it). Every range field uses it: bookings (create/modify), owner block requests, rate periods, discounts, extras, assignments, services, changeover rules, intake rates.

  Why it behaves this way: handleSelect passes through react-day-picker v10's default `addToRange` (before the start = extend before, after the end = extend after, inside = move the end). The component docstring says this is "pinned by test" and that `resetOnSelect` stays off. Tests: DateRangePicker.test.tsx:198-275 ("keeps the library's default extend/shrink re-click semantics"). I found nothing in decisions.md or todo/ that requires it, so it is a default we chose, not a binding decision.

  Proposed change (the usual "alternating clicks" picker):
  - Keep a local `awaitingEnd` flag in the component.
  - Click 1 (or any click once a range is complete) sets the start. In nights mode it still draws one night as a preview. Sets awaitingEnd = true.
  - Click 2 sets the end. A click before the start makes that day the new start (some pickers swap the two dates instead; restarting is simpler). Sets awaitingEnd = false.
  - The flag resets when the popover opens, so reopening a saved range starts a fresh pick.
  - react-day-picker's `resetOnSelect` does most of this. But nights mode's one-night preview makes the range look complete after click 1, so the component needs its own flag. That's a few lines in handleSelect, not a library swap.
  - Keep: blocking a range that crosses blocked days, same-day changeover checkout, typed ISO inputs.
  - Optional: on hover, draw the range in progress up to the hovered day.

  Cost: about 1-2 hours. Rewrite the "default addToRange" tests to the new rules and update the docstring. Callers need no API change. Hosts' tests that click twice from an empty state should still pass. Any test that extends a saved range with one click will fail.

  Next step if you want it: ticket it in django_res_design/todo/ (or just /workflow-ship it).

  Addendum 2026-11-19 (blocked days):
  - Blocked-day rules are right for villas and stay: same-day changeover checkout, and no range that crosses a booking.
  - Change: today a click past the next booking silently resets the range to that day, which looks like a bug. Instead, while the picker waits for the end, grey out every day after the next changeover day so that click can't happen. Drop the reset.
  - To check: can you check in on another booking's checkout day? If a form puts a booking's checkout day itself in disabledDays (e.g. a 10th-15th booking greys out the 15th), arriving that morning is wrongly blocked. Look at how the booking dialogs build disabledDays (CreateBookingDialog, ModifyDatesDialog, BlockRequestDialog).
  - Days mode has no crossing check. Probably fine for rate periods etc., but nobody has written that down as a choice.
  - All of this fits in the same piece of work as alternating clicks.

  Ticket: filed as BUG-101, django_res_design/todo/bug-101-date-range-picker-click-semantics.md (commit 03ba256b on main, not pushed).
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: I don't love teh date picker behavior.
updated: 2026-11-19 19:17:40.053402
waiting_on: null
waiting_since: null
working_on: false
---

current:
before period - extend before. 
after period - extend after
in period, make clicked date last day

Most pickers have a stateful thing going on where alt clicks do beginning, end