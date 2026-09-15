---
area: null
completed_at: null
contexts: []
created: 2026-09-01 14:51:58.920317
defer_until: null
due: 2026-09-14
energy: low
id: 2026-09-01T1451-plan-discussion-for-blake-directs-gdpr-retention-p
order: null
output: |
  ## Blake directs — GDPR retention: impact, comms, rollout (~20 min)
  Condensed 2026-09-14 from Slack, Notion, code, Granola EMEA meetings (Aug 10–Sep 14) and the Sep 9 weekly GDPR sync.

  ### Context (read-ahead)
  - **Scope, phase 1:** check-in/checkout in Canary and guest data in the PMS Gateway. In code these are two separate sweeps with separate retention values and no sync between them. ID document OCR fields are in. Audit logs and messages are out; the activity log is hidden per redacted record.
  - **No blanket default (Sep 3):** only countries on the vetted list get deleted. Where domestic and foreign-guest rules differ, the longer one applies (e.g. DE 455d, FR 180d, IT 0d). The countdown starts the day after checkout.
  - **Status:** end-to-end tests on Sep 4 were in a "very good state"; DSAR is ready; Marta's country-retention PR is up; a GrowthBook flag is being added to the Gateway. On master as of Sep 14: no country map, no feature flag on the Canary sweep, no day-after-checkout buffer, and no scheduler entry for the sweep in this repo.
  - **Deadline:** "mid–end September" is an internal target from Aug 13 block planning, not a legal deadline.

  ### 1. Impact (6 min) — verified against code 2026-09-14
  - Redaction is irreversible: text fields are overwritten with `__redacted__<hex>` tokens and ID scans are hard-deleted from S3. Admin values are bounded to 1–1827 days; there is no country floor.
  - Staff lose search by guest name, email and phone. The record itself shows the token where the name was. The only explanation text is the activity-log modal's "anonymized" message (EMEA-361); nothing else explains it.
  - Exports leak the tokens: check-in CSV reports and reg-card PDFs print `__redacted__…`.
  - Redacted check-ins stop syncing with the PMS: room/status updates and upsells stop for those stays.
  - Not erased: primary guest name/email/phone on the Reservation and Guest rows, messaging threads, amenities, add-ons, auth forms, contracts. "Deleted after N days" is not true yet.
  - ID images run on a separate 181-day clock (`id_retention_days`, images only). The GDPR sweep clears OCR fields but not check-in ID images or signatures. Immediate purge at OCR exists today and IHG UK/DE/ES already use it.
  - First run walks each hotel's full history. It is batched (1000-row pages, 10 hotels in parallel, per-row isolation, dry-run by default) but there is no per-hotel selector: a pilot is controlled only by which hotels have a retention value set.
  - Known gaps:
    - PMS-9787 fix (Gateway obfuscation lock) exists but sits behind an in-house rollout defaulting to 0%; Gateway re-syncs also create duplicate ghost guest rows.
    - Both sweeps compute the cutoff in UTC from `departure_date`; deletion happens exactly N days after departure, no extra buffer day.

  ### 2. Comms (5 min)
  - Sep 3 chose to roll out without telling customers: the terms of service and ROPA cover it, the UI shows the retention periods, and changes go through the CSM in writing. Is that acceptable given the data loss? Proposal: give strategic accounts (IHG, Marriott, Wyndham EU) advance notice, and require the EMEA-636 explanation UI before go-live.
  - Owners needed:
    - CS talk track for ID-purge changes
    - GDPR FAQ for CS & Sales
    - Snowflake audit of hotels not on immediate ID purge
  - Don't claim "deleted after N days" while copies remain in Snowflake, Kiosk Workbench (Vercel/Supabase) and Birdbrain.

  ### 3. Rollout (5 min)
  - **Country values:** Sebastian is reconciling sources that conflict. Approvers are Gareth and Blake. Does legal (Alex) review too?
  - **Sequence:**
    1. Test on generated data.
    2. Daytime per-hotel pilots run by command.
    3. Country or batch waves behind the GrowthBook flag.
  - **Gates:**
    - EMEA-636 explanation UI
    - A position on PMS-9787
    - The day-after-checkout buffer shipped
    - A named kill-switch owner
  - **Existing hotels:** Gareth owes the approach for moving them onto the right values.
  - **End of September:** is it firm given IHG onboarding, HotelKit, Yauheni's reassignment and Marta's holiday?

  ### 4. PII in unapproved tools (4 min)
  - Blake likely doesn't know yet (he was on vacation Sep 9).
  - Kiosk Workbench copies production PII to Vercel/Supabase; Birdbrain runs on Cloudflare. Neither was in the June audit, and both are outside SOC 2 and the sub-processor list.
  - Asks:
    - An owner and date for moving Workbench.
    - Back Bernard's all-hands talk and a lightweight security review for new tools.

  ### 5. Rollout plan vs code (code review 2026-09-14)
  - **Verdict:** the plan is sound on paper, but master can't execute it yet. Wave mechanics live in three open PRs behind a hardcoded `False` switch.
  - **Coding:** Marta's stack adds a shared country map (#56133) with resolvers in Canary (#56281) and the Gateway (#56135), resolved at read time; `pii_retention_days` becomes override-only. Both resolvers are gated by `is_country_retention_enabled`, which returns `False` today. The GrowthBook flag is designed, not written.
  - **Canary sweep today:** opt-in by non-null `pii_retention_days`, 10 threads, 1000-row pages, idempotent via `obfuscated_at`, irreversible on `--commit`. Covers check-in, checkout, kiosk, ID docs, blobs. No adapter for messages, auth forms or audit logs.
  - **Gateway today:** its own `ObfuscationPolicy` per account, set in admin. The PMS-9787 re-sync guard is merged but behind a `FeatureRollout` flag that fails open.
  - **Execution per Notion plan (draft, no dates):** dry-run, staging with 3 seeded hotels, Canary test hotel 7 nights, one low-volume customer 14 nights with legal and customer sign-off, then waves. Kill switch is "disable the CronJob".
  - **Reality:** the Canary sweep has no CronJob, beat or cron entry. It is manual, dry-run by default, with no `--hotel`, limit or cutoff args. A pilot means setting one hotel's value and sweeping every configured hotel.
  - **Gaps to raise:**
    - No per-hotel targeting and no kill switch on the Canary side.
    - No buffer day. Canary uses `departure_date <= today - N`; the Gateway is inclusive, so the two erase on different days.
    - Demo hotels aren't filtered; no opt-out (`pii_purge_strategy=none` is in the plan, not the code).
    - Two independent retention configs (Canary column vs Gateway policy) with no sync.
    - EMEA-636 explanation UI and EMEA-601 alerting not started.

  ### Decisions to leave with
  1. Approve the country list, and name who signs off.
  2. Tell customers or not, and who owns comms.
  3. Go-live gates and pilot hotels.
  4. Is end of September firm, or does it slip?
  5. ID purge at OCR vs customers keeping reg cards and IDs.
  6. Owner and date for moving Workbench.

  ### Links
  - Slack defaults thread: https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1787299618453699
  - Buffer thread: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1788968522010779
  - Retention sheet: https://docs.google.com/spreadsheets/d/1oItyp7d5keDcJjis1onPo0GmcjGbUEj3173Hqpr7A1A/edit
  - Design doc: https://app.notion.com/p/3ce8146861518059934ec78cf2f98777
  - Rollout plan: https://app.notion.com/p/3ba81468615181a9bb85c7e645ca97af
  - EMEA-636: https://linear.app/canary-technologies/issue/EMEA-636/gdpr-hotel-dashboard-ui-check-in

  ### Code review notes (2026-09-14, master 3bfef07c7d2, read-only)
  Claim → verdict, with pointers.
  - Null retention skips the hotel → TRUE (`gdpr/management/commands/obfuscate_scheduled_sweep.py:49`).
  - Irreversible → TRUE (`shared/gdpr/models/overwrite.py:79-93`, blobs deleted on commit in `gdpr/services/executor.py:41`). No restore path.
  - Admin overrides unvalidated → FALSE. Min 1, max 1827 (`hotels/models/hotel.py:966-971`). Scripts using `update()` bypass it.
  - Day-after-checkout buffer → NOT ON MASTER. Cutoff is `today - retention_days`, inclusive, on `departure_date` (sweep `:76`, `check_in_obfuscation.py:45`).
  - UTC → TRUE in Canary (`sweep:41`) and Gateway (`scheduled_obfuscation_service.py:135`).
  - Country map, GrowthBook flag on Canary sweep → NOT ON MASTER. Gateway gate is its own `FeatureRollout` keyed by account uuid, `gdpr.enforce_obfuscation_lock`, default 0%.
  - Shared Canary/Gateway window → FALSE. Gateway uses `ObfuscationPolicy` per Account, set in Django admin; no code pushes Canary's value across.
  - PMS-9787 → PARTIAL. Lock via `obfuscated_at` in `pms-gateway/gdpr/lock/gate.py:63-81`, only when the rollout is on. One-time re-obfuscate and ghost-purge commands exist, which confirms it happened.
  - Name search breaks → TRUE, Postgres FTS vector rebuilt without guest terms (`check_in/services/check_in_search.py:24-37`). No stale external index.
  - Activity log hidden → TRUE per record (`guest/views/reservation_audit_logs.py:76-83`).
  - Retention visible to staff in the UI → FALSE. Django admin only.
  - Kill switch → Canary: none beyond clearing `pii_retention_days`. Gateway: `ObfuscationPolicy.is_active`.
  - Failure handling → run continues; failed rows retried next run; S3 delete failures only logged (orphans).
  - Scheduler → daily cron in canary-kubernetes, all regions, deployed Aug 25 (EMEA-592, canary-kubernetes PR 4824). Not in this repo.
  - Buffer day → not a ticket of its own. Agreed in the Sep 8 Slack thread; implemented in PR 56281 (Canary, `departure_date < cutoff`) and PR 56135 (Gateway, `check_out >= cutoff`), both In Review 2026-09-14. Local-time sweep is untracked.
project: 2026-07-20-gdpr
source_id: null
tags: []
time_minutes: 5
title: 'Plan discussion for Blake directs: GDPR retention policies and implications'
updated: 2026-09-14 15:31:40
waiting_on: null
waiting_since: null
working_on: true
---

Impact will be huge, and it's happening before end of September

https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1787299618453699

 Proposed defaults: 30d after checkout for check-in info, 30d for messages, 5y activity logs, 6y user consent. Configurable per hotel in django admin already; question is the defaults. Sudarshan has signed off from the messaging side.

https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1787306070419209?thread_ts=1787299618.453699&cid=C0B3EUYPRL4

Promoted from the 2026-09-10 awareness report (Slack highlights).
https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1788968522010779

Discussion points: 
* Rollout
* comms
* impact (immediatley changes behavior for clients)