---
area: null
contexts: []
created: 2026-05-18 13:19:53.873028
defer_until: 2026-05-18 15:19:00
due: null
energy: low
id: 2026-05-18T1319-follow-up-on-security-sitch
order: -18
output: "## Agent run 2026-05-18T13:30 (research only — nothing posted to Linear)\n\nENT-6244
  \"Bad actor attempting to gain access\" — status: still **Triage**,\nlast comment
  2026-05-15, SLA **breached 2026-05-17**. Needs your attention.\n\n### Situation\nRepeat
  social-engineering caller (numbers +1 646-389-3416 and +1 417-712-6597)\nhas made
  20+ Support calls impersonating IHG / Crowne Plaza Sydney Burwood\nadmins (Dony
  Andrian, Dewi Meliala, Greg Nawrocki). Once tried to redirect\nGreg Nawrocki's email
  to \"LinChris\". Real Dony Andrian confirmed by email he\nnever contacted Support
  and asked us to investigate.\n\n### Actions already taken (Support / Lautaro)\n-
  `doniandria` (user 4114753) — deactivated.\n- `ihg_donyandrian-8nc6` (4114319) —
  could NOT deactivate; valid IHG Prod SSO\n  account. Property must ask IHG to deactivate
  upstream, then tell us.\n- `ihg_donyandrian` (4113891) — legitimate, untouched.\n\n###
  Outstanding asks aimed at you (@glloyd)\n1. Lautaro: \"@glloyd @connor @andrea any
  other ideas here?\" — preventing\n   impersonation + flagging accounts so CS is
  more vigilant.\n2. Lautaro: \"@glloyd @sbarry this is another issue where we are
  blind if a\n   user gets deactivated on the customer identity provider.\" — recurring
  IdP\n   deactivation visibility gap.\n3. Nensy (routed to @zlee @bpietraga, unanswered):
  can we investigate whether\n   any logins/actions occurred through the potentially
  compromised accounts?\n\n### Recommended next steps (your call)\n- Answer #3 first
  — it's the concrete security question. Decide whether you /\n  zlee / bpietraga
  pull Datadog auth logs for users 4113891 / 4114319 /\n  4114753 to confirm no successful
  bad-actor logins or data access. This is\n  the highest-value action and is currently
  unowned in practice.\n- On #1: process control, not eng. Suggest CS adds a watch/flag
  note on the\n  Crowne Plaza Sydney Burwood property + named users so any future\n
  \ access/email-change request is escalated, not actioned.\n- On #2 (IdP deactivation
  blindness): this is a known recurring gap worth a\n  separate tracked ticket rather
  than re-litigating in this incident thread.\n- Move out of Triage and assign an
  owner — SLA already breached.\n\n### Draft reply (NOT posted — for your review/approval)\n---\nA
  few thoughts:\n\n1. Login/action investigation (answering Nensy's question): we
  should pull\nauth logs for the three accounts (ihg_donyandrian 4113891,\nihg_donyandrian-8nc6
  4114319, doniandria 4114753) to confirm whether any\nsuccessful logins or actions
  occurred from the bad actor before deactivation.\n@zlee @bpietraga — can one of
  you own that pull? Happy to pair.\n\n2. Preventing impersonation is fundamentally
  a CS process control, not\nsomething we can block in product. Recommend flagging
  the Crowne Plaza Sydney\nBurwood property and the named users so any future access
  / email-change\nrequest is escalated to a known-good verification path rather than
  actioned.\n\n3. The \"blind when a user is deactivated on the customer IdP\" problem
  is real\nand recurring — I'll spin up a separate ticket so we track it properly
  rather\nthan solving it inside this incident.\n---\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Follow up on security sitch
updated: 2026-05-18 14:19:39.996790
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6244/bad-actor-attempting-to-gain-access