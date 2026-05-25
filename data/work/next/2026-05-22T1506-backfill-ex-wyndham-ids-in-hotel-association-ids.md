---
area: null
contexts: []
created: 2026-05-22 15:06:39.751009
defer_until: null
due: null
energy: low
id: 2026-05-22T1506-backfill-ex-wyndham-ids-in-hotel-association-ids
order: null
output: |
  ## Agent run 2026-05-25T07:00Z

  **Status of ENT-6028 backfill: not done.**

  ### What shipped
  - PR #45141 (`7ff696bf0f0`, merged 2026-05-14) — `HotelAssociationService.preserve_as_ex`, wired into `DeactivateHotelPlan` via `DeactivateConfig.preserve_removed_associations_as_ex`. All four brand remove providers (Wyndham, BW, IHG Pilot, IHG Messaging) opted in.
  - PR #45142 — migrations adding `EX_WYNDHAM_SITE_ID`, `EX_IHG_INN_CODE`, `EX_BEST_WESTERN_PROPERTY_ID` to `HotelAssociationIdType`.
  - Ticket status: Deployed on 2026-05-14.
  - Net effect: any *future* REMOVE_HOTEL_FROM_PARENT_BRAND run preserves the EX marker. Historical removals (pre-2026-05-14) are still uncovered.

  ### What's still outstanding (this follow-up)
  The backfill script outlined in the ticket — `tmp/repeatable/ex_brand_marker_backfill.py` — was never written. Confirmed by:
  - No file at `backend/canary/tmp/repeatable/ex_brand_marker_backfill.py` (or anywhere matching `ex_brand*` / `ex_wyndham*`).
  - No code references to `EX_WYNDHAM_SITE_ID` outside the model enum, service, and tests.

  ### Recommended next steps (decide which)
  1. **Build the script.** Three independent passes per the ticket spec:
     - Pass A: walk `OnboardingScriptBatch.objects.filter(script_type=REMOVE_HOTEL_FROM_PARENT_BRAND)`; identifier source priority = surviving brand HotelAssociationId → `Hotel.sso_hotel_id` → `SalesforceHotelAccount.account_data.<brand>_site_id`.
     - Pass B: Wyndham TERMINATED CSV (codes 8/9/11) — reuse `tmp/repeatable/wyn/correct_wyndham_portfolio_membership.py` loader.
     - Pass C: `SalesforceHotelAccount` leftovers — cached brand site_id but hotel not in live brand portfolio.
     - Dedup by hotel; pad Wyndham IDs with `fix_numeric_id(min_length=5)`; write via `HotelAssociationService.set_hotel_association`; dry-run by default.
  2. **Validation anchor:** dry-run must report ≥116 ex-Wyndham hotels (canonical terminated count from ENT-5952 investigation). Investigate gaps before applying.
  3. **Apply order:** dry-run on `prod-shell-ro` → spot-check 10 hotels for identifier provenance → apply on `-m rw` shell with explicit user confirmation.
  4. **Smoke after apply:** `Hotel.objects.filter(hotel_association_ids__id_type__in=[WYNDHAM_SITE_ID, EX_WYNDHAM_SITE_ID])` returns active + ex hotels.

  ### Sizing note
  This is not actually a 5-minute task — building and validating the backfill script is more like a half-day. The GTD item is a capture; consider promoting to its own next-action (or a Linear ticket) before doing the work. If you want, I can scaffold the script as the next step in a fresh session.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: backfill ex wyndham ids in hotel association ids
updated: 2026-05-25 11:36:52.875834
waiting_on: null
waiting_since: null
working_on: false
---

ENT-6028 follow up