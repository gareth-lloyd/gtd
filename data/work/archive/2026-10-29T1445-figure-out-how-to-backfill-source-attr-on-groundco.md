---
area: null
completed_at: 2026-10-30 16:03:08.790236
contexts: []
created: 2026-10-29 14:45:42.949080
defer_until: null
due: null
energy: low
id: 2026-10-29T1445-figure-out-how-to-backfill-source-attr-on-groundco
order: null
output: |
  ## Agent run 2026-10-30T12:38:24Z

  **Answer: yes, Groundcover has enough to backfill, but only from Sep 30 on, and the data is expiring.** Retention looks like about 31 days: Sep 30 has logs, Sep 29 has none. Oct 1 should age out around Nov 1, and another day goes each day after that. The export needs to happen now, even if the backfill itself runs later.

  ### What Groundcover has
  - The signal is `request_headers.X-Sdk-Version`. It's been logged throughout. `X-Sdk-Platform` and `client_source` only exist from #61883 (merged Oct 29), so they can't be used for the backfill: https://github.com/canary-technologies-corp/canary/pull/61883
  - The version header alone isn't proof of SDK traffic. `global_blue_webhook_handler` also sends it (70 POSTs on Oct 6), so filter by route.
  - The IDs needed for the join are on the rows. `on_flow_completed` has `CTX_check_in_id` and `CTX_reservation_slug`. `request_finished` on session POST has only the reservation slug.
  - The log pipeline config has no drop rule for django logs. I didn't reconcile log counts against the DB, so completeness is unproven.

  Three queries to export (`workload:django env:production`, split into 1-day chunks because 4-8 day windows mostly hit the 30s timeout):
  1. v3 completed: `event:on_flow_completed request_headers.X-Sdk-Version:"*"`
  2. v3 started, including abandoned: `event:request_finished method:POST url_name:guest_experience_sessions_api request_headers.X-Sdk-Version:"*"`. Needed because #61975 stamps at session start, so abandoned sessions count as SDK going forward.
  3. Legacy: `event:request_finished method:POST url_name:check_in_guest_check_in_registration_cards code:200 request_headers.X-Sdk-Version:"*"`

  Volumes (SDK check-ins completed on v3):
  - Oct 4-8: 12
  - Oct 20: 19
  - Oct 20-24: 210
  - Oct 24-30 12:00 UTC: 566
  - Oct 29: 139, plus 24 on the legacy route that same day
  - Other windows timed out, so I have no full total.
  - SDK session POSTs already appear on Sep 30 (6), before the "early Oct" launch. Anything before Sep 30 is not recoverable from Groundcover.

  ### Alternatives
  **1. Flow manifest version on the session row (the best one).** It's durable, needs no logs, and could reach back before Sep 30.
  - SDK 1.x resolves to manifest 1 and web resolves to the newest flow, normally 3 (`guest_experience/versioning.py`, `guest_experience/selectors/flow.py`). The result is stored as `CheckInSession.flow`.
  - In logs, every SDK completion on Oct 20 (19) and every non-manifest-3 completion on Oct 20 (19) and Oct 29 (139) matched. Web on Oct 20 12:00-15:00 UTC was 651 manifest 3, 1 manifest 1.
  - It isn't clean, though: on Oct 6 12:00-18:00 UTC, 1 of 3 manifest-1 completions had no SDK header. Possibly a hotel with no manifest-3 flow; I didn't check.
  - It can't see the legacy route, which has no session row. That was 24 of 163 SDK completions on Oct 29.
  - `start_session` overwrites `flow` on a later POST from another client, so it records the last client to start the session, not the first.
  - Row-level check still needed. CANARY_RAW isn't authorized on this Snowflake role, and I didn't query prod because the repo rules need your explicit OK. Query to run (read-only):
    `select f.manifest_version, c.source, c.analytics_source, count(*) from guest_experience_checkinsession s join guest_experience_flow f on f.id = s.flow_id join check_in_checkin c on c.id = s.check_in_id where s.created_at >= '2026-09-30' group by 1,2,3;`
    Table names are Django defaults I inferred, not confirmed. Then compare manifest < 3 against the Groundcover export.

  **2. `FACT_CHECK_IN.SOURCE is null`: not usable.** Oct 20 had about 4,600 null-source check-ins against 19 SDK completions, so nearly all nulls aren't SDK.

  **3. `datadog_raw.datadog.logs` in Snowflake: not assessed.** It's still loading (15M rows, has `attributes`), but I didn't check whether it holds request headers. Worth a look only if something older than Sep 30 matters.

  **4. IHG/Wyndham app analytics: not checked.** At best these would give aggregate cross-checks, not check-in IDs.

  ### Recommended plan
  1. **Now:** export the three queries to a file, Sep 30 onward. Each day of delay loses a day of data.
  2. Merge #61902 and #61975 so the forward path stops growing the gap. Neither has merged yet: https://github.com/canary-technologies-corp/canary/pull/61902 and https://github.com/canary-technologies-corp/canary/pull/61975
  3. Run the manifest query above to validate, and to decide whether it can cover anything before Sep 30.
  4. Write a management command that takes the exported IDs and sets `source=sdk` and `analytics_source=sdk`, the same as `apply_client_attribution`. Report how many rows already had a non-null source, because this overwrites them, as the forward path does.
  5. Confirm the rows reach `FACT_CHECK_IN`. #61975 assumes Airbyte picks up the change; I didn't verify the sync mode. If it relies on `updated_at`, a plain `.update()` won't bump that, so set it explicitly.

  Check-outs (#61985) and upsells (#62000) have the same gap, and the manifest shortcut doesn't help with check-outs. If they need backfilling too, add `check_out_guest_view` and `check_in_guest_check_in_purchase_order` to the export now. I didn't validate those routes beyond seeing them in the SDK traffic list.

  ### Not verified
  - Exact launch date. I couldn't read the SDK observability plan (https://claude.ai/artifact/D4SpuUtxtCiNo22yE6u1H4): artifact not found on this account. Diana Perez owns the work under MOB-1424: https://linear.app/canary-technologies/issue/MOB-1424
  - Retention is inferred from where the logs stop, not from a config. Only us-west-2 was checked for region: all 230 SDK session POSTs on Oct 29 were there.

  Nothing was exported or written to any system. Reads only: Groundcover, Snowflake, GitHub, Linear, Slack.

  ## Agent run 2026-10-30T13:05:26Z

  **Export done, at your request.** It covers Sep 30 to about 12:44 UTC on Oct 30, all prod regions. Files are local and gitignored, in `/Users/garethlloyd/projects/canary/backend/canary/tmp/data/sdk_source_backfill/`:
  - `v3_completed.csv`: 1,071 rows
  - `v3_session_post.csv`: 1,930 rows (1,818 with code 200, 108 with 404, 4 with 500)
  - `legacy_registration_card.csv`: 814 rows, all code 200
  - `reservations_union.csv`: 2,584 reservations, one row each, successful requests only, with a flag for `staging-` hotels

  Rows were extracted by script from the raw tool results, not retyped. Successful windows cover the whole period with no gaps, and no window hit the 5,000-row limit.

  **Correction to the run above:** legacy is much bigger than Oct 29 suggested. Over the full window it's 813 reservations against 1,071 v3 completed, about 43% of completions, not the 15% seen on Oct 29. Legacy peaked mid-October and has been falling. The manifest signal can't see any of these, so it can't replace the export. It's a cross-check for v3 only.

  **What's in the union file:**
  - 2,488 reservations are at `ihg-*` or `wyndham-*` hotels: 2,221 Wyndham and 267 IHG. Of those, 1,814 completed and 674 only started.
  - The 701 started-only reservations (674 at those hotels) have no check-in ID, because that log row doesn't carry one. Resolve them by reservation slug.
  - The other 96 are test traffic by name: 92 `staging-*`, plus `canary-*` and `vibhors-*`. Exclude them.
  - `ihg-atlmu` has 105 reservations, by far the most of any hotel, and may be a test property. Unconfirmed. Check it before including it.
  - SNAPSHOT builds appear in a few rows (11 session POSTs, 4 completions), which also suggests test traffic. One session POST has version `3`.
  - 7 rows are in eu-central-1, so the backfill has to run there as well as in the US.

  **Header check:** on Oct 30, all 15 legacy POSTs and all 111 session POSTs with `X-Sdk-Version` also had `X-Sdk-Platform` and `client_source:sdk`. That's one day, on these routes only. Platform (iOS/Android) isn't available before Oct 29.

  **Still to do:**
  - The gap keeps growing until #61975 is deployed, so run a top-up export for Oct 30 12:44 UTC onward before the backfill.
  - The export isn't validated against the DB yet.
  - Check-out and upsell routes were not exported.

  **Linear draft (not created):** `/Users/garethlloyd/projects/plans/mob-sdk-source-backfill-linear-draft.md`. Proposed as a sub-issue of MOB-1325, whose requirement 5 already asks for this backfill: https://linear.app/canary-technologies/issue/MOB-1325

  ## Agent run 2026-10-30T13:41:28Z

  Validated the export against `ANALYTICS_PUBLIC.FACT_CHECK_IN`, excluding test-named hotels. Per-check-in results: `backend/canary/tmp/data/sdk_source_backfill/validation_fact_check_in.csv`.

  - **v3 completed (1,018):** all found. 1,014 have `submitted_at`, all within 5 minutes of the log. 1,017 have null source.
  - **Legacy (798):** all found. 795 have the registration card submitted, but only 601 have `submitted_at`. So a legacy POST means the card was submitted, not that the check-in was completed. 797 have null source; 795 have `analytics_source = direct`.
  - **Started-only (674):** 669 resolve by slug. 641 have null source, **27 have source `kiosk`** and 1 has `sms`. 96 have `submitted_at` with no completion in the logs; cause unknown.
  - **Corrected completed count:** 1,615 reached `submitted_at` (1,014 v3 + 601 legacy), not 1,814.
  - **Overwrite decision changed:** only set `source = sdk` where source is null. Overwriting would relabel the 27 kiosk check-ins.
  - **User-agent check:** all 62 legacy POSTs in three 6-hour samples (Oct 9, 16, 22) have Wyndham or IHG app user agents. The Oct 9 jump is `WyndhamRewards/5508` on SDK 1.4.1, so it looks like an app rollout. Rollout itself unconfirmed.
  - **EU:** the 2 EU legacy rows also matched by ID in the US table, so those matches may be ID collisions. EU needs its own check.
  - **Log completeness:** still open. `CheckInSession` isn't in Snowflake, so a read-only shell script covers it. Log counts to compare (us-west-2): `on_flow_completed` 393 on Oct 6 12:00-15:00 UTC and 631 on Oct 20 12:00-15:00 UTC; session POST 200s on Oct 20 12:00-13:00 UTC are 355 across 286 reservations.

  ## Agent run 2026-10-30T13:47:25Z

  Compared the shell output with the export. Saved as `session_low_manifest.csv` and `session_low_manifest_not_in_export.csv` in the same folder.

  - **Log completeness:** `on_flow_completed` matches `CheckInSession.completed_at` exactly: 393 of 393 (Oct 6) and 631 of 631 (Oct 20). 192 sessions were created in the hour with 286 reservations POSTing, which fits because POSTs also hit existing sessions.
  - **Row level:** 1,475 of 1,491 manifest-1 sessions at non-test IHG and Wyndham hotels are in the export. The other 16 (8 completed, 8 not) have no timestamps in the shell output, so some may be after the 12:44 UTC cutoff.
  - **Manifest false positives:** 92 manifest-1 sessions at `bowie-house` have no SDK header in the logs. Cause unknown. This is why manifest alone can't drive the backfill.
  - **96 started-only with `submitted_at`, mostly explained:** 27 have source `kiosk`, 63 moved off manifest 1, 6 unexplained. Moving off manifest 1 implies a later non-SDK POST (`start_session` overwrites the flow), so those 63 look like started in the app and finished elsewhere. Inferred from code and counts, not observed per guest.
  - **58 log-completed sessions now off manifest 1:** all 58 have `submitted_at`, and 57 have null source. Likely reopened on web after finishing in the app. They stay in the backfill, because the logs show the SDK completion.
  - **Proposed population:** about 2,300 null-source check-ins: 1,017 v3, 797 legacy and 487 started-only still on manifest 1. Before any `ihg-atlmu` exclusion. Exact count comes from the command's dry run.
  - **Conflict to resolve:** #61975 stamps `sdk` at session start, so app-started, web-finished check-ins would be labelled SDK going forward. MOB-1325 defines SDK as submitted through the SDK.

  Ticket draft updated. Still not created.

  ## Agent run 2026-10-30T13:51:40Z

  Created MOB-1441 in Triage at your request, with six CSVs attached: https://linear.app/canary-technologies/issue/MOB-1441/backfill-source-sdk-on-historical-sdk-check-ins-from-groundcover

  It's a sub-issue of MOB-1325, related to MOB-1424, in the SDK Observability project, priority High, unassigned. Nothing has been written to prod. The backfill itself is still to do.
project: null
source_id: null
tags: []
time_minutes: 5
title: figure out how to backfill source attr on groundcover -> snowflake mobile analytics
updated: 2026-10-30 16:03:08.790227
waiting_on: null
waiting_since: null
working_on: false
---

Diana Perez has done some recent work to track check-in origin (app/web) using the source attribute. This will feed through to snowflake. 

WE need to backfill from app launch in early oct. Does Groundcover give us enough informatino to do this? 

If not, alternatives?