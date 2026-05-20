---
area: null
contexts:
- react
created: 2026-05-20 11:34:33.337198
defer_until: null
due: null
energy: medium
id: 2026-05-20T1134-review-prs-43847-and-45628-ryan-rogers-enterprise
order: null
output: |
  ## Agent run 2026-05-20T12:05

  Read both diffs end-to-end + surrounding source (provider files, LoyaltyConfig + BW models, MSAService, shared auth/urls/admin_history, OnboardingValue model).

  ### PR #43847 — Foundation + Portfolio + User
  Verdict: approve as-is. Already approved on GitHub; enterprise visibility satisfied.
  - User PII scrub correctly implemented in `backend/canary/hotels/agent_context/providers/user.py` (only uuid + is_active/is_staff/is_superuser; no email/username/name). Negative test covers it.
  - `PropertyRoleGrant` exposure on user is acceptable given auth class only accepts GLOBAL JWT or static bearer (`backend/shared/shared/agent_context/auth.py`).
  - Portfolio queries are clean: `select_related("parent")`, narrow `only(...)`, `order_by("id")` for stable pagination, 500/1000 caps.

  ### PR #45628 — Cohort + Loyalty + Hotel schema extensions
  Verdict: approve with two cheap follow-ups (not blockers).

  Two concrete asks:

  1. **MSAService test does not actually exercise the LIVE-vs-ALL filter** (`hotels/agent_context/tests/test_hotel_provider.py::test_includes_live_and_all_msas`). The fixture uses `LIVE` + past `go_live_date`, which satisfies BOTH `MSAService.get_live_msas_for_hotel` and `get_all_msas_for_hotel` — the "all" status set is a superset of "live". Test would still pass if both helpers were aliased to the same function. Fix: add a second opportunity with `onboarding_status=CONFIGURATION` and future `go_live_date`, assert it appears in `all_msas` but not `live_msas`. (This is the very item Ryan flagged in his own checklist.)

  2. **Tighten onboarding-value secret handling** (`hotels/agent_context/providers/hotel.py` SAFE_ONBOARDING_VALUE_KINDS). Allowlist is the right approach, but the model already has `OnboardingValue.SECRET_VALUE_KINDS`. Two small hardening steps:
     - Add module-level `assert SAFE_ONBOARDING_VALUE_KINDS.isdisjoint(OnboardingValue.SECRET_VALUE_KINDS)` so any future regression fails at import.
     - Add `TWILIO_REGISTRATION_DATA` and `TWILIO_PRE_REGISTERED_DATA` to `SECRET_VALUE_KINDS` — Ryan's own redaction test (~line 787) shows these hold auth_tokens.

  Other findings (non-blocking):
  - **No secrets leaking through loyalty provider**: `MembershipGatewayConfiguration` exposes only vendor/default_kind/default_level/use_api_enrollment_only (no creds); `BestWesternConfiguration` exposes only the BW property id (`hotel_association_id.identifier`). Safe.
  - **admin_history is safe**: `shared/agent_context/admin_history.py` consumes Django LogEntry change-messages, which only contain field names, not values. No custom `log_change` overrides in `membership_gateways/` or `onboarding/`.
  - **No soft-delete footgun**: Cohort/CohortHotel/Portfolio/OnboardingScriptBatch/SalesforceOpportunity/OnboardingValue/MembershipGatewayConfiguration all use `TimeStampedModel`, not `SoftDeleteModel`. `.objects` vs `.every` convention doesn't apply.
  - **N+1 in loyalty path**: hotel provider's `_loyalty_for` triggers a lazy FK fetch on `bw.hotel_association_id.identifier` for every BW hotel call. Worth `select_related("best_western_configuration__hotel_association_id")`.
  - **Cohort `batches` is unpaginated** while `hotels` is paginated. For a BW/IHG wave cohort with many script batches, response size balloons. Cap with `[:N]` or paginate.
  - **Discoverability**: `/agent_context/loyalty_config/<uuid>/` takes a *hotel* UUID, but `list_agent_context_providers` doesn't surface that — only msgspec field types. Worth a future `description` class attribute on `AgentContextProvider`.
  - **Per-call cost** on `/agent_context/hotel/<uuid>/` increases by ~6–8 SQL roundtrips (live_msas, all_msas, cohorts, loyalty, opportunities, onboarding_values, admin_history). Watch Datadog post-deploy if MCP fans out across portfolios.

  ### Cross-cutting
  - **Static-token auth fallback is materially more sensitive now**. With Salesforce opportunity stage, MSA membership, and cohort go-live dates exposed, `AGENT_CONTEXT_SECRET_TOKEN` is a bigger liability post-#45628. Suggest filing a follow-up to remove the static fallback and require GLOBAL JWT only.
  - **Investigation-agent persistence**: MCP responses can land in Linear comments forever. Cohort go-live dates and SalesforceOpportunity stages on non-Closed-Won deals are commercially sensitive. Worth confirming with deal-desk that this is acceptable, or restrict opportunities to `stage in {"Closed Won"}` in the response.

  ### Suggested PR comment (drafted, NOT posted)

  PR #43847: no comment, approve as-is.

  PR #45628: comment drafted below — needs Gareth approval before sending.

  ----
  Enterprise review — overall LGTM, two concrete asks and a few follow-ups.

  Blocking-ish (both cheap):

  1. `test_includes_live_and_all_msas` doesn't actually differentiate the two helpers — your fixture (`LIVE` + past `go_live_date`) satisfies both `MSAService.get_live_msas_for_hotel` and `get_all_msas_for_hotel` (the "all" status set is a superset of "live"). Test would still pass if both were aliased. To exercise the filter, add a second opportunity with `onboarding_status=CONFIGURATION` and a future `go_live_date`, then assert it appears in `all_msas` but not `live_msas`.

  2. `SAFE_ONBOARDING_VALUE_KINDS` is the right allowlist approach, but the model already maintains `OnboardingValue.SECRET_VALUE_KINDS`. Two small hardening steps:
     - Add `assert SAFE_ONBOARDING_VALUE_KINDS.isdisjoint(OnboardingValue.SECRET_VALUE_KINDS)` at module load so any future regression fails at import.
     - Add `TWILIO_REGISTRATION_DATA` and `TWILIO_PRE_REGISTERED_DATA` to `SECRET_VALUE_KINDS` — they hold auth_tokens (your own redaction test on ~line 787 covers it).

  Non-blocking:
  - `_loyalty_for` triggers a lazy FK on `bw.hotel_association_id.identifier`. `select_related("best_western_configuration__hotel_association_id")` would save a query per BW hotel.
  - Cohort `batches` is unpaginated while `hotels` is paginated. For a wave cohort with many batches the response can balloon — cap with `[:N]` or paginate.
  - LLMs hitting `/agent_context/loyalty_config/<uuid>/` won't easily learn that the URL UUID is the *hotel's* UUID. A `description` field on `AgentContextProvider` surfaced via `list_agent_context_providers` would fix this — out of scope here.
  - With SalesforceOpportunity stage now exposable, the `AGENT_CONTEXT_SECRET_TOKEN` static fallback is materially more sensitive than before — worth filing the removal as a follow-up.
  ----

  Status: review complete, comment drafted, nothing posted to GitHub. Awaiting Gareth's decision on whether to send (and which items to keep/drop).
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1779202190630429?thread_ts=1779202190.630429&cid=C0B1MN8F869
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 30
title: 'Review PRs #43847 and #45628 (Ryan Rogers, enterprise MCP exposure)'
updated: 2026-05-20 12:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Ryan asked the enterprise team for review on the foundational agent_context provider PR and the additional cohort/loyalty extensions. https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1779202190630429?thread_ts=1779202190.630429&cid=C0B1MN8F869