---
area: null
completed_at: null
contexts: []
created: 2026-10-01 11:01:21.200026
defer_until: null
due: null
energy: low
id: 2026-10-01T1101-choose-very-flexible-dates-villa-with-no-fixed-cha
order: null
output: |
  ## Agent run 2026-10-01T11:42:57

  **Answer: it is the midpoint of the arrival window, and there is no choice today. Confirmed from code, not a guess.**

  How the dates are chosen (very flexible = `flexible` preset = +/-14 days):

  1. Frontend turns the enquiry into a search window: `enquiryDatesForFlexibility` in `frontend/src/features/quotations/searchCriteria.ts` opens the window 14 days before the enquiry arrival and 14 days after the last arrival in the stay (clamped at 42 days).
  2. `searchFormToCriteria` (same file) converts that window to the wire shape the backend wants: preferred arrival = window start + ceil(width/2), always a 7-night stay, `flex_days` = ceil(width/2). So the "preferred" date is the window midpoint (rounded up a day for odd widths).
     - When the search is seeded straight from the enquiry and not touched, the midpoint IS the guest's requested arrival (window is symmetric around it). It only drifts from the guest's date if the operator drags the window by hand.
  3. Backend `StayOptionsService._plan_blocks` (`django_res/reservations/services/stay_options.py` ~L473) asks `ChangeoverService.required_weekday()`. For a villa with no fixed changeover it returns None, so the service returns no candidate blocks and prices the preferred (midpoint) week as-is. One option, no alternatives. Module docstring states this: "No fixed changeover day -> a single option: the client's preferred dates."
  4. Frontend `QuoteResultLine.tsx` ~L243: with no stay options the card has no week picker and stages on the criteria dates. Nothing on the card tells the operator these dates were picked by maths rather than by the guest, and nothing lets them change them per-line.

  So the behaviour you saw is by design (the fixed-changeover week strip was the GAP-043/128 feature; any-changeover villas were explicitly left as the single preferred week).

  Existing ticket covering the long-term answer: GAP-074 `django_res_design/todo/gap-074-nightly-price-quoting-no-changeover.md` (nightly-price quoting for no-fixed-changeover villas: show full available range + per-night price). It is gated on the owner/Debbie call, Q-041 in `django_res_design/todo/questions.md`. It does not cover the small interim fix.

  **Decision needed (pick one):**

  - A. Leave as-is, add a hint on the card ("priced at the window midpoint; this villa has no fixed changeover"). Cheapest, no new behaviour.
  - B. Per-card arrival date input for any-changeover lines, default = current midpoint, repriced via the existing reprice path (`useRepriceStayOption`, same endpoint with `flex_days=0`). Frontend-only, small. Recommended as the interim fix.
  - C. Backend emits a stay option per arrival day in the window for any-changeover villas so the existing week strip appears. Works for +/-3 (7 cells) but +/-14 gives 29 cells; would need a step or cap. More work, worse UX at wide windows.
  - D. Wait for GAP-074 (nightly quoting) and do nothing now.

  If you choose A/B/C I would file it as a new GAP (next free id is GAP-152) referencing GAP-074, with the note that the enquiry-seeded default already equals the guest's requested date so the fix is about operator choice, not a wrong default.

  No files changed in the repo. No external writes.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Choose very flexible dates. Villa with no fixed changeover. How does it choose
  which dates to add
updated: 2026-10-01 11:42:57.256825
waiting_on: null
waiting_since: null
working_on: false
---

Seems to be in the middle
Needs choice