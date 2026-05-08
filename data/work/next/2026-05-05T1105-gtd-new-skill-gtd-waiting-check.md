---
area: engineering
contexts:
- craft
created: 2026-05-05 11:05:00
defer_until: null
due: null
energy: low
id: 2026-05-05T1105-gtd-new-skill-gtd-waiting-check
order: 9
output: ''
project: 2026-04-27-gtd
source_id: null
tags:
- gtd-meta
- skills
time_minutes: 60
title: 'GTD: new skill /gtd-waiting-check'
updated: 2026-05-08 15:22:23.550452
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** Waiting items get reviewed only during the weekly
review. Mid-week check-ins on stale "waiting on someone" items
require manual triage. No standalone skill for this.

**Approach.**
- New file `.claude/skills/gtd-waiting-check.md`. Reference
  `.claude/skills/gtd-coach.md` for voice.
- Lists `waiting/` sorted by `waiting_since` ascending. (Depends on
  item #3 being done — note dependency in skill body.)
- For items >7d, offers to draft a follow-up next item with body
  template `"Follow up on <waiting_on> — first asked <waiting_since>"`.
- Walks one at a time; user can skip, follow up, archive, or move
  back to next.
- Doesn't replace the weekly review — fills the mid-week gap.

**Verification.** Manual run; check follow-up items land in `next/`
with appropriate frontmatter.

**Size.** S (~1h)