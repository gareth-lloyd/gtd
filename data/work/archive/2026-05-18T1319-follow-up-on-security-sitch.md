---
area: null
contexts: []
created: 2026-05-18 13:19:53.873028
defer_until: null
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
  rather\nthan solving it inside this incident.\n---\n\n## Agent run 2026-05-18T14:40
  (read-only prod shell investigation)\n\nRan account + event + auth-trail queries
  against prod (read-only). This is\nNOT just nuisance calls -- it is a confirmed,
  partially-successful intrusion.\n\nCONFIRMED FINDINGS:\n- ihg_donyandrian-8nc6 (user
  4114319, email crownpsb@accountant.com) is the\n  severe one. Attacker-controlled
  free-mail address provisioned in IHG\n  Production SSO and asserted by IHG as SYDRB:property_admin.
  Confirmed\n  successful login 2026-05-13 21:53:23, then MODIFIED a guest chat thread\n
  \ (chat.Thread__updated 21:53:37) and browsed the property over ~18h\n  (sessions
  through 2026-05-14 15:51). STILL ACTIVE in Canary because IHG\n  SSO keeps asserting
  it -- cannot be fixed in Canary, IHG must deprovision.\n- doniandria (user 4114753,
  jay.bake234@aol.com): one successful login\n  2026-05-14 15:53, viewed hotel once,
  no recorded writes. Now deactivated.\n- ihg_donyandrian (user 4113891, LEGIT email):
  logins 2026-05-13 (creation)\n  and 2026-05-15 14:23, activity to 19:54 -- inside
  the active abuse window.\n  Real-Dony-vs-attacker can only be told from login IPs
  (UserLoginDetails);\n  IP query queued, awaiting output.\n\nESCALATION PRIORITY
  (unchanged owner = you to drive):\n1. URGENT: get IHG to deprovision crownpsb@accountant.com
  from their IdP for\n   SYDRB. Until then the attacker retains property_admin on
  a live hotel.\n2. Treat as a security incident with data interaction (guest chat
  modified),\n   not a support nuisance. Notify whoever owns incident response.\n3.
  Pull login IPs to confirm scope of the legit-account session and to get\n   attacker
  source IPs for blocklisting; invalidate any KnownDeviceToken.\n\nNOTHING posted
  to Linear or any external service -- investigation only.\n"
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Follow up on security sitch
updated: 2026-05-22 14:41:39.909081
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6244/bad-actor-attempting-to-gain-access