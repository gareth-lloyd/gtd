---
area: null
contexts:
- react
created: 2026-05-15 07:28:44.650733
defer_until: null
due: null
energy: low
id: 2026-05-15T0728-review-kill-mark-frentz-duplicate-portfolio-2535-i
order: null
output: "## Agent run 2026-05-15T07:25Z\n\n**Verdict: NOT actionable yet. Do not delete
  either portfolio. The task's\npremise (\"kill 2535 in favor of 2080\") is one of
  two competing proposals and\nis explicitly unconfirmed by the team. The real blocker
  is data accuracy, not\na technical merge — this is a CS/data-reconciliation task,
  not eng work.**\n\n### What the Slack thread actually says (read full 59-reply thread)\n-
  Same customer = Intermountain Management (IMM); Mark Frentz is their admin\n  contact.
  Two portfolios exist:\n  - 2535 \"Mark Frentz's Portfolio\" — **105 properties**\n
  \ - 2080 \"IMM Portfolio\" — **92 properties**\n- They do NOT match (105 vs 92).
  Natalya: \"one is accurate and one isn't\" —\n  she does NOT know which, and flags
  \"there's a good chance this is not\n  accurate\" for the larger one too.\n- Direction
  is UNDECIDED. Connor floated BOTH:\n  1. Kill 2535, use 2080 (the framing in this
  task), and\n  2. The opposite — rename 2535 -> \"IMM\" and delete 2080, because
  2535 has\n     MORE properties and he \"want[s] to confirm the Mark portfolio does\n
  \    indeed have all of their properties.\"\n- Lean (Natalya): prefer the non-personal
  name (2080/IMM) since \"it doesn't\n  have Mark's name tied to it\"; Rachel also
  filed her change ticket against\n  2080. But this is naming preference, not a confirmed
  property-set decision.\n- Hard blocker: need an authoritative property list from
  the customer +\n  Rachel (owner) is on vacation. Nobody has reconciled the 105/92
  delta.\n- **Interim issue already resolved**: Connor granted Mark + Alyssa\n  portfolio-wide
  Property Manager prop roles on the UNION of both portfolios.\n  Access complaint
  is fixed; no urgency remains. Connor: \"I don't like it but\n  it'll fix the issue.\"\n\n###
  Technical review (codebase, read-only — no prod access)\n- No `merge_portfolio`/consolidate
  exists. Only\n  `PortfolioService.delete_portfolio(portfolio, deleted_by, browser_info)`\n
  \ in backend/canary/portfolios/services/portfolio.py.\n- delete_portfolio refuses
  ROOT/parent portfolios\n  (`CannotDeleteRootPortfolio`). PRE-CHECK NEEDED: confirm
  the loser\n  portfolio is not a parent and has no child portfolios before any plan.\n-
  delete_portfolio is atomic and cascades: removes PortfolioManagedUser,\n  PortfolioWidePropertyRoleGrant,
  PropertyRole, PortfolioRoleGrant,\n  PortfolioRole, PortfolioHotel, then calls\n
  \ RoleService.remove_company_hotel_users_from_users. Users left with no\n  remaining
  portfolio membership can be deactivated.\n- Reporting continuity risk: Portfolio
  carries explo_customer_token and\n  override_explo_* dashboard IDs + reporting_currency.
  Deleting whichever\n  portfolio has the live Explo dashboards configured breaks
  customer\n  reporting. Must check both before choosing the survivor.\n- \"Mark Frentz's
  Portfolio\" / \"IMM Portfolio\" are almost certainly the free\n  `name` field (identifier
  enum is fixed/likely null here). Renaming is\n  trivial; the only thing that matters
  is the hotel set + reporting config.\n- Per saved guidance: membership changes must
  go through\n  PortfolioService.add_hotels / remove_hotel, never PortfolioHotel directly.\n\n###
  Safe consolidation sequence (for WHEN it's approved — not now)\n1. Get authoritative
  hotel list from Intermountain Management (Rachel owns).\n2. Pick survivor: prefer
  non-personal name AND whichever holds the live\n   Explo/reporting config — verify
  these don't conflict.\n3. Reconcile the ~13+ delta: add every missing hotel to the
  survivor via\n   PortfolioService.add_hotels (the union is the safe superset; prune
  only\n   hotels the customer confirms are gone).\n4. Migrate PortfolioManagedUser
  + role grants to the survivor.\n5. Verify explo_customer_token / dashboard overrides
  on the survivor.\n6. PortfolioService.delete_portfolio on the loser. Audited via\n
  \  PortfolioEventService.\n\n### Recommendation\n- Defer / move to WAITING on Rachel's
  return + authoritative property list\n  from the customer. There is no eng action
  and no urgency (access fixed).\n- When unblocked this is a CS-driven cleanup with
  an eng-assisted scripted\n  step; loop in whoever owns IMM. Do not let \"delete
  2535\" be executed off\n  the current ambiguous state — 2535 has the larger property
  set and may be\n  the more complete one.\n- No external/prod actions taken. No Slack
  reply sent.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1778796343763539?thread_ts=1778792630.221239&cid=C01V4NYTQRH
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Review: kill Mark Frentz duplicate portfolio (2535) in favor of IMM (2080)'
updated: 2026-05-15 13:48:02.429737
waiting_on: null
waiting_since: null
working_on: false
---

Connor in #product-questions: two portfolios causing confusion; wants to consolidate Mark Frentz's Portfolio (2535) into IMM Portfolio (2080) but needs confirmation (chatted w/ Rachel). https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1778796343763539?thread_ts=1778792630.221239&cid=C01V4NYTQRH