---
area: null
completed_at: 2026-08-05 14:55:56.286894
contexts:
- react
created: 2026-08-05 07:19:55.316937
defer_until: null
due: null
energy: medium
id: 2026-08-05T0719-review-pr-52136-tool-508-add-optional-sfdc-opportu
order: null
output: |
  ## Agent run 2026-08-05T13:41:17

  Reviewed PR #52136 (https://github.com/canary-technologies-corp/canary/pull/52136) —
  [TOOL-508] Add optional sfdc_opportunity_id to OnboardingPlanData, by Ramiro Nieto.
  Ran two review agents (general code review + test-coverage analysis) over the diff,
  verified claims against the codebase. NOTHING POSTED to GitHub — findings below are
  for you to relay/approve manually.

  **Verdict: no blockers — safe to approve.** 44 additions, purely additive plumbing;
  all CI green (backend tests, linters, E2E). Dataclass field is appended last with a
  default, so all ~26 existing OnboardingPlanData construction sites are unaffected.
  The threading point is correct: data is built before provider selection AND provider
  __init__, so the TOOL-485 consumer sees it in both places. Verified no cross-test
  pollution from the module-level NoOpPlan/RecordingProvider test classes.

  Worth raising (the one substantive item):
  1. sfdc_opportunity_id is accepted unvalidated (onboarding/services/onboarding.py:282).
     The app already guards this exact mistake elsewhere: _is_valid_salesforce_opp_id()
     (same file, ~line 1172, used in fetch_account_id_from_salesforce) and the "001"
     account-prefix check in views/onboarding_hotel_products.py:55. Once TOOL-485's
     provider lands, a wrong ID silently scopes plans to the wrong/empty opportunity
     instead of erroring. Two-line fix, cheapest now while there's a single entry point.

  Minor / take-or-leave:
  2. Test: add autospec=True to the new @patch("...query_salesforce") — the CI canary
     linter already flags it; verified autospec works here (log_elapsed uses
     functools.wraps; both call sites are positional-compatible; in-file precedent at
     line 2155).
  3. Test robustness: RecordingProvider appends the mutable `data` object and the assert
     reads it after the run. OnboardingPlanData is non-frozen and this service late-
     assigns fields after provider construction — recording data.sfdc_opportunity_id
     (the scalar) at __init__ time would pin "present at construction", the actual
     contract TOOL-485 depends on.
  4. The 2-line field comment's second clause ("plans fall back to querying all eligible
     opportunities") documents behavior of a not-yet-written provider; house comment
     rules prefer one line, e.g. "Scopes plans to a single opportunity; None means
     account-wide."
  5. Follow-up notes for the ticket (not this PR): CohortHotelService.get_local_onboarding_data
     (cohort_hotel.py:~567) already has a SalesforceOpportunity in hand and doesn't pass
     it — post-TOOL-485 that path silently takes the account-wide fallback. Also nothing
     verifies the opportunity belongs to the account (needs an SF round trip — reasonable
     to defer to the consuming provider, but worth stating in TOOL-485).

  Positives worth mentioning to Ramiro: test asserts at the provider-constructor
  boundary (the exact TOOL-485 contract) using real ABC subclasses rather than mocks;
  stub extended keyword-for-keyword; logger.bind(**asdict(data)) now carries the
  opportunity ID into every onboarding log line for free.

  Next step: this was a personal review request (you + ldewald) — post the review on
  GitHub yourself, or tell me which of the above to draft as review comments and I'll
  prepare exact text for your approval.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/52136
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #52136: [TOOL-508] Add optional sfdc_opportunity_id to OnboardingPlanData'
updated: 2026-08-05 14:55:56.286874
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro Nieto, personally requested (you + ldewald).
https://github.com/canary-technologies-corp/canary/pull/52136