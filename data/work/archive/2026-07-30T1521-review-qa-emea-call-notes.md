---
area: null
contexts: []
created: 2026-07-30 15:21:41.333470
defer_until: null
due: null
energy: low
id: 2026-07-30T1521-review-qa-emea-call-notes
order: null
output: |-
  ## Agent run 2026-07-31T11:45:00+01:00

  Read the full Gemini notes + transcript (15-min call, Jul 30). Speakers were James
  Saram, Martijn Dekker, Eugênio Portella — you don't appear in the transcript, so this
  is a catch-up digest. Doc:
  https://docs.google.com/document/d/1tguPkU-si0lylzJHWc9xkKGYm5Y21WZnJvzNXPyI3HI/edit

  **TLDR:** Routine sync, no action items assigned to you. Main decision: automated
  kiosk/tablet tests are generic (default kiosk config only), so hotel-specific
  configs/feature flags still require manual testing — James will manually test the
  Kempinski ("Kapinsky" in notes) tablet flow using Eugênio's Notion test cases.
  Two strategic items worth your awareness:

  1. **Guest Foundation Service (GFS)** — Martijn briefed the QA team on the kickoff
     (led by Julius and Aish): replacing PMS-gateway→Canary DB syncing with live API
     requests to pms-gateway when e.g. opening a reg card. Rollout per area with
     per-hotel feature flags. Martijn flagged it as high-blast-radius and wants QA
     heavily involved in verification.
  2. **Clock PMS integration** — new two-way PMS integration; Martijn's team pulled in
     to support. He noted pms-gateway team historically tests via Postman only and
     misses reg-card/check-in edge cases, so wants systematic QA verification with
     dev + QA + product perspectives.

  **Other points:**
  - Kempinski tablet flow updated (billing address added by EJ); EJ + Elena building
    the flow in UAT/tablet-reg; property kickoff early next week. Automated tests run
    as CI checks on every PR (must pass to merge).
  - QA capacity is a pain point: only 5 QAs supporting the whole company; Eugênio
    overwhelmed (also supports Wyndham directly, gets direct emails from them) and has
    flagged the structure to Lorena. He committed 8h (one day) this week for manual
    testing + reviewing the test automation suite.
  - Cycle planning done; Marta on Luna, will need more work toward end of cycle.
  - Priorities stack-ranked: Clock PMS and GFS/pms-gateway are the two competing QA
    priorities (Host/Hostaway PMS already covered by Martin on the QA side).

  **Action items (none yours):**
  - Eugênio: confirm Elena knows the CI automated tests exist and must pass pre-merge.
  - James: manual-test tablet flow from the test case folder; re-test with EJ once the
    user environment is configured.

  No response or follow-up from you appears required; awareness-only unless you want
  to weigh in on GFS QA involvement or Clock PMS test planning.
project: null
source_id: null
tags: []
time_minutes: 5
title: review QA emea call notes
updated: 2026-07-31 12:43:13.729547
waiting_on: null
waiting_since: null
working_on: false
---

https://docs.google.com/document/d/1tguPkU-si0lylzJHWc9xkKGYm5Y21WZnJvzNXPyI3HI/edit?tab=t.vji2tygccs5f