---
area: null
contexts: []
created: 2026-05-18 15:12:54.565837
defer_until: null
due: null
energy: low
id: 2026-05-18T1512-push-on-tipping-and-emea-things-that-need-rules-ba
order: null
output: "## Agent run 2026-05-19T15:30 (EMEA Block 2 Planning review)\n\nRead the
  EMEA Block 2 Roadmap Planning meeting note (2026-05-15):\nhttps://www.notion.so/36181468615180168d3bea77fa01ed93\n\n###
  Things explicitly flagged for \"Gareth's rule engine\" (enterprise team)\n\n1. **Check-in
  v3 — Additional Guest Support (region-specific rules).**\n   Next major Check-in
  v3 feature after OCR. The doc states it\n   \"will leverage Gareth's rule engine
  from enterprise team to apply\n   region-specific rules.\" Driver: regions have
  different requirements\n   for international vs. domestic guests; customers are
  currently\n   over-collecting data from domestic guests due to lack of regional\n
  \  logic. Greco-Gel/Beck Hotel has a manual workaround today.\n\n2. **GDPR / regional
  compliance.** Team plans to apply the rule engine\n   to handle GDPR and regional
  compliance requirements. Needs Aksel\n   looped in for public-facing documentation
  + audit (open action item,\n   unassigned). This is a compliance-grade use of the
  rule engine —\n   worth pinning down what \"compliance via rules\" means vs. CS
  config.\n\n3. **Design-philosophy constraint (the real ask).** Configuration\n   blocks
  must be abstract enough that ID flows and additional-guest\n   flows adapt automatically
  based on (a) hotel location, (b) guest\n   passport/nationality, and (c) regional
  requirements. Explicitly:\n   \"cannot rely on CS configuration for regional compliance.\"
  This is\n   the strongest signal that regional rules need to live in the rule\n
  \  engine, not in per-hotel CS setup.\n\n### Adjacent / regional but NOT clearly
  rule-engine (voice config)\n\n- Voice AI language detection: country-code → predicted
  guest language,\n  phone-number → reservation language match, and IVR \"press 1
  for\n  default language\" routing for hotels with one predominant language.\n  Regional
  in nature and rules-ish, but framed as voice-team A/B tests,\n  not the enterprise
  rule engine. Flag as adjacent — possible future\n  overlap if language routing becomes
  policy-driven.\n\n### Note on \"tipping\"\n\nThe GTD item title mentions tipping,
  but this planning block contains\n**no tipping content**. Tipping regional rules
  (if that's a real need)\nwould have to be pushed/sourced elsewhere — not covered
  by this doc.\n\n### Suggested next actions (for user to decide)\n- Confirm scope/ownership
  of \"rule engine for region-specific check-in\n  additional-guest rules\" with EMEA
  team — this is the concrete Block 2\n  dependency on you.\n- Clarify expectations
  for GDPR-via-rule-engine + sync with Aksel.\n- Separately chase down the \"tipping
  needs rules\" thread; it is not in\n  this document.\n\n## Agent run 2026-05-19T16:10
  (design note drafted)\n\nWrote a short design note: how rules_based_configuration
  addresses items 1\n(Check-in v3 region-specific rules) and 2 (GDPR/regional compliance)
  via a\nnew brand-agnostic \"General Rules\" layer enforced at startup.\n\nDraft
  (local, uncommitted):\n/Users/garethlloyd/projects/canary/.local-drafts/general-rules-rbc-design-note.md\n\nKey
  points: rules_based_configuration already has region/country matchers,\nOverridePolicy.FINAL
  locking, and startup system-check enforcement; the gap\nis that legal rules are
  per-brand (Wyndham tree only) and can silently\ndiverge. Proposal: one general_rules.py
  registry of legal universals +\na cross-brand startup conformance check that refuses
  to boot on violation.\nOpen questions flagged: scope-intersection semantics, negative
  scopes,\nmigration of existing WYNDHAM_NO_ID_* groups, ownership/legal sign-off.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Plan next steps on check in v3 additional guest and GDPR compliance using rules-based
updated: 2026-05-19 15:57:52.048209
waiting_on: null
waiting_since: null
working_on: false
---

https://www.notion.so/canarytechnologies/Block-2-Planning-36181468615180168d3bea77fa01ed93?source=copy_link

Key: We will need to have general rules. 
MSAs cannot conflict with these
Therefore they need to be truly general