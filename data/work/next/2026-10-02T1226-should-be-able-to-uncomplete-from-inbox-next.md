---
area: null
completed_at: null
contexts: []
created: 2026-10-02 12:26:03.934021
defer_until: null
due: null
energy: low
id: 2026-10-02T1226-should-be-able-to-uncomplete-from-inbox-next
order: -1
output: |-
  ## Agent run 2026-10-19T14:35:24

  Done, and the bonus works too. Commit 78f752b6 on main (code only, no data). Service restarted.

  **Cause:** when you click done during inbox processing, the row greys out and gets marked "processed", and every button on a processed row is locked. That included `↺ uncomplete`, which the detail pane shows once it refetches the item as archived.

  **Fix** (frontend/src/WorkflowActions.tsx, ProcessedItemsContext.tsx):
  - Processed items now remember which bucket they were moved to.
  - A row marked done in this inbox session shows the archive buttons with `↺ uncomplete` enabled. → reference and Delete stay locked.
  - Uncomplete moves the item back to **inbox**, un-greys the row, and refreshes it in place. The other greyed rows stay where they are.
  - Bonus, outside inbox processing (archive view, search): uncomplete now sends items with no project to **inbox** and items with a project to **next**. Before, everything went to next. The button tooltip says where the item will go.

  **Tests:** 5 new vitest cases in WorkflowActions.test.tsx. All 193 frontend tests, all 695 pytest tests, lint.sh and the build pass. I haven't clicked through it in the browser.

  **Not done (your call):** other processed rows (moved to next/waiting/someday or deleted) are still locked. Now that the outcome bucket is tracked, a general "↺ back to inbox" undo for them would be a small follow-up.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: should be able to uncomplete from inbox/next
updated: 2026-10-19 14:35:24.271220
waiting_on: null
waiting_since: null
working_on: false
---

Currently, after "done" the greyed out item's "uncomplete" is disabled. 

Not sure if it's possible, but bonus would be to put inbox items back to inbox instead of "next" with no project selected