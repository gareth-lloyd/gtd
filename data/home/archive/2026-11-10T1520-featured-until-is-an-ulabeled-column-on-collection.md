---
area: null
completed_at: 2026-11-12 10:41:23.291052
contexts: []
created: 2026-11-10 15:20:15.436076
defer_until: null
due: null
energy: low
id: 2026-11-10T1520-featured-until-is-an-ulabeled-column-on-collection
order: 1
output: |
  ## Agent run 2026-11-12T09:50

  Fixed in a worktree, NOT committed (waiting for your go-ahead).

  Cause: on the collection detail page each villa row has a bare date input
  whose only label was an aria-label ("Featured until for <villa>"), so
  nothing on screen said what the date was. The description input beside it
  at least has a placeholder.

  Change: each row now shows a small muted "Featured until" caption to the
  left of the date input. The per-villa aria-label is unchanged.

  - Worktree: /Users/garethlloyd/projects/villacollective/.claude/worktrees/collection-featured-until-label
  - Branch: fix/collection-featured-until-label (off main 0e414d57)
  - Files (all under frontend/src):
    - features/collections/components/MemberRow.tsx (caption + wrapping label)
    - features/collections/__tests__/CollectionDetailPage.test.tsx (new assertion, seen failing first)
    - i18n/locales/en/collections.json (members.featured_until_caption)
    - i18n/locales/el/collections.json ("Προβεβλημένη έως", machine translated)
    - i18n/locales/el/_machine_translated.json (manifest entry)

  Checked: vitest for src/features/collections, src/i18n and src/test
  (236 passed), eslint, prettier and tsc clean.
  Not checked: the full frontend suite, and I did not look at it in a browser.

  Design call for you: I captioned every row rather than adding one column
  header, because the rows wrap (flex-wrap) and a header would not line up on
  narrow widths. If you would rather have a single header row, say so.

  Next step if you are happy: commit on the branch and ff-merge to main.

  ## Agent run 2026-11-12T10:05

  You chose a header instead ("site is designed to be used at high res"), so
  the per-row caption is gone. Same worktree and branch, still NOT committed.

  Now: one header row above the villa list with three captions, Villa /
  Description / Featured until, each sitting over its column.

  - MemberRow.tsx: new MemberRowHeader that repeats the row's boxes so the
    captions line up; the remove button got a fixed width (w-8) for the same
    reason. Per-villa aria-labels unchanged.
  - MembersList.tsx: renders the header above the list (not in the empty state).
  - i18n: members.column_villa / column_description / column_featured_until
    in en and el (Greek machine translated: Βίλα / Περιγραφή / Προβεβλημένη έως).
  - Test asserts the three header captions.

  Checked: vitest for src/features/collections, src/i18n, src/test (236
  passed), eslint, prettier, tsc clean.
  Not checked: the full frontend suite, and not viewed in a browser, so the
  column alignment and the header-to-list spacing are unverified by eye.
  Below the width where rows wrap, the captions will not line up.

  ## Agent run 2026-11-12T10:20

  You ran /code-review on the header change; it raised 7 findings, the main
  one being that the header's negative margin probably let the first row
  paint over the captions. Reworked, same worktree and branch, NOT committed.

  - Header and rows now share one CSS grid column template (MEMBER_GRID in
    MemberRow.tsx: handle / villa / description 16rem / date 10rem / remove),
    so captions align by construction, not by two hand-matched layouts.
  - Rows no longer wrap at narrow widths (they were flex-wrap). Follows from
    your high-res call; the villa column shrinks to 10rem and no further.
  - Negative margin removed; header and list sit in their own space-y-1 wrapper.
  - Header is aria-hidden: each input already has a label naming its villa.
  - Test now asserts the captions exist and says plainly that jsdom cannot
    prove layout.

  Checked: vitest for src/features/collections and src/test (149 passed),
  eslint, prettier, tsc clean.
  Not checked: full frontend suite; still not viewed in a browser, and
  drag-to-reorder was not tried by hand after the row layout change.

  ## Agent run 2026-11-12T10:40

  Merged to main at your request: commit 9b2317b0 "fix(collections): caption
  the villa list columns on collection detail". Local only, NOT pushed.

  - Main had gained two commits, so the fast-forward was refused; I
    cherry-picked the commit onto main instead (no overlap with those commits).
  - Worktree removed, branch fix/collection-featured-until-label deleted.
  - Full frontend suite passed before the commit (383 files, 4785 tests);
    after landing on main, tsc and the collections tests (56) pass.
  - Still not viewed in a browser; drag-to-reorder not tried by hand.
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: featured until is an ulabeled column on collection detail
updated: 2026-11-12 10:41:23.291024
waiting_on: null
waiting_since: null
working_on: false
---