---
area: null
contexts: []
created: 2026-06-02 13:25:19.774471
defer_until: null
due: null
energy: low
id: 2026-06-02T1325-updating-booking-dates-didn-t-update-main-display
order: null
output: |
  ## Agent run 2026-06-03T18:54Z — root cause found (diagnosis only, no code changed)

  **Bug confirmed and located.** Editing dates via the modal updates the wrong
  React Query cache entry, so the main display (right-rail summary + the booking
  fed to every tab) never re-renders. Sub-resources (activity, notes, etc.) DO
  refresh, so it looks like "everything but the booking's own fields is stale."

  ### Root cause — string vs. number query-key mismatch
  - `BookingDetailLayout.tsx:69-70` is the ONLY place that reads the raw URL
    param: `const { id } = useParams<{ id: string }>(); useBooking(id);`.
    `useParams` returns a **string**, so the booking detail is cached under
    `["bookings","detail","51"]`.
  - `schemas.ts:21` defines `id: z.number()`, so `booking.id` (passed via Outlet
    context to all tabs and to the mutation hooks) is a **number** `51`.
  - `hooks.ts:147-148` `onActionSuccess` does
    `setQueryData(queryKeys.bookings.detail(booking.id), updated)` → writes to
    `["bookings","detail",51]` (numeric).
  - React Query hashes keys via `JSON.stringify`, so `"51" !== 51`. The fresh
    booking lands in an **orphan numeric-keyed entry with no observer**; the
    layout keeps observing the string-keyed entry → no re-render of dates/status.

  This affects ALL booking action mutations (confirm/cancel/decline/modify-dates/
  modify-guests/archive/restore), not just dates — the user happened to notice it
  on dates. NB the FIRST thing I checked, a `staleTime: 30s` theory, is WRONG:
  `setQueryData` notifies observers synchronously regardless of staleness.

  ### Why it slipped through
  - `OwnerBookingDetailPage.tsx:21` already does it right
    (`const bookingId = id ? Number(id) : undefined;`) — owner portal is immune;
    only the staff `BookingDetailLayout` has the bug.
  - `bookingActionsHooks.test.tsx` uses `BOOKING_ID = 51` (number) for BOTH the
    cache seed and the hook, so the test never crosses the string→number boundary
    that exists in the real app. Green test, false confidence.

  ### Recommended fix (one line, matches existing owner-portal convention)
  In `BookingDetailLayout.tsx`:
  ```tsx
  const { id } = useParams<{ id: string }>();
  const bookingId = id ? Number(id) : undefined;
  const query = useBooking(bookingId);
  ```
  This makes the detail query numeric-keyed, matching what every mutation writes,
  so the rail + tabs re-render immediately. `fetchBooking` works with either type,
  so the change is safe.

  ### Regression test to add (per project TDD gate)
  Add a test that renders `BookingDetailLayout` at route `/bookings/51` (string id
  from the URL), runs `useModifyBookingDates(51)`'s onSuccess, and asserts the
  rendered dates update — i.e. exercises the string-route / numeric-id boundary
  that `bookingActionsHooks.test.tsx` currently sidesteps.

  STOPPED here for review — did not modify code. Say the word and I'll implement
  the fix + regression test and run the frontend quality gate.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Updating booking dates - didn't update main display
updated: 2026-06-03 23:17:40.905434
waiting_on: null
waiting_since: null
working_on: false
---

I used the modal to change dates
No updtes in the main booking information area