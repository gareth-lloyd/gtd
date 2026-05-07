---
area: null
contexts:
- consume
created: 2026-05-07 11:29:44.793532
defer_until: null
due: null
energy: low
id: 2026-05-07T1129-read-stephen-reddekopp-s-on-production-canary-admi
order: null
output: '## Agent run 2026-05-07T13:45:00Z


  TL;DR — Stephen''s "on production canary admin" turned into incident #236 (no healthy
  upstream, HIGH, complete outage, internal-only). Mitigated in 17 min by bumping
  django-admin memory. Root-caused, fix PR up.


  ### Timeline (2026-05-06, EEST)

  - 19:06 — Stephen posts screenshot of error on US canary-admin in #eng-general.
  Was on an external call so context arrived late.

  - 19:07–19:10 — Z, Kevin, Aditya can''t repro; Stephen says it''s working again.
  Aditya checks pod count, notes synthetics didn''t fire.

  - 19:10 — Kevin sees it go down again; Aditya: "django admin is separate now from
  main django… I think a pod sweep occurred."

  - 19:13 — Ishwar: crashloop alert fires.

  - 19:14 — Z: "start incident". Aditya confirms OOMs.

  - 19:15 — Incident #236 opened (Kevin oncall, Andrea IC).

  - 19:32 — Marked mitigated by Aditya — fix was bumping django-admin memory.

  - 19:36 — James M identifies the offending page: `/canary-admin/message_scheduler/messagejourneytraceentry/`
  (don''t click — OOMs).

  - 19:40 — James M: resolving for now, internal-only, no customer impact.

  - 20:15 — James M posts root cause.

  - 00:03 next day — Justin Ligman opens fix PR #44874.


  ### Root cause

  Earlier-in-day migration added table partitioning to `message_scheduler_messagejourneytraceentry`.
  Django admin uses `AccurateAdminPaginator`, which estimates row counts via `pg_class.reltuples`.
  After partitioning, the parent table''s reltuples returns -1 (rows live in partition
  leaves, not the parent), so the paginator went haywire and the page OOM''d the pod.


  ### Fix

  PR https://github.com/canary-technologies-corp/canary/pull/44874 — Justin replaced
  the simple `pg_class` lookup with a recursive CTE that walks `pg_inherits` and sums
  `GREATEST(reltuples, 0)` across only leaf (`relkind=''r''`) tables. Justin flagged
  it''s not his area; worth a glance from anyone who owns admin paginator code.


  ### What stood out

  1. **canary-admin is now its own deployment**, separate from main django. Stephen''s
  read at the end of the thread: this likely saved canary itself — main django has
  more memory headroom and could have absorbed the hit, but the smaller canary-admin
  pods OOM''d first and contained the blast radius. Aditya partially agreed.

  2. **Gap: no synthetics on canary-admin yet.** Aditya called this out at 19:26 —
  synthetics fire on main django so initial signal was "looks fine here." Action item
  from the incident.

  3. **Partitioning has a sneaky admin-side blast radius.** Anywhere admin uses `AccurateAdminPaginator`
  (or anything else reading `pg_class.reltuples` directly) is at risk when we partition
  more tables. PR 44874 is the canonical fix — worth confirming it landed and that
  there are no other reltuples readers.

  4. **Process note:** initial post had thin context ("on production canary admin"
  + tiny screenshot). Z pushed back appropriately ("more context is needed", "screenshot
  is too small"). Stephen apologized later — he was gathering data on an external
  call. A one-liner like "US canary-admin returning errors, gathering details" up
  front would have saved a few minutes of triage churn.


  ### Open questions / followups (not started)

  - Did PR #44874 merge? Worth checking before any future partitioning work.

  - Was the canary-admin synthetic added?

  - Retro doc would live in `#incident-20260506-no-healthy-upstream`.


  Done. Returning control.

  '
project: null
source_id: https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1778083605808159?thread_ts=1778083605.808159&cid=C019TQLQDJP
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: Stephen Reddekopp''s ''on production canary admin'' thread'
updated: 2026-05-07 13:54:47.674716
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from awareness. 27-reply thread in #eng-general worth catching up on.
https://canarytechnologies.slack.com/archives/C019TQLQDJP/p1778083605808159?thread_ts=1778083605.808159&cid=C019TQLQDJP