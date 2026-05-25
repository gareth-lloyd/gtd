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

  ## Agent run 2026-05-25T07:30Z (follow-up)

  Wrote the backfill script: `backend/canary/tmp/repeatable/ex_brand_marker_backfill.py`.

  ### What it does
  Three passes per brand (Wyndham / IHG / Best Western), deduped by hotel:
  - **Pass A** — `OnboardingScriptBatch(script_type=REMOVE_HOTEL_FROM_PARENT_BRAND)` × brand via `limit_to_parent_brand`, joined to `OnboardingScriptHotel` for hotel ids. Identifier chain: live `HotelAssociationId` → `Hotel.sso_hotel_id` (only when SSO org slug matches brand) → `SHA.account_data.<brand>_site_id`.
  - **Pass B** — Wyndham only. Latest completed `BatchUpdateRun(WYNDHAM_PROPERTIES)`, rows in `WyndhamUpdateRow.STATUSES_TERMINATED` (8/9/11), matched to Canary hotels with `sso_organization__slug=wyndham`. Padded wid via `fix_numeric_id(min_length=5)`.
  - **Pass C** — Wyndham only (today). Hotels with cached `account_data.wyndham_site_id` whose hotel is not in any live Wyndham portfolio.

  Skips hotels that already have the live brand id row (still in-brand) or already have the EX row (idempotent). Dedup ranks Pass A > B > C (real REMOVE evidence beats heuristic).

  ### Public API (paste into shell-plus)

      from tmp.repeatable import ex_brand_marker_backfill as bf

      bf.audit()                          # all brands, no writes; prints anchor check
      bf.audit(brand="wyndham")
      bf.sample("wyndham", n=10)          # spot-check identifier provenance
      bf.apply(brand="wyndham", apply=False)   # dry-run preview
      bf.apply(brand="wyndham", apply=True)    # writes EX rows
      bf.verify("wyndham")                # post-apply consumer-side smoke

  ### Guardrails
  - **Wyndham anchor:** `apply()` refuses to write if dedup count < 116 (`WYNDHAM_MIN_ANCHOR`).
  - **Dry-run default:** must pass `apply=True` explicitly.
  - **Idempotent:** hotels already EX-marked are skipped up-front.

  ### Validation
  - `direnv exec . pyright tmp/repeatable/ex_brand_marker_backfill.py` → 0 errors
  - `direnv exec . ruff check tmp/repeatable/ex_brand_marker_backfill.py` → clean
  - `ruff format` applied

  ### IHG / BW caveats
  - `SalesforceHotelAccount.account_data` has no `ihg_inn_code` / `bw_property_id` attributes → Pass C is Wyndham-only.
  - No daily-CSV equivalent for IHG/BW → Pass B is Wyndham-only.
  - IHG/BW therefore rely on Pass A. Legacy REMOVE batches without `limit_to_parent_brand` won't be picked up — expect IHG/BW counts to be much smaller than Wyndham.

  ### Suggested next steps for you
  1. `prod-shell-ro`: `bf.audit()` — confirm Wyndham anchor met, sanity-check IHG/BW counts.
  2. `bf.sample("wyndham", n=10)` — verify identifier provenance on a handful.
  3. `prod-shell -m rw` with explicit user-confirmed approval: `bf.apply(brand="wyndham", apply=True)`. Then `bf.verify("wyndham")`.
  4. Repeat for IHG and BW once Wyndham is signed off.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: backfill ex wyndham ids in hotel association ids
updated: 2026-05-25 07:30:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

ENT-6028 follow up