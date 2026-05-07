---
area: null
contexts:
- consume
created: 2026-05-07 11:29:44.797021
defer_until: null
due: null
energy: low
id: 2026-05-07T1129-read-rafael-nunes-on-pool-portfolio-one-to-many-de
order: null
output: "## Agent run 2026-05-07T11:35:00\n\nRead the full #epd-general thread (44
  replies). Rafael's specific message\nis reply 43; Blake's resolution is reply 44
  with a thank_you from Rafael.\n\n### Thread origin (the frame, not what was promoted)\nJason
  Flax kicked it off: he's building the push notification service\nand realized the
  data model doesn't fit. He had tied it to Hotel; Jordan\nsaid that's wrong. Tying
  it to Portfolio is the obvious fallback but\nhits the same one-to-many problem Rafael
  is now flagging from a\ndifferent angle.\n\n### Rafael's point (the promoted item)\nIn
  Guest Profiles he needs to aggregate a set of hotels into a single\n\"account pool\".
  Because a hotel can belong to many portfolios, there is\nno automatic way to derive
  which portfolio a pool belongs to from\nhotel→portfolio membership. So portfolio-as-pool-owner
  is ambiguous.\n\n### Blake's resolution (which Rafael accepted with a reaction)\nPools
  that cross hotel boundaries should be created manually. They sit\nin the bounds
  of contractual relationships, so manual provisioning is\nthe right modeling choice
  — not something to derive from existing\nmembership graphs. For single-hotel pools,
  an enum on the pool plus a\ndirect hotel FK (with constraints) keeps it explicit.\n\n###
  Wider design points worth retaining\n- Hotels-to-portfolios is many-to-many; portfolios
  overlap Venn-style.\n  Logical portfolios exist (regional groupings) but don't share
  data.\n- Jordan: push/app credentials belong at portfolio level; there will be\n
  \ canonical portfolios per brand. He floated portfolios needing to live\n  as global
  objects (DynamoDB, not just Postgres).\n- Blake: PMS Gateway lacks direct portfolio
  access; portfolios should\n  be a foundational, global service.\n- Constraint required
  either way: a hotel cannot be in >1 credentialed\n  portfolio, OR we define a precedence/resolution
  order. Blake stated\n  this as: \"Notification credentials → one-to-many → portfolios\"
  with a\n  check that prevents multiple credentials applying to the same hotel.\n-
  Same shape applies to guest-profile pools — same check needed.\n- Portfolios can
  nest but we currently cap at one level deep. Use case\n  is presentational (\"Wyndham\"
  → \"Wyndham LATAM\"). Each level can still\n  own its own app credentials per Jordan.\n\n###
  What I (Gareth) committed to in the thread\n- A call with Jason (tomorrow in the
  thread = today, 2026-05-07) about\n  portfolio formalization + push notification
  routing.\n- Said I've been thinking about this for a while and there's an\n  opportunity
  to tighten up portfolio rules and definitions. Looped in\n  Connor and Andrea with
  eyes reactions.\n- Suggested formalizing types of portfolios so one type can be
  relied\n  on as the brand-grouping anchor.\n\n### Open threads / things to come
  back to\n- Whether to outright forbid a hotel being in >1 credentialed portfolio\n
  \ vs. defining precedence rules. (I leaned forbid; Jordan was OK with\n  multiple.)\n-
  Whether portfolios should move to a global service / DynamoDB\n  storage. Touches
  PMS Gateway access too.\n- The rule that pools-crossing-hotel-boundaries must be
  manual is now a\n  shared assumption between push-notifications and Guest Profiles
  —\n  worth writing down in whatever portfolio formalization doc comes out.\n\n###
  My take for follow-up\nSame root problem is showing up in two products in the same
  week (push\nnotifications, guest profiles). Strong signal that a portfolio-\nformalization
  design doc is overdue and would unblock multiple teams at\nonce, not just Jason.
  Worth drafting before the call with Jason rather\nthan only inside it.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/C05K3SM1EDC/p1778088309253729?thread_ts=1778078223.074589&cid=C05K3SM1EDC
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read: Rafael Nunes on pool/portfolio one-to-many design constraint'
updated: 2026-05-07 13:54:12.017971
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from awareness. Rafael in #epd-general flagged one-to-many issue: pools per portfolio when a hotel can be in many portfolios.
https://canarytechnologies.slack.com/archives/C05K3SM1EDC/p1778088309253729?thread_ts=1778078223.074589&cid=C05K3SM1EDC