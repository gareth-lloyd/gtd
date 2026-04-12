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

4. Print a compact table per environment:

```
== work ==
  inbox:      3 ⚠
  next:      37
  waiting:    2 (1 stale >7d)
  someday:    1
  reference:  0
  projects:   5 active, 2 on hold
  due soon:   1 item (2026-04-15)
  deferred:   0 activating this week

== home ==
  ...
```

5. End with action suggestions:
   - "3 items in work inbox — consider `/gtd-inbox work`"
   - "1 stale waiting item — consider following up"

## Notes

- This is read-only. Do not modify any files.
- Use `ls | wc -l` for counts (fast) and only parse frontmatter for the flags.
- Keep output concise — this is a quick health check, not a full review.
