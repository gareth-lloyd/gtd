---
area: null
contexts:
- react
created: 2026-05-15 07:28:44.720159
defer_until: null
due: null
energy: medium
id: 2026-05-15T0728-review-ent-6245-investigation-backfill-plan-ryan
order: null
output: "## Agent run 2026-05-15T11:05Z — Review of ENT-6245 investigation + backfill
  plan\n\n### What Ryan posted\nENT-6245 (\"Investigate missing user roles in portfolio
  group\") is now **Canceled**,\nsuperseded by follow-ups. Ryan's investigation comment
  identified two real, separate bugs:\n\n1. **Hotel-add doesn't grant access to existing
  portfolio members.** Adding a hotel to a\n   portfolio only auto-grants to users
  who already hold a \"covers all hotels\" portfolio-wide\n   role. Everyone else
  (e.g. members set up for a manual hotel subset) is silently skipped.\n   This is
  why Alyssa Lewter / Mark F. are \"in the portfolio but missing the hotel\" —\n   thousands
  of Wyndham hotels added since their manual setup never linked to them.\n2. **Portfolio
  user form allows saving a user with zero roles.** No validation requires at\n   least
  one role grant. Explains Natalya's \"how do they get saved with no role\" question.\n\nPlan:
  (a) one-time backfill of missing hotel access, (b) code fix to grant on hotel-add
  to\nall members, (c) code fix to require >=1 role on save. \"Will follow up with
  audit list + backfill plan.\"\n\n### Assessment — the investigation diagnosis is
  sound. Three gaps to flag:\n\n**GAP 1 (highest concern): the durable code fix for
  bug #1 is not tracked anywhere.**\nConnor's comment on ENT-6165 says he \"fixed
  #1\" — but that was a *manual emergency grant*:\nhe gave Mark + Alyssa portfolio-wide
  Property Manager access to ALL hotels in Mark Frentz's\nPortfolio OR the InterMountain
  Management Portfolio. He explicitly flagged it as an\nover-grant: \"possible/likely
  we've given them permission to properties they should not have\naccess to... we
  should look to remove these ASAP\" and asked for a definitive IMM property\nlist.
  So bug #1's systemic code fix (grant-on-hotel-add to every member) has NO open ticket.\nENT-6247
  only covers bug #2 (form validation). ENT-6243 is the duplicate-user cleanup. This\nrecurrence-prevention
  change is at risk of falling through the cracks — it needs its own ticket.\n\n**GAP
  2: the emergency mitigation is an active least-privilege risk and is time-sensitive.**\nMark/Alyssa
  currently hold portfolio-wide access to potentially-incorrect property sets.\nThis
  must be reconciled against a definitive IMM portfolio property list and tightened\n(\"ASAP\"
  per Connor). The definitive-list ask is parked on Connor's ENT-6165 comment to\nRachel
  Smoller — no owner/ticket for the tighten-down step yet.\n\n**GAP 3: Ryan's promised
  audit list + backfill plan has not been posted.**\nNo later comments on ENT-6245
  (issue cancelled same day). Scope is potentially large —\n\"thousands of hotels\",
  \"likely affects others in Wyndham and other large portfolios\".\nThe wider backfill
  is unscoped and unowned. Worth chasing Ryan for the audit before\nassuming Mark/Alyssa
  were the only affected users.\n\n### Note on ENT-6247 (the one ticket that exists,
  Triage / Medium, branch glloyd/...)\nSpec quality is good (clear where: portfolios/views/portfolio_users.py\nPortfolioUserRequestSchema.validate_object
  ~line 112; clear fix; clear AC). One caveat:\nit explicitly scopes OUT \"SSO/JIT
  provisioning paths that bypass this form.\" For IMM/Wyndham\nthese users may well
  have been provisioned via SSO/JIT, not the form — in which case ENT-6247\nwill NOT
  prevent recurrence for the actual affected cohort. Confirm the provisioning vector\nfor
  the affected users before treating ENT-6247 as the recurrence fix.\n\n### Recommended
  next actions (for user to decide — no external writes made)\n- Create/locate a ticket
  for bug #1's systemic code fix (grant-on-hotel-add to all members).\n  This is the
  real recurrence-prevention change and is currently untracked.\n- Chase Ryan for
  the audit list + backfill plan; confirm blast radius beyond Mark/Alyssa.\n- Drive
  the IMM definitive-property-list ask to closure so the over-grant can be tightened.\n-
  Confirm provisioning vector (form vs SSO/JIT) for affected users — determines whether\n
  \ ENT-6247 actually prevents recurrence.\n- Branches glloyd/ent-6245-... and glloyd/ent-6247-...
  suggest this lands on you; ENT-6247\n  is unscheduled in Triage and needs prioritisation.\n\nNo
  code changes made. No Linear/Slack writes made.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1778798100720309?thread_ts=1778795903.905479&cid=C08RJU9Q7FV
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Review ENT-6245 investigation + backfill plan (Ryan)
updated: 2026-05-15 13:47:59.680937
waiting_on: null
waiting_since: null
working_on: false
---

Ryan posted ENT-6245 investigation: short-term backfill to restore hotel access for the portfolio group, plus a potential code change to prevent recurrence. https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1778798100720309?thread_ts=1778795903.905479&cid=C08RJU9Q7FV