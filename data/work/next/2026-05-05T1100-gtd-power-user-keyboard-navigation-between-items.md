---
area: engineering
contexts:
- deep
created: &id001 2026-05-05 11:00:00
defer_until: null
due: null
energy: high
id: 2026-05-05T1100-gtd-power-user-keyboard-navigation-between-items
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- frontend
time_minutes: 90
title: 'GTD: power-user keyboard navigation between items'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** No keyboard navigation *between* items in lists. To move
between cards you have to mouse to each one. Power-user gap. Also a
small UX bug: Escape only deselects when focus is *outside*
capture/search — it should deselect when not in a text field, and
blur (without deselecting) when it is.

**Approach.**
- `frontend/src/SelectionContext.tsx` already owns selected/hovered
  state. Extend it with `selectNext()` / `selectPrev()` driven by the
  rendered order in `ItemList`.
- Wire a global handler in `App.tsx` (lives next to existing
  `C` / `Shift+C` / `A` shortcuts). Bind:
  - `j` / `ArrowDown` → next, `k` / `ArrowUp` → prev
  - `Enter` → expand, `Escape` → collapse (if expanded) else deselect
  - `e` → expand, `.` → toggle `working_on`, `d` → open defer picker
- Reuse the existing `isEditableTarget()` filter so shortcuts don't
  fire inside text inputs.
- Auto-scroll the selected card into view via
  `scrollIntoView({ block: "nearest" })`.
- Fix the Escape backwardness while you're in there.

**Verification.**
- New vitest covering `SelectionContext.selectNext/Prev` ordering
- Playwright spec at `frontend/e2e/keyboard-nav.spec.ts` covering
  j/k/Enter/Escape with regression for capture/search Escape
- Manual: load next-actions list, navigate with j/k, expand with
  Enter, hit `.` to toggle working_on

**Size.** S (~90 min)