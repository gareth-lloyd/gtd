---
area: null
completed_at: null
contexts: []
created: 2026-10-14 17:41:13.519562
defer_until: null
due: null
energy: low
id: 2026-10-14T1741-i-need-to-be-able-grab-multiple-items-and-put-them
order: null
output: |
  ## Agent run 2026-10-14T17:47:19

  Implemented grab bags end to end. Committed to main as 6e6ddc50 (code only, no data). Frontend rebuilt and service restarted (`make restart-service`). Live `GET /api/envs/work/grab-bags/` returns 200.

  **What you get**
  - **✋ grab** button on every item: active buckets, archive and trash, in both the card and the detail pane. It opens a dialog that lists every existing bag as a button (one click adds the item). Below that is a "New grab bag name…" field; pressing Enter creates the bag with this item already in it.
  - **Side nav**: "grab bags" sits right under projects, with the 3 most recently touched bags as sub-links. Clicking "grab bags" opens `/<env>/grab-bags`, a list of every bag with its item count and age.
  - **Bag view** (`/<env>/grab-bags/<id>`): the normal three-column layout (nav, item list, detail panel). It shows the name, "created Xh ago" and the item count. The items use the usual ItemCards, so they're editable and j/k works. There is one action, **Empty**: after a confirm it deletes the bag. The items are not touched at all (bucket, project, `updated`, everything stays the same) and you return to the list. No history is kept.
  - **Auto-cleanup**: a bag is deleted the next time it is read once every item in it is archived, trashed or purged.

  **Design decisions to check**
  1. **Membership is stored on the bag, not the item**: `data/<env>/grabbags/<id>.md` with frontmatter `name`, `created`, `updated` and `items: [ids]`. Grabbing and emptying never write item files, so they don't bump `updated` or create snapshot noise. An item can be in several bags.
  2. **Reference is NOT terminal for cleanup.** Only archive, trash and purged count. Otherwise a bag of reference material you grabbed to read together would vanish straight away. This is a one-line change (`_GRAB_BAG_TERMINAL` in `gtd_core/service.py`) if you want it the other way.
  3. **Cleanup is lazy.** It runs when bags are listed or opened (the nav fetches the list on every page load), not on a schedule or at snapshot time.
  4. **"Most recent" means most recently grabbed into**, not most recently created (`updated` bumps on each grab). The age shown is from `created`.
  5. Completed and trashed items stay visible in the bag (greyed as usual) while at least one item is still live.
  6. A bag created with no items is not pruned. The UI can't produce one, because creating always includes the item.

  **Not done / possible follow-ups**
  - There's no way to remove a single item from a bag (the spec said Empty only).
  - No keyboard shortcut for grab.
  - No Playwright e2e spec. Coverage: 22 core tests, 8 API tests, 14 frontend tests.
  - The snapshot "unloadable files" check doesn't scan `grabbags/`.

  **Files**: `gtd_core/{models,storage,repository,service}.py`, `gtd_api/{views,serializers,urls}.py`, `frontend/src/GrabBags.tsx` (new), plus `App.tsx`, `WorkflowActions.tsx`, `ItemEdit.tsx` (cache invalidation and `findItemInCache` for bag views), `api.ts`, `format.ts` (`fmtAge`) and the CLAUDE.md docs.

  ## Agent run 2026-10-14T17:58:59

  > Change UI. Add a small "+" icon next to grab bags in left menu: only way to add one. On an item, instead of one "Grab" which opens dialog, output a new row of buttons below existing, one per grab bag: "<hand> <name>". Clicking grabs directly

  Done and committed as 2908038b. Frontend rebuilt and service restarted.
  - **Side nav**: a small **+** sits next to "grab bags". Clicking it shows an inline "Bag name…" field: Enter creates the bag, Esc cancels. This is now the only way to create a bag.
  - **Items**: the grab dialog is gone. Below the existing action buttons there is now a second row with one `✋ <name>` button per bag, and a click grabs the item straight away. If the item is already in a bag, that button shows as pressed and can't be clicked. The row is hidden when there are no bags.
  - API change: the bag list now returns `item_ids` so the row can show which bags already hold the item.
  - A bag created from the + starts empty and is never cleaned up automatically while it's empty. Remove it with Empty.
  - Tests: 695 backend and 187 frontend pass; lint is clean.
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 5
title: I need to be able grab multiple items and put them in an arbitrary, temporary,
  "grab bag" to look at them in one place.
updated: 2026-10-14 17:58:59
waiting_on: null
waiting_since: null
working_on: false
---

Feature:
* New action on any item: "Grab"
* Grab opens a simple dialog:
  * All existing Grab bags listed as buttons for easy selection
  * Obviously many bags will litter the UI, but they are intended to have short life spans and get cleaned up
  * Option to create a new grab bag, enter name only
* New entry in left menu under Projects: Grab bags
  * Most recent three shown as clickable
  * Clicking Grab bags takes you to a view of all of them
* Grab bag view:
  * Normal three column layout
  * Show age of grab bag
  * One action: "Empty". Removes the association with all items, but does not affect their project, state, or any other attribute (I.e. they are not "Done" because the bag is going away)
   * Once empty the bag is deleted. No record of historical bags. 

* Cleaned up automatically once every item in a terminal state