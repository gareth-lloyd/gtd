---
area: null
contexts: []
created: 2026-07-31 11:18:03.577659
defer_until: null
due: 2026-07-31
energy: medium
id: 2026-07-31T1118-read-andres-s-segmentation-design-see-dms-with-and
order: null
output: |
  ## Agent run 2026-07-31T11:35:00+03:00

  Found and read the design. Andrés shared it in your DM on 2026-07-30
  (https://canarytechnologies.slack.com/archives/D0AANN14E04/p1785426090353449):
  "Segmentation for Wyndham" — Notion, status **REVIEW ME!**
  https://www.notion.so/canarytechnologies/Segmentation-for-Wyndham-3ad81468615180759a4fed4a9d9c7e1b

  ### What it proposes
  Migrate Wyndham (the last v1-segmentation brand) to v2 (`Segment` + `MessageVariant`), in 4 parts:
  1. **Provider**: Wyndham config provider emits `message_specs_with_variants` for ALL messages.
     Only Welcome is segmented (Members prio-1 / Non-Members prio-1 / Default prio-0);
     other messages get a single Default variant. Non-loyalty brands: Default only.
  2. **Migration**: onboarding re-run for conforming hotels (~6.3k US + 128 EU), script for
     the 18 drift hotels. Copies enabled state (1,520 all-off hotels stay off), disables v1
     welcome specs in the same transaction, deletes nothing. Dry-run + verify commands.
  3. **Upsell segmentation**: flip `ROLLOUT_UPSELL_GUEST_SEGMENTATION` for the Wyndham cohort;
     brand admins add `UpsellSegmentRule` rows. Safe: only 1,166 hotels have upsells.
  4. **Pre-populated standard segments** at every hotel via onboarding + `safe_backfill_iterator`.

  Rollout: pilot (Galt House + 4 test) → full-fleet dry-run → US waves 50/500/~5,800 →
  upsell flag → EU → cleanup after 30-day soak. Per-hotel rollback command until cleanup.
  Cohort classification via `sync_wyndham_case_cohorts` (READY_TO_MIGRATE vs 8 exception buckets).

  ### Open questions (owners assigned in doc)
  1. Plan for 50 US + 51 EU live hotels with `rollout_guest_segmentation=False` (Andrés + CS)
  2. WhatsApp variant templates — blocks EU phase only, 92% of EU specs use WhatsApp (Andrés + CC)
  3. Welcome Default-variant content: reuse non-member template or new copy? Needed before US wave 1 (Andrés + Product)
  4. Standard upsell segment set definition — needed before upsell flag flips (Andrés + Product)

  ### My review observations (not posted anywhere — for your review pass)
  - Overall: thorough and well-audited (per-region numbers, drift detection, idempotency,
    copy-don't-enable, single-transaction v1-off/v2-on, no v1 deletes until soak). The error-case
    and monitoring tables are strong.
  - **Invalid-expression behavior is the sharpest edge**: a bad segment expression causes
    NO_MATCH and the send is *skipped entirely* (no Default fallthrough). Doc mitigates via
    fixed expressions + dry-run + metric, but worth asking whether `_pick_variant` should
    fail-open to Default instead — a platform fix that de-risks every brand, not just Wyndham.
  - Open question 3 gates US wave 1 and Q4 gates Phase 3 — both sit with Product; worth
    nudging early so they don't become the critical path.
  - Campaigns dependency: 47 campaigns on 8 hotels keep v1 targeting until CC migrates them —
    those hotels' v1 GuestSegment rows must survive; design handles it (no deletes) but Phase 5
    cleanup must re-check campaigns before deleting GuestSegment rows.
  - Re-evaluation of upcoming/in-house reservations before first sends is listed as a risk
    mitigation but isn't an explicit migration step or command — worth asking where it runs.
  - EU portfolio inconsistency is acknowledged; scoping by portfolio union + per-wave
    reclassification looks right.

  Suggested next action: review the doc in Notion and leave comments (status is REVIEW ME!),
  or reply to Andrés in the DM.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: Read Andres's segmentation design (see DMs with Andres Figueiro)
updated: 2026-07-31 12:47:16.392838
waiting_on: null
waiting_since: null
working_on: false
---