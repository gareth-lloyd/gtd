# GTD Dashboard

Show a text summary of the current GTD state. Read files directly — no server needed.

## Behavior

For each environment (work, home):

1. Count files in each bucket directory:
   ```
   inbox/  next/  waiting/  someday/  reference/  projects/  archive/  trash/
   ```

2. For projects, parse frontmatter and split by status (active / on_hold / complete / dropped).

3. Flag issues:
   - **Inbox > 0**: items need processing
   - **Stale waiting**: read waiting/*.md, find items where `updated` is >7 days ago
   - **Due soon**: read next/*.md, find items where `due` is within the next 7 days
   - **Deferred activating**: read next/*.md, find items where `defer_until` is within the next 3 days

4. Decay signals — surface items that are quietly rotting:
   - **Stale next**: read next/*.md, count + list items where `updated`
     is >30 days ago. These are committed actions nobody has touched in
     a month — either do them, defer them, or drop them.
   - **Stuck inbox**: read inbox/*.md, count + list items where `created`
     is >24h ago. Inbox is supposed to be transient; anything older than
     a day is unprocessed friction.
   - **Projects with no next action**: for each `active` project, check
     whether any next/*.md item has `project: <project-id>`. List the
     titles of active projects with zero next actions — these are
     stalled and need a next step defined (or to be put on hold).
   - **Cap every surfaced list at 10 entries** (show "+N more" if
     truncated) so the dashboard stays scannable. Counts are always
     the true total; only the printed list is capped.

5. Print a compact table per environment:

```
== work ==
  inbox:      3 ⚠  (2 stuck >24h)
  next:      37     (4 stale >30d)
  waiting:    2 (1 stale >7d)
  someday:    1
  reference:  0
  projects:   5 active, 2 on hold  (1 with no next action)
  due soon:   1 item (2026-04-15)
  deferred:   0 activating this week

  stale next (>30d, oldest first):
    - 2026-03-01T0900-...  (updated 2026-03-10, 69d)
    - ... (cap 10, then "+N more")
  stuck inbox (>24h, oldest first):
    - 2026-05-15T...  (created 2026-05-15, 3d)
  projects with no next action:
    - Launch personal blog
    - ... (cap 10)

== home ==
  ...
```

6. End with action suggestions:
   - "3 items in work inbox — consider `/gtd-inbox work`"
   - "1 stale waiting item — consider following up"
   - "4 stale next actions in work — consider `/gtd-coach work`"
   - "1 active project with no next action — define a next step or put it on hold"

## Notes

- This is read-only. Do not modify any files.
- Use `ls | wc -l` for counts (fast) and only parse frontmatter for the flags.
- Keep output concise — this is a quick health check, not a full review.
