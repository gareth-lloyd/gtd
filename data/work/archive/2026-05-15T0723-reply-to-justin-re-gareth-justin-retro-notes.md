---
area: null
contexts:
- react
created: 2026-05-15 07:23:46.092145
defer_until: null
due: null
energy: low
id: 2026-05-15T0723-reply-to-justin-re-gareth-justin-retro-notes
order: null
output: "## Agent run 2026-05-15T10:40 (research + drafts; nothing sent)\n\n### Context
  gathered\n- Slack DM (Justin Ligman, U08T86L3ES3, channel D098AGZSU86, parent ts\n
  \ 1778784804.530579): \"shared my notes with you. feel free to tweak or\n  add things
  i may have missed.\" Links the Notion retro. No thread\n  replies yet — a reply
  is expected.\n- Notion doc \"Retro with Gareth/Justin\"\n  (https://www.notion.so/36081468615180178901c69fc61df772).
  Current\n  content = exactly the bullets quoted in Slack:\n    Learnings: 1) \"Perfect
  Storm\"  2) Feature flags painful — only\n    depend on backend flag  3) Onboarding
  scripts decide who/when but\n    call a Pod-owned API  4) CC should consider Enterprise
  impact in\n    planning + include them earlier (4a: regular Gareth<>Andrea syncs).\n
  \   Notes: ENT moving under Andrea (timezone win).\n    Follow Ups: (a) session
  with ENT to learn the onboarding stuff;\n    (b) check if messaging rearchitecture
  (system msgs as auto-created\n    messages) fits ENT's onboarding system.\n- The
  two Follow-Up entries are mention-page links (task stubs); not\n  separately accessible
  via integration, but their text is fully\n  captured in Justin's Slack message above.\n-
  Incident this retro covers = IHG HotelKey pilot rollout (matches\n  memory project_ent6032_ihg_hotelkey_pilot
  + the AttributeError fix on\n  HotelKey accounts in PMS create-config, current branch\n
  \ ihg-hotelkey-account-attr). Messaging follow-up ties to SRE-362.\n\n### DRAFT
  — proposed Notion tweaks/additions (engineering side, NOT applied)\nAdd to **Learnings**:\n
  \ 5. Feature-flag failure mode in detail: rollout was gated on both a\n     frontend
  and a backend flag; when they diverged, hotels landed in\n     a partially-enabled
  state. Action: gate on a single backend-owned\n     flag; frontend reads flag state
  from backend rather than holding\n     its own. (sharpens existing point 2)\n  6.
  Cross-pod API contract gap: onboarding scripts call a Pod-owned\n     API, but no
  contract/integration test exercised the inputs\n     onboarding actually sends (e.g.
  HotelKey account types), so an\n     unhandled account attribute surfaced as a runtime
  AttributeError\n     in prod. Action: contract tests at the onboarding↔Pod boundary;\n
  \    Pod owns a documented input contract. (sharpens existing point 3)\nAdd to **Notes**:\n
  \ - Onboarding cohort included dual-brand / shared-integration\n    properties (e.g.
  Bessemer shares one integration across brands);\n    cohort-selection logic needs
  explicit handling + tests for that.\nAdd to **Follow Ups**:\n  - Add an explicit
  \"Enterprise impact\" sign-off step to the project\n    planning / launch checklist
  before rollout of changes to shared\n    onboarding or messaging infra.\n  - Backfill
  contract/integration tests for onboarding scripts → Pod\n    APIs, HotelKey account
  path specifically.\n\n### DRAFT — proposed Slack reply to Justin (DM thread, NOT
  sent)\n\"Thanks Justin — added a few engineering-side notes to the doc:\n• Expanded
  the feature-flag learning with the specific failure mode\n  (FE/BE flags diverging)
  + recommendation to gate on a single\n  backend-owned flag.\n• Added a learning
  on the onboarding↔Pod API contract gap — the\n  HotelKey account attribute that
  surfaced as a prod AttributeError\n  would've been caught by a contract test at
  that boundary.\n• Noted the dual-brand / shared-integration cohort edge case (Bessemer).\n•
  Added follow-ups: an ENT sign-off step in the launch checklist for\n  shared onboarding/messaging
  changes, and backfilling contract tests\n  for the onboarding→Pod path.\nAgree the
  regular sync with Andrea + ENT moving under her will help a\nlot. Happy to own the
  contract-test follow-up if useful.\"\n\n### Status\nNothing sent or edited. Awaiting
  Gareth's approval on (a) whether the\nIHG HotelKey framing is right, (b) sending
  the Slack reply, (c) applying\nthe Notion edits.\n"
project: null
source_id: https://canarytechnologies.slack.com/archives/D098AGZSU86/p1778784804530579
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Justin re: Gareth/Justin retro notes'
updated: 2026-05-15 13:09:32.114465
waiting_on: null
waiting_since: null
working_on: false
---

Justin shared retro Notion doc, asked me to tweak/add. https://canarytechnologies.slack.com/archives/D098AGZSU86/p1778784804530579