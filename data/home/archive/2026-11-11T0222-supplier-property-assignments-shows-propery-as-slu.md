---
area: null
completed_at: 2026-11-12 10:41:35.941182
contexts: []
created: 2026-11-11 02:22:03.865308
defer_until: null
due: null
energy: low
id: 2026-11-11T0222-supplier-property-assignments-shows-propery-as-slu
order: 9
output: |-
  ## Agent run 2026-11-12T09:42

  Fixed and committed on a branch; NOT merged to main (your call).

  - Branch `fix/assignment-property-name`, commit `62d8d995`, worktree
    `~/projects/villacollective/.claude/worktrees/assignment-property-name`.
  - Cause: the company Properties tab (`frontend/src/features/companies/tabs/PropertiesTab.tsx`)
    labelled each row with `property_slug`, because `GET /organisations/{id}/properties`
    returned no name at all. The contact Properties tab had the same bug (it is the
    tab the company one was copied from), so I fixed both.
  - Change: both `/properties` actions (`accounts/views/organisation.py`,
    `accounts/views/contact.py`) now return `property_name` (`display_name`, else the
    internal name). Both tabs render it, falling back to slug, then `#id`, only if a
    row has no name. Row click still routes by slug.
  - Checks: backend `accounts` API tests for contacts + organisations pass (135);
    the two PropertiesTab vitest files pass (10); pre-commit hooks (ruff, mypy,
    import-linter, eslint, prettier, tsc) pass. The full suites (pre-push) were not run,
    and I did not look at it in a browser.
  - To land: `git merge --ff-only fix/assignment-property-name` on main, then push
    (the push hook runs the full tests), then remove the worktree.

  ## Agent run 2026-11-12T09:50 (after /code-review)

  Second commit on the same branch (see `git log -2 fix/assignment-property-name`).
  Applied from the review: `property_name` is now explicitly
  `display_name or name` (no reliance on `Property.__str__`); backend tests tell
  the display name from the internal name and cover the empty-display-name
  fallback; the contact tab trims the slug in its fallback and tests the `#id` case.
  Same scoped checks pass (135 backend, 10 vitest, pre-commit hooks).

  Left alone, your call:
  - Two properties with the same display name now give identical rows (the slug
    was unique). Possible when a GAP-190 archived stub shares a villa's name.
    Fix would be showing the slug as secondary text.
  - The row dict and the label logic are each duplicated between contacts and
    companies. Kept as is (small, and companies may not import contacts).
  - Dead `getattr(a.property, "slug", None)` guard in `accounts/views/contact.py`
    (the FK is non-nullable); not touched.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: supplier property assignments shows property as slug, not name
updated: 2026-11-12 10:41:35.941171
waiting_on: null
waiting_since: null
working_on: false
---