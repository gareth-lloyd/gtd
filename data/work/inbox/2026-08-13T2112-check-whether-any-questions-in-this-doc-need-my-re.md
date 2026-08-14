---
area: null
completed_at: null
contexts: []
created: 2026-08-13 21:12:20.198907
defer_until: null
due: null
energy: low
id: 2026-08-13T2112-check-whether-any-questions-in-this-doc-need-my-re
order: null
output: |
  ## Agent run 2026-08-13T22:05Z

  Doc: 🔐 Different levels of Support Access Grant
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07

  5 open comment threads, all unresolved. All 5 opened by **Stephanie Barry**
  (sbarry@); one reply from **Laura DeWald** (ldewald@) today. Nothing from
  anyone else. Verdict: **2 need your response, 2 are stale and can just be
  resolved, 1 needs nothing.**

  ### Needs your response

  **1. "Who approves a check-in configuration grant?" — Steph, 2026-08-07**
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b5814686151808f9aa0001c417269ab&pvs=42#320bfa505c2049b49fdf446ceb3da951
  > "what dimension do we need available to define who can approve and who
  > notifications get routed to? Currently use `segment` set → primary for that
  > CS segment. Choices are `smb`, `mm`, `apac`, `tech_ops_messaging`"
  > (+ link to https://www.canarytechnologies.com/canary-admin/internal_support/supportaccessapprover/)

  This is the one real question aimed at you. Your doc raises it back as an open
  system-level question ("Which dimension governs approver routing?") but never
  answers it, so the thread is still live.

  Worth knowing before you reply — Steph is describing the admin UI as if segment
  routing works today, and it does not. I checked the code:
  - `internal_support/services/hotel_segments.py:4` — `get_hotel_segment()` is a
    Phase-3a stub with a hardcoded `return None`. Docstring defers the real source
    (Salesforce / CS-org table / portfolio metadata) to a follow-up, referencing
    the TOOL-205 PR.
  - `support_access_grant_slack.py:248` `_compute_authorized_approver_emails()`
    calls it, gets `None`, logs
    `internal_support.support_access_grant.segment_routing_fallback`, and returns
    the **full backup-approver list** every single time.
  - `models/support_access_approver.py:19-23` does carry exactly the four segment
    choices Steph names, and the DB constraint enforces one active primary per
    segment — so the admin page looks functional and rows can be configured, but
    nothing ever matches.

  So the honest answer: segment is configurable on the approver side, inert on the
  hotel side. Any per-segment routing Steph has set up in that admin is currently
  a no-op. That reframes her question — the choice isn't just "which dimension",
  it's "do we finish segment (TOOL-284 / TOOL-205), lean on enterprise portfolio
  (TOOL-498), or route by grant type". Your doc already recommends answering this
  once for the system rather than adding a fourth dimension; the missing piece is
  telling Steph the current state is a silent fallback.

  **2. "Grant types" — Steph, 2026-08-07**
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b5814686151805fa7b5001cd822f86d&pvs=42#77a4a12d7e42447d92031545bf5bc954
  > "we've also mentioned auto creating requests when there is an expansion
  > opportunity. Having a type could make this more robust so we just auto-grant
  > the permission for the type needed for the expansion"

  Not a question, but it's the only comment whose content is **not** reflected
  anywhere in the current doc body. Auto-*approval* is covered (the dial you'd
  build and leave off); auto-*creation* of a grant triggered by an expansion
  opportunity is a different thing — a system-initiated grant with no human
  requester, which collides directly with your requester-binding design
  (`requested_by` compared against the acting staff user). Worth either a short
  reply or a line in the doc saying it's out of scope for v1.

  ### Stale — already absorbed into the doc, safe to resolve

  **3. Linear ticket requirement** — Steph, 2026-08-07, on "Approval varies by type"
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b58146861518038b9e4001c32fc5654&pvs=42#95d45c1df035403691324248ff0f3a6d
  Her point (CS config requests have no natural ticket, would create one just to
  satisfy the gate) is now verbatim in Product decisions as "Does this type still
  require a Linear ticket? (TOOL-365)". Answered by the doc.

  **4. Requester binding** — Steph, 2026-08-07
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b581468615180fbabc9001cf2f365b7&pvs=42#3d70ea9f500a495b85e587ef7456ad80
  > "I think we should do this. If more than one person needs access they should
  > put in their own request"
  Now the stated working position in the doc ("yes — if a second person needs
  access they file their own request"). Agreed, nothing owed.

  ### No response needed

  **5. "Breaking out the work (Steph)"** — Steph 2026-08-12, tagging Laura + you;
  Laura replied "makes sense to me!" on 2026-08-13.
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3ba8146861518078b983001c9bc86483&pvs=42#bf5fce7cc6384fecb2cdf1a8fc52a874
  Green light rather than a question: both stakeholders now agree the eng track
  can start ahead of the product answers.

  ### One thing nobody has picked up

  The doc flags exactly one item as blocking the build — "What can the check-in
  configuration type actually do?" — and explicitly says it needs whoever is
  building the Check-in V3 flow builder, **not** the CS org. Steph and Laura are
  both CS-side, so neither of them is going to answer it, and nobody is tagged on
  it. That's the item most likely to stall this, and routing it is probably yours.

  ### Note on attribution

  Steph's 2026-08-12 comment says she broke out the eng-vs-product split, and the
  heading is "Breaking out the work (Steph)" — but that section contains
  file-level corrections to Appendix A (`assignable_roles.py`,
  `list_create_roles.py`, the `ends_at` rebuttal). Flagging in case the section
  isn't actually hers and the heading needs fixing before this circulates wider.

  No writes made to Notion — read-only, per session rules. Drafts above are for
  you to send or discard.
project: null
source_id: null
tags: []
time_minutes: 5
title: check whether any questions in this doc need my response
updated: 2026-08-13 22:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Different-levels-of-Support-Access-Grant-3b48146861518198ac27c246cb4baf07?source=copy_link