---
area: null
completed_at: null
contexts: []
created: 2026-10-01 10:59:07.112640
defer_until: null
due: null
energy: low
id: 2026-10-01T1059-newly-created-enquiry-should-navigate-straight-to
order: null
output: |
  ## Agent run 2026-10-01 11:47:42.228312
  Done on branch `feat/enquiry-create-to-builder` (worktree `.claude/worktrees/enquiry-create-to-builder`), commit c282a1bd. Not merged to main.

  **Change:** `frontend/src/features/enquiries/components/EnquiryFormDialog.tsx` — after a successful create the dialog now navigates to `enquiryQuoteBuilderPath(created.id)` (`/enquiries/<id>/quote-builder`) instead of `/enquiries/<id>`. Edit mode is unchanged. No new i18n strings.

  **Why it is safe:** the "New enquiry" button on the list page is already disabled without the reservations role, which is the same role the builder gates on, so the builder's no-role redirect toast cannot fire on this path. A lost/converted status is impossible on a just-created enquiry.

  **TDD:** tightened the existing test in `EnquiryFormDialog.test.tsx` to assert the exact `/enquiries/42/quote-builder` pathname (it previously used a substring match on `/enquiries/42`, which would have kept passing). Red confirmed before the code change, green after.

  **Quality gate:** dialog test file 18/18; full vitest 2830 passed, 1 failed; eslint, prettier, tsc all clean; pre-commit hooks passed on commit. The one failure is `RateWorkbenchPage.test.tsx` "period create" — the already-filed BUG-047 real-clock flake, unrelated to this change.

  **Next (your call):** ff-merge the branch into main (per the ship memory: ExitWorktree first), then remove the worktree.

  ## /code-review on the branch (2026-10-01 11:55:00.047467)
  No correctness bug found; role claim verified against `useHasReservationsRole` and `IsReservationsWriter` on the enquiry viewset. Four findings, none applied:
  1. Redirect is unconditional — non-quote request types (info/brochure/availability/other) also land in the builder. Task asked for unconditional; branch on `created.request_type === "quote"` if you want otherwise. Product call.
  2. Dialog hard-codes its post-create destination; reviewer suggests an `onCreated` callback owned by the list page. Only one create caller today, left as is.
  3. `useCreateEnquiry` never seeds the detail cache from the 201 body, so the builder waits on a second GET. Pre-existing; one-line `setQueryData` fix.
  4. My test asserts the path twice with a misleading comment; collapse to one anchored regex match. Trivial cleanup.
  ## Agent run 2026-10-01 12:12:16.524848 — review fixes applied, merged to main
  Per your instruction: applied review findings 3 and 4 on the branch, rebased onto main (no file overlap with the BUG-049/BUG-050 commits that landed meanwhile), ff-merged, removed the worktree and branch.
  - 08599426 feat(frontend): newly created enquiry navigates straight to the quote builder
  - 974619da fix(frontend): seed the enquiry detail cache on create; tidy the builder-redirect test — `useCreateEnquiry` now `setQueryData`s the detail from the 201 body (new test proves no second GET; confirmed red without the seed), and the navigation test is one anchored regex match.
  Gate: full vitest green bar the known BUG-047 flake; eslint/prettier/tsc clean; pre-commit passed. Post-merge on main: enquiries folder 176/176, tsc clean.
  Not done (your call): finding 1 (only redirect for request_type "quote") and finding 2 (`onCreated` callback on the dialog).
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: Newly created enquiry should navigate straight to builder
updated: 2026-10-01 12:12:16.524848
waiting_on: null
waiting_since: null
working_on: false
---
