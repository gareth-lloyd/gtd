---
area: null
completed_at: null
contexts:
- react
created: 2026-08-13 21:12:20.198907
defer_until: null
due: null
energy: medium
id: 2026-08-13T2112-check-whether-any-questions-in-this-doc-need-my-re
order: null
output: "## Agent run 2026-08-13T22:05Z\n\nDoc: \U0001F510 Different levels of Support
  Access Grant\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07\n\n5 open
  comment threads, all unresolved. All 5 opened by **Stephanie Barry**\n(sbarry@);
  one reply from **Laura DeWald** (ldewald@) today. Nothing from\nanyone else. Verdict:
  **2 need your response, 2 are stale and can just be\nresolved, 1 needs nothing.**\n\n###
  Needs your response\n\n**1. \"Who approves a check-in configuration grant?\" — Steph,
  2026-08-07**\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b5814686151808f9aa0001c417269ab&pvs=42#320bfa505c2049b49fdf446ceb3da951\n>
  \"what dimension do we need available to define who can approve and who\n> notifications
  get routed to? Currently use `segment` set → primary for that\n> CS segment. Choices
  are `smb`, `mm`, `apac`, `tech_ops_messaging`\"\n> (+ link to https://www.canarytechnologies.com/canary-admin/internal_support/supportaccessapprover/)\n\nThis
  is the one real question aimed at you. Your doc raises it back as an open\nsystem-level
  question (\"Which dimension governs approver routing?\") but never\nanswers it,
  so the thread is still live.\n\nWorth knowing before you reply — Steph is describing
  the admin UI as if segment\nrouting works today, and it does not. I checked the
  code:\n- `internal_support/services/hotel_segments.py:4` — `get_hotel_segment()`
  is a\n  Phase-3a stub with a hardcoded `return None`. Docstring defers the real
  source\n  (Salesforce / CS-org table / portfolio metadata) to a follow-up, referencing\n
  \ the TOOL-205 PR.\n- `support_access_grant_slack.py:248` `_compute_authorized_approver_emails()`\n
  \ calls it, gets `None`, logs\n  `internal_support.support_access_grant.segment_routing_fallback`,
  and returns\n  the **full backup-approver list** every single time.\n- `models/support_access_approver.py:19-23`
  does carry exactly the four segment\n  choices Steph names, and the DB constraint
  enforces one active primary per\n  segment — so the admin page looks functional
  and rows can be configured, but\n  nothing ever matches.\n\nSo the honest answer:
  segment is configurable on the approver side, inert on the\nhotel side. Any per-segment
  routing Steph has set up in that admin is currently\na no-op. That reframes her
  question — the choice isn't just \"which dimension\",\nit's \"do we finish segment
  (TOOL-284 / TOOL-205), lean on enterprise portfolio\n(TOOL-498), or route by grant
  type\". Your doc already recommends answering this\nonce for the system rather than
  adding a fourth dimension; the missing piece is\ntelling Steph the current state
  is a silent fallback.\n\n**2. \"Grant types\" — Steph, 2026-08-07**\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b5814686151805fa7b5001cd822f86d&pvs=42#77a4a12d7e42447d92031545bf5bc954\n>
  \"we've also mentioned auto creating requests when there is an expansion\n> opportunity.
  Having a type could make this more robust so we just auto-grant\n> the permission
  for the type needed for the expansion\"\n\nNot a question, but it's the only comment
  whose content is **not** reflected\nanywhere in the current doc body. Auto-*approval*
  is covered (the dial you'd\nbuild and leave off); auto-*creation* of a grant triggered
  by an expansion\nopportunity is a different thing — a system-initiated grant with
  no human\nrequester, which collides directly with your requester-binding design\n(`requested_by`
  compared against the acting staff user). Worth either a short\nreply or a line in
  the doc saying it's out of scope for v1.\n\n### Stale — already absorbed into the
  doc, safe to resolve\n\n**3. Linear ticket requirement** — Steph, 2026-08-07, on
  \"Approval varies by type\"\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b58146861518038b9e4001c32fc5654&pvs=42#95d45c1df035403691324248ff0f3a6d\nHer
  point (CS config requests have no natural ticket, would create one just to\nsatisfy
  the gate) is now verbatim in Product decisions as \"Does this type still\nrequire
  a Linear ticket? (TOOL-365)\". Answered by the doc.\n\n**4. Requester binding**
  — Steph, 2026-08-07\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3b581468615180fbabc9001cf2f365b7&pvs=42#3d70ea9f500a495b85e587ef7456ad80\n>
  \"I think we should do this. If more than one person needs access they should\n>
  put in their own request\"\nNow the stated working position in the doc (\"yes —
  if a second person needs\naccess they file their own request\"). Agreed, nothing
  owed.\n\n### No response needed\n\n**5. \"Breaking out the work (Steph)\"** — Steph
  2026-08-12, tagging Laura + you;\nLaura replied \"makes sense to me!\" on 2026-08-13.\nhttps://app.notion.com/p/3b48146861518198ac27c246cb4baf07?d=3ba8146861518078b983001c9bc86483&pvs=42#bf5fce7cc6384fecb2cdf1a8fc52a874\nGreen
  light rather than a question: both stakeholders now agree the eng track\ncan start
  ahead of the product answers.\n\n### One thing nobody has picked up\n\nThe doc flags
  exactly one item as blocking the build — \"What can the check-in\nconfiguration
  type actually do?\" — and explicitly says it needs whoever is\nbuilding the Check-in
  V3 flow builder, **not** the CS org. Steph and Laura are\nboth CS-side, so neither
  of them is going to answer it, and nobody is tagged on\nit. That's the item most
  likely to stall this, and routing it is probably yours.\n\n### Note on attribution\n\nSteph's
  2026-08-12 comment says she broke out the eng-vs-product split, and the\nheading
  is \"Breaking out the work (Steph)\" — but that section contains\nfile-level corrections
  to Appendix A (`assignable_roles.py`,\n`list_create_roles.py`, the `ends_at` rebuttal).
  Flagging in case the section\nisn't actually hers and the heading needs fixing before
  this circulates wider.\n\nNo writes made to Notion — read-only, per session rules.
  Drafts above are for\nyou to send or discard.\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: Check whether any comments in this doc need my response. Draft unambiguous
  responses or flag for my input
updated: 2026-08-14 07:10:21.090590
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Different-levels-of-Support-Access-Grant-3b48146861518198ac27c246cb4baf07?source=copy_link