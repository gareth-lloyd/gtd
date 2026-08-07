---
area: null
completed_at: 2026-08-06 14:17:57.647423
contexts:
- react
created: 2026-08-06 11:56:55.356310
defer_until: null
due: 2026-08-06
energy: medium
id: 2026-08-06T1156-review-pr-51809-tool-500-relink-salesforce-hotel-a
order: null
output: |
  ## Agent run 2026-08-06T14:05

  Reviewed PR #51809 (https://github.com/canary-technologies-corp/canary/pull/51809),
  Linear TOOL-500 (https://linear.app/canary-technologies/issue/TOOL-500/relink-stale-salesforcehotelaccount-hotel-links-during-salesforce-sync).
  Author Ramiro Nieto. Diff is small: +32/-9 across
  `onboarding/services/salesforce_hotel_account.py` and its test file.
  No review comments posted — nothing sent to GitHub or Linear.

  ### Verdict

  Sound fix, mechanism verified against the code. I'd approve with two questions
  (items 2 and 3 below) and one operational heads-up (item 4). Nothing here is a
  correctness blocker.

  ### What it does

  The heal loop in `get_or_create_salesforce_hotel_accounts` used to only fill an
  *empty* `SalesforceHotelAccount.hotel`. It now treats `SalesforceHotelMetadata`
  as source of truth: if metadata points at a different hotel, relink, refresh the
  search vector, and log `get_or_create_salesforce_hotel_accounts.relink_stale_hotel`.

  ### Premise checks (all hold)

  - `SalesforceHotelMetadata.canary_hotel` is a OneToOne and `sfdc_id` is unique
    (`internal/models/models.py:140-176`), so metadata→hotel is unambiguous.
  - `SalesforceHotelAccount.hotel` has NO unique constraint (only
    `unique_salesforce_account_id`), so relinking cannot raise IntegrityError even
    if two accounts transiently land on the same hotel.
  - The stale-link path is real: `OnboardingService` at
    `onboarding/services/onboarding.py:396-403` re-points an *existing* metadata row
    at the new hotel (`hotel_metadata.canary_hotel = hotel`), while nothing updates
    the account. So metadata legitimately becomes the newer truth.
  - Note the PR/ticket's stated cause ("metadata row is removed on deactivation")
    only matches `DeactivateHotelPlan` when `strip_salesforce_associations=True`
    (`onboarding/plans/deactivate_hotel_plan.py:165-178`) — and that branch deletes
    the `SalesforceHotelAccount` rows too, so it wouldn't leave a stale link. The
    re-point path above is the more likely real cause. Worth confirming with Ramiro
    that the observed sequence matches, since it doesn't change the fix.

  ### Findings

  1. [MEDIUM] 15-char sfdc_id keys silently skip the heal.
     `existing_hotels_by_identifier` is keyed on the raw `metadata.sfdc_id`, but
     `SalesforceHotelMetadata.query_by_ids` deliberately matches BOTH 15- and 18-char
     forms (`internal/models/models.py:217-222`), while
     `SalesforceHotelAccount.salesforce_account_id` is always 18 chars (max_length=18
     + MinLengthValidator(18)). A metadata row stored with a 15-char id produces a
     dict key that never matches → relink silently no-ops for exactly those accounts.
     Pre-existing hole (old fill-empty heal had it too), but this PR is *about*
     making the heal reliable, so it's the natural place to close it. One-line fix:
     key by `add_sf_id_checksum(metadata.sfdc_id)` — idempotent for 18-char input
     (`canary/salesforce_ids.py:221-224`).

  2. [MEDIUM / question] No `is_active` guard on the relink target.
     The PR guards the reverse direction but not this one. If metadata still points
     at a deactivated hotel while the account was correctly pointed at the live
     replacement — e.g. by `_link_created_hotel_to_salesforce_account`
     (`onboarding/services/onboarding_batch.py:1074-1093`) or a manual admin fix —
     the 4-hourly sync now silently reverts the account back to the deactivated
     hotel. That is the reported bug, inverted. Ask: should it skip when the
     metadata hotel is inactive and the currently-linked hotel is active?

  3. [LOW] Heal reach is narrower than "converges within one cycle" implies.
     The 4-hourly path (`onboarding/services/salesforce_onboarding_fields.py:351`)
     only passes account ids for opportunities surviving the region filter. Stale
     accounts whose SF opportunity has since closed are never revisited, so the
     existing bad population won't self-heal. If the reported hotels are in that
     set, a one-time reconciliation over SalesforceHotelAccount vs
     SalesforceHotelMetadata is needed. Worth asking whether the specific hotels
     that triggered the ticket are actually covered.

  4. [MEDIUM — operational, not code] Behaviour change worth broadcasting.
     Manual corrections to `SalesforceHotelAccount.hotel` (Django admin, one-off
     scripts) are now transient — the next sync reverts them unless the metadata is
     also corrected. That's the intended "metadata is source of truth" semantics,
     but the fix location has moved and CS/support tooling folk should know.

  5. [NIT] Redundant `update_search_vector` call. `update_salesforce_account_data`
     runs immediately after and calls `update_search_vector` for every account the SF
     query returns (`salesforce_hotel_account.py:258`), so the new explicit call is
     an extra UPDATE per relinked account on the happy path. Only load-bearing when
     the SF query doesn't return the account. Harmless (relinks are rare), but note
     the new test only passes *because* of it — it stubs
     `patched_query_salesforce.return_value = []`, so it doesn't exercise the
     production path.

  6. [NIT] Test coverage gap. The PR explicitly promises "accounts whose linked
     hotel has no metadata are left untouched", but there's no regression test for
     it — and that's the invariant most likely to be broken by a well-meaning
     follow-up. A three-liner (account→hotel A, metadata row with
     `canary_hotel=None`, assert unchanged) would lock it in.

  7. Good: log event follows the repo `<parent_callable>.<short_message>` dot-path
     convention; info level is right given relinks should be rare (expect a burst on
     the first post-deploy cycle).

  8. Pre-existing, NOT this PR: the whole method is `@transaction.atomic` and calls
     Salesforce inside the transaction, against
     `.claude/rules/backend/django-transactions-and-tasks.md`.

  ### Verification

  - I did NOT run the tests locally — Postgres/Docker aren't running on this machine
    (connection refused on localhost:5433, Docker daemon down). I applied the PR
    files locally to try, then reverted; working tree is clean.
  - CI: all 57 non-skipped checks pass, none failing. `make test-backend` on the
    canary backend ran in subset mode (11 selected test files, including the changed
    one) and reported `162 passed`
    (https://github.com/canary-technologies-corp/canary/actions/runs/31014408341/job/92335348163).
  - No existing reviews or review comments on the PR as of this run.

  ### Suggested next step

  Post items 1–3 as review comments if you agree; item 4 is a Slack/CS note rather
  than a PR comment. Nothing has been sent anywhere yet.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/51809
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #51809: [TOOL-500] Relink Salesforce hotel accounts to current metadata
  hotel'
updated: 2026-08-06 14:17:57.647414
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested by ramironieto (with ldewald). Branch: purring-petroleum. Touches the Salesforce→hotel linkage that StoredHotelAttributes cohorts depend on.
https://github.com/canary-technologies-corp/canary/pull/51809