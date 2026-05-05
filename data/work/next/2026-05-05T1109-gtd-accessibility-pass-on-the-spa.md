---
area: engineering
contexts:
- craft
created: &id001 2026-05-05 11:09:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1109-gtd-accessibility-pass-on-the-spa
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- frontend
- a11y
time_minutes: 180
title: 'GTD: accessibility pass on the SPA'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Roughly 18 aria-* attributes across the entire frontend
codebase. Icon buttons lack labels, cards lack `aria-expanded`,
toasts aren't a live region, no skip-to-content link.

**Approach.**
- `ItemCard.tsx` — `aria-expanded={selected}` plus `role` /
  `aria-controls` linking to the body region.
- All chip toggles — consistent `role="button"` and `type="button"`;
  `aria-pressed` for selected state.
- Icon-only buttons (working_on toggle, URL link icons, move
  icons) — add `aria-label`.
- `frontend/src/toast.tsx` — wrap container in `role="status"` for
  successes, `role="alert"` (or `aria-live="assertive"`) for errors.
- `App.tsx` — add skip-to-content link as the first focusable
  element.
- `DetailPanel.tsx` — `role="complementary"` and
  `aria-label="Item details"`.
- Add `@axe-core/playwright` to e2e and assert no critical
  violations on the main views. Document any non-trivial remaining
  issues in a follow-up.

**Verification.** Axe-core passes in e2e; manual screen-reader spot
check on capture, expand, move flows.

**Size.** M (~3h)