---
area: null
contexts:
- react
created: 2026-06-11 09:43:42.344271
defer_until: null
due: null
energy: medium
id: 2026-06-11T0943-review-pr-47479-tool-263-remove-account-integratio
order: null
output: |
  ## Agent run 2026-06-11T13:58:35

  Reviewed PR #47479 (https://github.com/canary-technologies-corp/canary/pull/47479)
  via the pr-review-toolkit (code-reviewer + pr-test-analyzer agents) plus direct
  structural verification on the fetched branch. Note: this PR was already APPROVED
  by gareth-lloyd and the item was in archive/ when the review completed, so this
  is confirmatory. No comments posted to GitHub.

  Verdict: clean removal, safe to merge. No critical issues.

  Verified directly (git grep on PR branch):
  - Zero dangling references to deleted symbols (update_salesforce,
    update_salesforce_to_snoozed, SalesforceIncidentPayload, _build_health_*,
    _is_gone_account_error, timeout constant) across backend/ and frontend/.
  - opinionated_state.py dep edit is correct and consistent: removes
    App.INCIDENTS from App.MONITORING's dependencies (line ~1911 block confirmed
    to be MONITORING) and mirrors it in INCIDENTS.depended_on_by; monitoring has
    no remaining imports from incidents.
  - All remaining imports in incidents/services/incident.py are used; internal
    integration-health (publish_status / IntegrationStatus / get_integration_status)
    is behaviorally unchanged.
  - CI fully green, E2E passed, coverage rose 74.56% -> 83.78%.

  One important callout (worth a note to Ramiro before/with the follow-up PR):
  - The PR description says the snooze feature + update_salesforce_snoozes cron
    are "intentionally left intact" — but the cron's only Salesforce path WAS
    ConfigurationService.update, which this PR strips. Post-merge the cron still
    clears expired snooze_alerts_until locally but never clears "Is Snoozed" in
    Salesforce; its docstring ("updates Salesforce to remove Is Snoozed") is now
    wrong. Fine given Integration_Health__c is confirmed unused SF-side, but the
    follow-up PR owner should know the cron is already neutered, not untouched.
    File: backend/canary/monitoring/tasks/update_salesforce_snoozes.py

  Test coverage analysis:
  - PR description's claim is accurate: snooze set/unset remains covered
    end-to-end by monitoring/tests/views/test_monitoring_configuration.py
    (set: lines 19-41, unset-via-Unset-sentinel: lines 43-65, real HTTP + DB).
  - The deleted test_configuration.py only tested SalesforceError swallowing for
    the now-deleted push — no surviving logic lost coverage.
  - Pre-existing (not introduced) gaps, low priority: MissingSnoozeAlertSetBy
    path untested; snooze_alerts_set_at/set_by bookkeeping unasserted; the
    snooze cron has zero tests; no positive assertion that subscribers fire on
    the property-audience path.

  Suggested follow-up if desired: one-line reply on the PR or Slack to Ramiro
  noting the cron is already a Salesforce no-op after this PR (drafted above —
  not sent, per external-write policy).
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/47479
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #47479: [TOOL-263] Remove Account.integration_health Salesforce
  write'
updated: 2026-06-11 13:58:35.000000
waiting_on: null
waiting_since: null
working_on: false
---

Ramiro, personally requested. Kills the ~15k/day Salesforce write load; first of 4 removal PRs. I wrote the code-archaeology history on TOOL-263.
https://github.com/canary-technologies-corp/canary/pull/47479