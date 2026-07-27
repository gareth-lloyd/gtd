---
area: null
contexts:
- react
created: 2026-07-23 10:46:48.815355
defer_until: null
due: null
energy: medium
id: 2026-07-23T1046-review-pr-50359-synxis-migration-andrea
order: null
output: |
  ## Agent run 2026-07-23T13:38+03:00

  Reviewed PR #50359 "[ENT-6126] Reconcile SynXis hotel_id on Wyndham brand flips"
  (https://github.com/canary-technologies-corp/canary/pull/50359, Andrea Bradshaw,
  Linear: https://linear.app/canary-technologies/issue/ENT-6126). Ran the full
  pr-review-toolkit (code-reviewer, pr-test-analyzer, silent-failure-hunter) plus my
  own read of the diff. NOTHING POSTED to GitHub — findings below are a local draft
  for you to act on.

  **State**: open, CI green, already APPROVED by rrgrs (2026-07-22) with one nit.
  477 additions / 9 files, all backend/canary onboarding + pms_gateway test stubs.

  **Verdict**: solid, well-tested PR — no blockers found. Design is sound: reconcile
  is de-facto Wyndham-scoped (only Wyndham providers emit SphConfiguration — verified),
  idempotent on re-run, 404 handling traced and correct, CRS config isolation tested.
  I'd approve with comments. Worth raising (ordered by importance):

  1. **Stage-ordering question**: CREATE_PMS_CONFIGURATION and PMS_SWITCH_COMPLETE run
     the same plan and share the "id differs" predicate. Once archive+cleanup complete,
     both gates pass; if an operator runs CREATE first, the reconcile flips the predicate
     and wyndham_pms_switch_complete_ready then returns "Nothing to complete" — COMPLETE
     is permanently blocked. Fine if COMPLETE is a superset-free no-op at that point;
     ask Andrea to confirm the runbook order isn't load-bearing.
  2. **Misleading error code on id collision**: the reconcile path reuses the
     duplicate-key -> ERROR_PMS_CONFIGURATION_ALREADY_EXISTS mapping (plan.py:104-112).
     PR description says this is deliberate ("fails loudly"), but in the reconcile case a
     unique-constraint hit means the NEW id is already claimed by another account — a real
     cross-hotel misconfiguration reported under a benign-sounding "already exists" code.
     Suggest restricting the expected-error mapping to reconciliation is None.
  3. **Silent swallow of malformed SynXis_CRS_ID__c**: _synxis_hotel_id_will_change
     (pms_switch_checks.py:86-96) catches ValueError with no log and returns False
     ("no change"). Blank/garbage SFDC id => operator sees "vendor unchanged / no PMS
     switch needed" — actively wrong message, zero signal. At minimum add a
     logger.warning; arguably the gates should return an explicit error.
  4. **Stale archive pair satisfies the guard on a SECOND flip**: the new
     wyndham_synxis_hotel_id_change_archived check accepts any completed
     PMS_SWITCH_ARCHIVE + CLEANUP pair — nothing ties them to the current id change. A
     hotel that flipped once (pair on record) drifts again later => guard passes green,
     old-id reservations never archived. Worth at least a docstring note or a recency
     bound.
  5. **Missing process-boundary wiring test** (also flagged by Macroscope): nothing
     asserts WYNDHAM_MSA CREATE_PMS_CONFIGURATION carries
     WYNDHAM_SYNXIS_HOTEL_ID_CHANGE_ARCHIVED (skippable=True). The wiring is one line in
     a ~350-line dict block; exact test precedent exists at
     onboarding/tests/models/test_script_config.py:127-140. ~10-line fix, cheapest
     high-value ask.
  6. **WYNDHAM_STAGING_MSA hole (probably fine, should be conscious)**: staging MSA uses
     StagingWyndhamPMSConfigProvider (emits SphConfiguration, operator-overridable
     hotel_id) but got NO guard check — staging re-runs reconcile unguarded. Likely
     acceptable for staging; worth one sentence from Andrea.

  Minor: pushback on rrgrs's "redundant account.synxis is None" comment — it's
  load-bearing for pyrefly type-narrowing of the later account.synxis.hotel_id accesses,
  so keep it (or re-narrow at use sites). Copilot's is-vs-== nit already addressed
  (head uses ==, matching file convention). "Id" -> "ID" naming nit valid but trivial.
  Mixed int/str in the synxis_hotel_id_reconciled {from, to} payload is mildly confusing.

  Strengths worth calling out to Andrea: idempotency verified, normalization
  (1234 vs "01234") pinned at both check and plan layers, CRS-config isolation test,
  reconcile result recorded only after successful upsert (no partial-state lie),
  reusable stub extensions instead of ad-hoc mocks.

  **Suggested next actions** (your call): (a) approve with the comments above — none are
  blockers, esp. since rrgrs already approved; (b) if you want, I can draft the GitHub
  review comments for you to approve before posting.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/50359
tags:
- morning-gtd
- github
- from-awareness
time_minutes: 20
title: 'Review PR #50359: synxis migration (Andrea)'
updated: 2026-07-23 13:52:28.106512
waiting_on: null
waiting_since: null
working_on: false
---

Andrea flagged in her EOD that this still needs review.
https://github.com/canary-technologies-corp/canary/pull/50359