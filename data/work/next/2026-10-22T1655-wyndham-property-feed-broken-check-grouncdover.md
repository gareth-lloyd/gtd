---
area: null
completed_at: null
contexts: []
created: 2026-10-22 16:55:37.271552
defer_until: null
due: null
energy: low
id: 2026-10-22T1655-wyndham-property-feed-broken-check-grouncdover
order: null
output: |
  ## Agent run 2026-10-22T17:10

  **Yes, the feed is broken. It crashes every day before it saves anything, so no Wyndham property data has been applied since Sept 16.**

  Groundcover, workload `c-wyndham-properties-update` (prod-main-us-west-2, cron `0 10 * * *` UTC):
  - **Today, 2026-10-22 10:01 UTC:** `_csv.Error: new-line character seen in unquoted field`. It fails in `create_missing_batches` -> `BatchUpdateRunService.create_batch_update_run` -> `extract_external_hotel_ids` -> `WyndhamBatchReceiver.hotel_identifiers_from_input_file` (`csv.DictReader` over `StringIO(contents)`). Sentry id 68dc7ae52eec4be28a8a6e822efe186f, version v2026.37.114.
  - **2026-10-08:** same csv error.
  - **2026-10-15:** a different failure: paramiko `EOFError` during the SFTP `transport.connect` in `get_batch` (Sentry 7e407155a03749e49e34853d907230fb). It looks transient, but `get_batch` only catches `SFTPConnectionError`, so the whole run dies.
  - Groundcover keeps about 3 weeks of logs: Sept 16/17 and Oct 1 come back empty. The Sept 16 start date comes from Andrés, not from me.

  **Root cause (Andrés found it, the logs match):** site 58694 has a stray `\r` in the GM first name. A bare CR in an unquoted field makes the csv module raise, and one bad row kills the whole file. The crash happens before a `BatchUpdateRun` row is created, so nothing shows in the DB or the admin either. It fails quietly apart from Sentry.

  **Thread:** Andrés asked you in #epd-enterprise-engineers (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1792677192562349). You said "yes". His open question to you: **is the job still meant to auto-create Cut Parent Ties batches?** He also says the #wyndham "batch created" Slack alert has never posted, and Ani didn't know about the batches.

  **Ticket context:** ENT-7941 (https://linear.app/canary-technologies/issue/ENT-7941/wyndham-cut-parent-ties-scripts-are-getting-auto-created) is Deployed. The fix, PR #60813 (https://github.com/canary-technologies-corp/canary/pull/60813), holds each hotel until SFDC shows Property Opted Out. It does nothing until the feed parses again. 131 stale batched hotels are still waiting on Jessica's run-or-cancel decision.

  **Suggested fix (not written):**
  1. Make the parse tolerant. Normalise bare `\r` (e.g. `re.sub(r"\r(?!\n)", " ", contents)`) before `csv.DictReader` in `WyndhamBatchReceiver` (`onboarding/services/vendor/wyndham_properties_batch_update_service.py`, `generate_update_rows` / `hotel_identifiers_from_input_file`), or catch `csv.Error` per row and skip it with a warning. One bad Wyndham row should not block every hotel.
  2. Catch `EOFError` / `paramiko.SSHException` in `get_batch` the same way as `SFTPConnectionError`.
  3. Add a Groundcover monitor on `cron_wyndham_properties_update.failed` (`/infra:monitors`) so a silent month can't happen again.
  4. The next run after the fix will apply about 5 weeks of changes at once, including any status-11 cut-parent batching. With #60813 merged, only SFDC-opted-out hotels get batched.

  **Draft Slack reply to Andrés (NOT sent):**
  > Yes, still intended. Wyndham's status 11 is the trigger, and your #60813 gating on SFDC Opted Out is the right shape. Confirmed the crash in Groundcover: same `_csv.Error` today and Oct 8 (plus an SFTP EOFError on Oct 15). Can you make the parser tolerate the stray CR (normalise bare `\r` / skip bad rows) and catch SFTP EOF in `get_batch`? Worth a failure monitor too.

  Edit the "still intended" part if you think otherwise. That's your call.
project: 2026-08-31-ihg
source_id: null
tags: []
time_minutes: 5
title: wyndham property feed broken? check grouncdover
updated: 2026-10-22 17:10:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-7941/wyndham-cut-parent-ties-scripts-are-getting-auto-created

comment says hasn't run since sept 16th