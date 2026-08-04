---
area: null
completed_at: 2026-08-04 15:09:38.366015
contexts:
- react
created: 2026-08-03 10:06:38.148192
defer_until: null
due: null
energy: low
id: 2026-08-03T1006-review-pr-51430-tool-396-drop-cohorthotel-onboardi
order: null
output: |
  ## Agent run 2026-08-03T10:18:50Z

  Reviewed locally. Nothing posted to GitHub.

  **PR:** https://github.com/canary-technologies-corp/canary/pull/51430 (ramironieto,
  branch `rnieto/tool-396-drop-cohorthotel-onboarding-type`, +22/-12)
  **Ticket:** TOOL-396 https://linear.app/canary-technologies/issue/TOOL-396/delete-the-onboarding-type-field-on-cohorthotel

  **Verdict: the change itself is correct, but it cannot merge as-is — needs a rebase.
  Recommend: comment asking for rebase, then approve.**

  ### BLOCKER — migration number collision with master

  The branch adds `onboarding/0161_remove_cohorthotel_onboarding_type.py` depending on
  `0160`. Master already has `onboarding/0161_alter_cohort_onboarding_type_and_more.py`,
  also depending on `0160` — it landed 2026-07-29 in 75ef9b703bb
  ("Migrations: WYNDHAM_CALL_CENTER_BOOKING onboarding type", PR #49000,
  https://github.com/canary-technologies-corp/canary/pull/49000), i.e. after this branch
  was cut. `75ef9b703bb` is not an ancestor of the branch; the branch is 457 commits
  behind master (merge base b7601d268be).

  Verified by materialising the merge tree (`git merge-tree --write-tree`): both 0161
  files coexist, both with `dependencies = [('onboarding', '0160_...')]`. That is two
  leaf nodes in the `onboarding` graph — `makemigrations --check` and `migrate` will
  both fail with "Conflicting migrations detected". GitHub reports `MERGEABLE` because
  there is no *textual* conflict, which is why this is invisible on the PR page, and
  the PR's own "makemigrations --check: no changes detected" evidence is now stale.

  Fix: rebase on master, `make makemigrations` again → `0162_remove_cohorthotel_onboarding_type`
  depending on `0161_alter_cohort_onboarding_type_and_more`. Nothing else in the diff
  should change. (Master's 0161 re-alters `cohorthotel.onboarding_type` choices; a
  RemoveField after it is fine.)

  ### Everything else checks out

  - Migration shape matches the documented two-PR drop-column flow
    (`docs/django/backwards-compatible-migrations.md`) and existing precedent —
    identical to `authorization/0362_remove_authorizationconfiguration_has_sales_agent.py`:
    `IgnoreMigrationLintRules(codes=["DROP_COLUMN"])` first in `operations`, then `RemoveField`.
  - Deprecation step is genuinely done: #50169 wrapped the field in `deprecate_field()`
    and reached prod 2026-07-27, so the ORM has not selected the column since. The
    deployment-window crash risk the doc warns about does not apply.
  - Grepped backend + frontend for every `onboarding_type` reference: zero remaining
    reads/writes of `CohortHotel.onboarding_type`. All surviving hits belong to
    `Cohort`, `OnboardingScriptBatch` or `SalesforceOpportunity`, which are different
    models and untouched. No ORM lookups (`cohort_hotel__onboarding_type` etc.), no admin
    config, no raw SQL.
  - `stub_cohort_hotel` in `onboarding/testing.py` still takes an `onboarding_type` kwarg
    but no longer writes it to the row — so the ~40 call sites don't break. Slightly
    misleading signature, but out of scope for this PR.
  - Import cleanup (`deprecate_field`, `OnboardingType` from `onboarding.models.cohort`)
    is correct — on current master those are used only by the field being deleted.
  - CI green on the 2026-07-30 run (make test-backend, linters, E2E). Note the
    "Django Migrations Linters && Run Migrations" jobs show as *skipping*, so CI would
    not have caught the collision above even on a fresh run.

  ### The author's merge gate is real, and bigger than the PR body implies

  The PR says: dropping the column erases `onboarding_type` for earmark rows whose
  `cohort` is null, and those should be deleted or adopted first. Nobody has answered
  this on the PR — it is probably why it's been sitting since 07-30.

  Queried prod (read-only, Snowflake `ANALYTICS.ANALYTICS.ONBOARDING_COHORTHOTEL_MERGED`,
  CDC deduped per id, deleted rows excluded, last sync 2026-07-31):

  - 43,975 live CohortHotel rows total; **7,437 have `cohort_id IS NULL` and a non-null
    `onboarding_type`** — i.e. every cohort-less row carries one. Not a handful of strays.
  - Breakdown: wyndham_tipping 4,208 · wyndham_ai_voice 1,719 · wyndham_msa 518 ·
    wyndham_connect_plus 470 · ihg_pilot 326 · best_western_msa 195 · default 1
  - Created 2025-03-28 → **2026-04-23** (nothing newer — confirms the write path died
    with #50165). 1,305 created in 2026. 1,613 have no `hotel_id`. None updated since
    June 2026.
  - The 326 `ihg_pilot` rows (all hotel-less, created Feb–Mar 2026) are the ones I'd
    want a second opinion on given ENT-6032 IHG pilot work is live.

  **Question for rami/abrad before merge:** does anyone still need to know what those
  7,437 rows were earmarked for? If yes, snapshot the column somewhere (or adopt them
  into cohorts) first. If they're dead weight, say so on the PR and merge.

  ### Minor — data-warehouse deprecation process not acknowledged

  The canary linter bot warned `warn_on_column_deprecation` on this PR, pointing at
  https://www.notion.so/canarytechnologies/23-33-Deprecate-Fields-in-Data-Warehouse-15a814686151802dbc5ddbb8bc384a0a
  — nobody responded. I checked Snowflake myself: no views in `ANALYTICS` or `CANARY_RAW`
  reference `ONBOARDING_COHORTHOTEL`, so the blast radius looks limited to the raw synced
  table losing a column. Worth a one-line "checked, no downstream consumers" on the PR
  rather than silently ignoring the bot.

  ### Draft comment (NOT posted — say the word and I'll send it)

  > Change itself looks right — matches the two-PR drop-column flow, deprecate step is
  > deployed, and I confirmed there are no remaining references to
  > `CohortHotel.onboarding_type` anywhere in backend or frontend.
  >
  > One blocker though: needs a rebase. #49000 landed
  > `onboarding/0161_alter_cohort_onboarding_type_and_more` on 07-29, so there are now two
  > `0161`s in the app, both depending on `0160`. Git merges cleanly so GitHub still says
  > mergeable, but Django will refuse with "Conflicting migrations detected". Rebase and
  > regenerate → `0162` depending on `0161`.
  >
  > On the merge gate: I checked prod — it's 7,437 rows with a null cohort and a non-null
  > `onboarding_type` (4,208 wyndham_tipping, 1,719 wyndham_ai_voice, 326 ihg_pilot, …),
  > created between Mar 2025 and Apr 2026, none touched since June. Do we care about
  > preserving what those were earmarked for, or are they dead weight? Happy to approve
  > once that's settled and the rebase is in.
  >
  > Also, the `warn_on_column_deprecation` bot warning is unanswered — FWIW I found no
  > Snowflake views referencing `ONBOARDING_COHORTHOTEL`, so it looks safe, but worth
  > noting on the PR.

  ### Files inspected

  - `backend/canary/onboarding/migrations/0161_remove_cohorthotel_onboarding_type.py` (PR)
  - `backend/canary/onboarding/migrations/0160_...`, `0161_alter_cohort_onboarding_type_and_more.py` (master)
  - `backend/canary/onboarding/models/cohort_hotel.py`
  - `backend/canary/onboarding/testing.py`
  - `docs/django/backwards-compatible-migrations.md`
  - `backend/canary/authorization/migrations/0362_...` (precedent)

  ## Agent run 2026-08-04T14:47:00Z

  Re-verification only — nothing has changed since the 08-03 review, so all findings
  and the recommendation stand. Nothing posted anywhere.

  Checked:
  - PR https://github.com/canary-technologies-corp/canary/pull/51430 is untouched:
    still OPEN / REVIEW_REQUIRED, same single commit `6e33da4ad76` (2026-07-27), zero
    human reviews or comments — only the bot comments already covered (linear-linkback,
    canary-linter `warn_on_column_deprecation`, migration-SQL, E2E-pass, and Macroscope,
    which independently flags "Needs human review" because drop-column migrations are
    on its hard deny-list). No rebase has happened.
  - Fetched fresh `origin/master`: latest onboarding migration is still
    `0161_alter_cohort_onboarding_type_and_more` — nobody has taken `0162`, so the
    migration-number collision blocker and the "rebase → regenerate as 0162" fix are
    still exactly right.
  - Linear TOOL-396
    (https://linear.app/canary-technologies/issue/TOOL-396/delete-the-onboarding-type-field-on-cohorthotel)
    has zero comments — the 7,437-row merge-gate question remains unanswered there too.

  Still blocked on you: the draft comment in the 08-03 run above is ready to post to
  the PR (asks for the rebase + poses the earmark-rows question). Say the word and I'll
  send it; alternatively raise it with rami/abrad directly. The PR cannot merge until
  the rebase happens regardless.
project: 2026-04-16T1210-unblock-team
source_id: https://github.com/canary-technologies-corp/canary/pull/51430
tags:
- morning-gtd
- github
time_minutes: 15
title: 'Review PR #51430: [TOOL-396] Drop CohortHotel.onboarding_type column'
updated: 2026-08-04 15:09:38.366008
waiting_on: null
waiting_since: null
working_on: false
---

Personally requested (rami, with abrad). Final phase of TOOL-396, +22/-12, still REVIEW_REQUIRED since 2026-07-30.
https://github.com/canary-technologies-corp/canary/pull/51430