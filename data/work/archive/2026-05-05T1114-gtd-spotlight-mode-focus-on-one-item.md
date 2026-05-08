---
area: engineering
contexts:
- deep
- fun
created: 2026-05-05 11:14:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1114-gtd-spotlight-mode-focus-on-one-item
order: 0
output: ''
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- frontend
- creative
time_minutes: 90
title: 'GTD: spotlight mode (focus on one item)'
updated: 2026-05-07 15:21:43.109207
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** The next-actions list is a wall of cards. When you tab
back to the tool after context-switching, the noise pulls attention
away from the one thing you've decided to focus on right now.
There's no UI mode that says "this is what we're doing, ignore
everything else." A spotlight reminder when refocusing on the tool
would be a useful nudge.

**Approach.**
- Add a "spotlight" affordance on the right side of each `ItemCard`
  (`frontend/src/ItemCard.tsx`) — a small icon button alongside the
  existing chips. Tooltip: "Focus on this item".
- Clicking spotlights the item: hide the rest of the list, show
  only this card centered and expanded. Title + body prominent.
  Detail pane collapses or merges into the spotlit view.
- State persistence: store the spotlit item id in the URL query
  param `?spotlight=<id>` (URL-driven UI state matches the
  existing pattern in `frontend/src/filters.ts`). When you tab
  back to the tool the spotlight is automatically restored.
  Bonus: change `document.title` to the item title so the browser
  tab itself reminds you what you're meant to be doing.
- **Exit is supposed to be cheap, not gated.** Bind `Escape` to
  exit, plus a small unobtrusive "exit spotlight" affordance
  (corner X). Navigating to a different bucket / project / view
  also exits implicitly. No confirm dialog. The whole point of
  spotlight is that the cost of exiting must be low — friction
  here would defeat the purpose.
- Composes with `working_on`: if an item already has
  `working_on=true`, surface a "Spotlight working item" entry-point
  in the header so you can drop into focus mode in one click.
- A11y: `aria-label="Focus on this item"`, focus management on
  enter/exit, focus returns to triggering card on exit.

**Verification.**
- Component test: clicking the affordance updates URL and hides
  other items.
- E2E spec: spotlight an item, navigate away, return — spotlight
  state restored from URL; document.title updated.
- Manual: spotlight an item, tab to email for 10 min, tab back to
  GTD, confirm only that item is visible and the browser tab
  shows its title.

**Size.** S-M (~90 min)