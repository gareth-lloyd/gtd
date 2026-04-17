- problem of non-sequential projects dumping all items into "next"
- Defer by hours
- Scheduled UI

  Considered and rejected
  1. Add max_active alongside sequential — keeps both fields. Rejected because they're the same axis ("how many items to surface") and the interaction is
     confusing: what does sequential: true, max_active: 3 mean?

  2. UI-only collapsing — group items by project in the frontend, collapse after N with "show 4 more". No backend change. Rejected because it doesn't actually
     reduce cognitive load — the items are still "active", just hidden behind a click. The GTD principle is that the list itself should be clean.

  3. Hybrid (both fields + UI collapsing) — dismissed as over-engineering.

  Approaches not considered
  4. Auto-throttle by project priority — no new field at all. Use existing priority to derive a slot count: P1 gets 5 items, P2 gets 3, P3 gets 2, P4-5 gets 1,
     no-priority gets 1. Zero configuration needed. Downside: the mapping is arbitrary and not tuneable per-project.

  5. Global default in config.yml — add e.g. default_max_active: 3 to the env config. Every non-sequential project shows at most 3 unless overridden per-project.
     Solves the HOME problem (198 items, 0 configuration) with a single line of config. Could combine with the per-project max_active field.

  6. Focus/starred items — add a boolean starred or focus flag on items. The next view defaults to showing only starred items (with a toggle to show all).
     Completely orthogonal to projects — you curate a daily short list. Downside: requires manual curation every day.

  7. Two-tier next: "ready" vs "planned" — split next into two sub-statuses. Items start as "planned" when assigned to a project; you explicitly promote to
     "ready" the ones you'll actually do. Only "ready" shows by default. Downside: adds friction to every item, and it's basically a manual version of max_active.

  8. WIP limit on the view itself — cap total visible items at e.g. 20, sorted by priority/due. No per-project logic, just a hard ceiling. Simple, but blunt —
     could hide urgent items from low-priority projects entirely.

  9. Defer-based throttling (no new fields) — use existing defer_until to stagger items within a project. Set all but the first 3 to defer_until: next week. No
     code changes, just a workflow convention. Downside: manual, and deferred items disappear completely rather than being "hidden but acknowledged."

  10. Kanban auto-promotion — items live in someday until capacity opens in next. When you complete something, the system auto-promotes the next highest-priority
      item. Downside: significant complexity, and fights the GTD model where you decide what's next.

  ***

  The ones I find most interesting beyond the current plan:
  - #5 (global default) pairs well with per-project max_active — it solves the "198 items, zero config" problem immediately without touching every project
  - #4 (priority-derived) is appealing as a zero-config starting point but feels too magic
  - #6 (starred/focus) solves a different but related problem — even with max_active, you might still have 60 items in next and want a "today" shortlist

  Any of these change your thinking, or should I refine the max_active plan?
