---
area: null
contexts:
- react
created: 2026-07-07 10:35:47.056695
defer_until: null
due: null
energy: medium
id: 2026-07-07T1035-review-pr-49533-tool-108-deprecate-cohorthotel-opp
order: null
output: |
  ## Agent run 2026-07-07T08:40Z — Review of PR #49533

  PR: https://github.com/canary-technologies-corp/canary/pull/49533
  [TOOL-108] Deprecate CohortHotel opportunity-mirror fields (author: ramironieto).
  Reviewers: pod-enterprise, gareth-lloyd, abrad. State: OPEN. +97 / -57, 2 files.

  ### Verdict: APPROVE — clean, correct, well-scoped. No blocking issues.

  This is the "PR 2" step of the standard 3-PR field-deprecation flow
  (agent-plugins/.../backend/commands/deprecate_field.md). The usage-removal
  ("PR 1") already landed across #49180, #49409, #49415; column DROPs are the
  follow-up "PR 3". This PR only wraps 11 dead columns with deprecate_field()
  and drops the now-orphaned index.

  ### What I verified
  1. **No remaining production read/write of the 11 CohortHotel columns.** Grepped
     all 11 field names across canary/ + shared/. Every production hit resolves to
     SalesforceOpportunity — either `opportunity.<field>` on an SFO instance or a
     `opportunities__<field>` / `salesforcehotelaccount__opportunities__<field>`
     relation lookup. Checked the highest-risk files directly:
       - onboarding/agent_context/provider.py — reads all onboarding data from the
         latest SalesforceOpportunity per account; no `ch.<deprecated>` left.
       - onboarding/services/cohort_hotel.py — the bare `Q(training_date__lt=...)`,
         `Q(training_state=...)`, `onboarding_blocked_reasons__contains=...` filters
         are all on `SalesforceOpportunity.objects`, NOT CohortHotel.
       - onboarding/schemas/salesforce_hotel_account.py — training_*/go_live fields
         are `fields.Method` resolvers that pull from the opportunity.
       - onboarding/views/cohort_hotels.py — training_state typed as
         SalesforceOpportunity.TrainingState; filters route through the service.
  2. **Test factory correctly rerouted.** onboarding/testing.py `stub_cohort_hotel`
     keeps the legacy kwargs (training_state, onboarding_status, ...) for back-compat
     but no longer writes them to CohortHotel — it forwards them to a
     stub_salesforce_opportunity(). Explains why the cited 3135 tests still pass.
  3. **deprecate_field mechanics confirmed against the installed lib source.** At
     runtime it returns a plain descriptor (field leaves Django's field registry →
     excluded from SELECT; attribute access returns None + DeprecationWarning; any
     `.filter/.values/.order_by/Meta.indexes` reference would raise FieldError —
     which is exactly why the Meta index had to go). During
     makemigrations/migrate/showmigrations it returns the real field with null=True
     forced, so migrations still see the column (no accidental RemoveField) and,
     since all 11 columns are ALREADY nullable, no AlterField is generated. Matches
     the PR body's claims exactly.
  4. **Migration chain is safe.** 0158 depends on 0157
     (0157_alter_cohorthotel_training_state, from #49415 which merged to master
     2026-07-06 13:48Z). master had no competing 0157+/0158 onboarding migration, so
     no merge-time migration conflict. Index drop uses RemoveIndexConcurrently with
     `atomic = False` and is the sole op in the migration — the linter-approved safe
     online drop, so no IgnoreMigration rule needed (consistent with "lintmigrations
     clean" in the PR).
  5. **onboarding_type correctly NOT deprecated** — still written on creation and
     read as the cohort-less-earmark fallback in
     CohortHotelService.get_onboarding_type_for_cohort_hotel. Good call to exclude it.

  ### Non-blocking heads-up (author FYI, not a review blocker)
  Several throwaway scripts under canary/tmp/ still reference these columns directly
  on CohortHotel and would break/return None post-deploy:
    - tmp/repeatable/bw/correct_best_western_portfolio_memberships.py
      (`CohortHotel.objects...order_by("go_live_date_from_source_of_truth")` →
      FieldError at runtime; `ch.go_live_date_from_source_of_truth` → None+warn)
    - tmp/repeatable/wyn/correct_wyndham_portfolio_membership.py (ch.onboarding_status,
      ch.onboarding_blocked_reasons, ch.go_live_date_from_source_of_truth)
    - tmp/repeatable/bw/analyze_inconsistencies.py, tmp/unmigr.py, several
      tmp/onetime/wyn|ihg scripts
  These are past-incident remediation scripts, not in the deploy path or CI, so they
  don't block. Worth a one-line note to Ramiro that the "repeatable" ones would need
  re-pointing at SalesforceOpportunity if ever re-run.

  ### Not done
  Did NOT post anything to GitHub (no approval/comment submitted) — recorded here only.
  If you want, I can draft an inline PR comment / approval for you to send.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/49533
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #49533: [TOOL-108] Deprecate CohortHotel opportunity-mirror fields'
updated: 2026-07-07 08:41:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Personal review request from ramironieto (you + abrad). Chore: deprecate CohortHotel opportunity-mirror fields.
https://github.com/canary-technologies-corp/canary/pull/49533