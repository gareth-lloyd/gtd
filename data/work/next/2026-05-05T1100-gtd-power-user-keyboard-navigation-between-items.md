---
area: engineering
contexts:
- deep
created: 2026-05-05 11:00:00
defer_until: null
due: null
energy: high
id: 2026-05-05T1100-gtd-power-user-keyboard-navigation-between-items
order: 5
output: ''
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- frontend
time_minutes: 180
title: 'GTD: tristate item card + power-user keyboard navigation'
updated: 2026-05-08 15:22:23.550452
waiting_on: null
waiting_since: null
working_on: false
---

**Scope expansion (2026-05-08).** Originally just keyboard nav. During
plan review surfaced a deeper concern: today selecting an item and
editing an item are the *same state* — `ItemCard.tsx:65-69` renders the
editor whenever `selectedId === item.id`. Walking selection with `j`/`k`
would whip every visited card into edit mode. So this PR bundles a
**tristate refactor** with the keyboard nav.

**Problem.** Two related gaps:

1. No keyboard navigation *between* items in lists; mouse-only.
2. Selection and editing are conflated. Clicking a card to highlight it
   immediately puts it into edit mode. There's no "I just want to point
   at this row" state — useful for keyboard nav, multi-select (item 8),
   and any future per-item action key (`.`, `d`, `m`).
3. Escape is broken inside capture/search inputs — never deselects.

**Approach.**

Tristate model in `SelectionContext`:

| State | Condition | Render |
|---|---|---|
| idle | not hovered, not selected | `<CollapsedCard>` |
| hovered | `hoveredId === id && selectedId !== id` | `<CollapsedCard>` + hover affordances |
| selected | `selectedId === id && editingId !== id` | `<CollapsedCard>` + focus ring |
| editing | `editingId === id` | `<SelectedInListCard>` (existing editor) |

Invariant: `editingId !== null ⇒ selectedId === editingId`.

Setters:
- `select(id)` — sets selectedId, **clears editingId**.
- `edit(id)` — sets both.
- `stopEditing()` — clears editingId, keeps selection.
- `selectNext()` / `selectPrev()` — walk `navigableIds` (registered by
  `ItemList`), clamp at ends, no wrap. Side-effect: clears editingId.

Interactions:
- Click idle card → `select(id)` (collapsed + focus ring, no editor).
- Click selected card → `edit(id)` (open editor).
- Click editing card → no-op.
- `j`/`ArrowDown`, `k`/`ArrowUp` → navigate without entering editor.
- `Enter` (selected, not in input) → `edit(selectedId)`.
- `Escape` inside the active editor → `stopEditing()` (single keystroke).
- `Escape` in any other input (capture, search) → blur, leave selection.
- `Escape` outside any input, editing → `stopEditing()`.
- `Escape` outside any input, selected → `select(null)`.
- Spotlight button click still calls `edit(id)`; URL-driven autospotlight
  uses `select(id)` only (don't force editor open).

`Cmd/Ctrl+Enter` in editor → `stopEditing()` (was `select(null)`).

Reuse existing `isEditableTarget` filter from `CaptureBar.tsx:20`. After
nav, scroll into view via `data-item-id` selector +
`scrollIntoView({ block: "nearest" })`.

**Out of scope (file as follow-ups):**
- `e` toggle, `.` toggle working_on, `d` defer picker.
- Wrap-around at list ends.
- Multi-select (item 8 covers it).

**Verification.**
- vitest `SelectionContext.test.tsx`: state machine — `select` clears
  editingId, `edit` sets both, `stopEditing` keeps selection, `selectNext`/
  `Prev` clamp.
- vitest `ItemCard.test.tsx`: editing renders editor; selected-not-editing
  renders collapsed + selected class.
- Playwright `keyboard-nav.spec.ts`: j/k/Enter/Escape + capture-Escape
  regression.
- Playwright `spotlight.spec.ts`: spotlight button still opens editor.
- Manual: load `/work/next`, walk j/k, Enter to edit, Escape ladder,
  capture-Escape doesn't lose selection.

**Size.** M (~3h).