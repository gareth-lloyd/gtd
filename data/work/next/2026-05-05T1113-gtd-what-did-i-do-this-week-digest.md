---
area: engineering
contexts:
- deep
- fun
created: &id001 2026-05-05 11:13:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1113-gtd-what-did-i-do-this-week-digest
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- creative
- skills
time_minutes: 90
title: 'GTD: what did I do this week digest'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** No structured way to look back at a week of work.
`/prep-self-review` exists but pulls from Linear/GitHub/Slack and
ignores the GTD signal. End-of-week reflection is manual and
ad-hoc.

**Approach.**
- New skill `.claude/skills/gtd-digest.md` that produces a
  structured weekly summary:
  - Items completed (`archive/` filtered by `updated >= today-7d`)
  - Projects advanced (project_ids appearing in completed items)
  - Contexts/energy distribution (where did time go?)
  - Items added (`created >= today-7d`)
  - Snapshots committed in the period (from `git log -- data/`)
- Output as markdown. Optionally write to `data/<env>/digests/` (new
  dir; user decides whether to gitignore or commit).
- Make it composable: `/prep-self-review` can include the GTD
  digest as a section.
- Voice: factual, terse. Numbers + a few standout completed items.
  No fluff.

**Verification.** Run `/gtd-digest` against current data; spot-check
counts vs manual `ls archive/ | grep '2026-04-' | wc -l`.

**Size.** S-M (~90 min)