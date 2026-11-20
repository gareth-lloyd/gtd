---
area: null
completed_at: 2026-11-20 13:39:34.050456
contexts: []
created: 2026-11-20 08:17:33.186941
defer_until: null
due: null
energy: null
id: 2026-11-20T0817-make-these-changes-to-tickets-close-out-ent-8222-e
order: null
output: |
  ## Agent run 2026-11-20T13:40

  Three of the four tickets are changed in Linear, each approved by you in session. ENT-5697 is untouched (you chose "Leave it"), and the Best Western list is not exported or sent.

  ### Done
  - ENT-8222 (https://linear.app/canary-technologies/issue/ENT-8222): state In Progress -> Done; closing comment posted with the three blocking asks (no title fallback, iteration 2 in a separate doc, store only the aggregate key).
  - STAY-6027 (https://linear.app/canary-technologies/issue/STAY-6027): comment posted with the four gaps (zero-price items skipped, Visual Matrix four-character limit, present-but-invalid codes, ECI/LCO codes on legacy addon tables) plus the Best Western scale (147 hotels, 467 rows, 92 sold in the last 30 days).
  - ENT-5695 (https://linear.app/canary-technologies/issue/ENT-5695): now Duplicate of STAY-6027.
  - ENT-5987 (https://linear.app/canary-technologies/issue/ENT-5987): reassigned to Marta Ziaei, state still In Progress; handover comment posted, mentioning her and asking whether Wyndham ever replied.

  ### Side effect to know about
  - Marking ENT-5695 as a duplicate made Linear move its related links onto STAY-6027. ENT-5695 now shows no related issues; STAY-6027 gained ENT-5697, INT-11979, PMS-11824, PMS-11508 and PMS-11495.
  - So ENT-5695 has no direct STAY-6032 relation. STAY-6027 was already related to STAY-6032 (https://linear.app/canary-technologies/issue/STAY-6032), so the link exists one hop away.
  - ENT-5697 is now related to STAY-6027 instead of ENT-5695.

  ### Not done
  - ENT-5697 (https://linear.app/canary-technologies/issue/ENT-5697): no change. Still In Review, assigned to you, in Enterprise, not related to STAY-6032. Unposted handover comment draft:

    Handing this to PMS Engineering. Re-validated on 2026-11-20:
    - 479 enabled Wyndham OHIP configs across 83 chains have no cashier ID.
    - Largest chains first: WHRMID3 (113 of 115), WHRFUL3 (47 of 61), WHRLT3 (36 of 37), WHRMP18 (27), WHRMP31 (16).
    - Cashier ID 0 is rejected ("Invalid Cashier") at wyndham-58739, wyndham-60260 and wyndham-57491.
    - No evidence either way, to check in Opera: wyndham-56382, wyndham-58362, wyndham-15483, wyndham-60566, wyndham-60577.
    - The tools exist: bulk edit by chain code (canary#51248) and create cashier ID (canary#50093), written by Drew Delianides and Lei Ferretti.
    - The silent-failure half is tracked in STAY-6032.

    Possible destinations: PMS Engineering team (key PMS), Integrations team (key INT), or stay in ENT assigned to Drew.
  - Best Western CS list (147 hotels, 467 rows, the 92 recent sellers first): not exported and not sent. The export is a production read and the send is outbound, so both need your go-ahead.
  - ENT-5987: the Wyndham-level ticket for the SynXis "Cannot find charge code" gap (13 Wyndham hotels in one day) was not opened; you chose the reassign route.
project: null
source_id: null
tags: []
time_minutes: null
title: 'Make these changes to tickets: close out ENT-8222, ENT-5695, ENT-5697, ENT-5987'
updated: 2026-11-20 13:41:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Validated read-only on 2026-11-20. Nothing has been changed yet.

## 1. ENT-8222 (review GJM Drift Detection design): mark Done
- Review is delivered; nothing is waiting on me in the Notion doc.
- Optional closing comment with my three blocking asks:
  - No title fallback (fix the association records instead).
  - Iteration 2 goes in a separate doc.
  - Store only the aggregate key for now.

## 2. ENT-5695 (addon charges fail on missing vendor_id): merge into In-Stay tickets
- Comment on STAY-6027 with what it is missing:
  - Zero-price items are skipped today, so they should not be flagged.
  - Visual Matrix rejects codes over four characters.
  - A code can be present but invalid.
  - Early check-in and late checkout codes live on the legacy addon tables, not the upsell row.
- Relate STAY-6032, then close ENT-5695 as a duplicate of STAY-6027.
- Send Best Western CS the list of 147 hotels with paid blank-code items (467 rows), starting with the 92 that sold one in the last 30 days. The list still needs exporting.

## 3. ENT-5697 (Wyndham addon charges fail on missing cashier_id): hand to PMS Engineering/Integrations
- Drew Delianides and Lei Ferretti wrote the tools (#51248 bulk edit by chain code, #50093 create cashier ID).
- 479 enabled Wyndham OHIP configs across 83 chains have no cashier ID.
- Largest chains first: WHRMID3 (113 of 115), WHRFUL3 (47 of 61), WHRLT3 (36 of 37), WHRMP18 (27), WHRMP31 (16).
- Cashier ID 0 is rejected ("Invalid Cashier") at wyndham-58739, wyndham-60260, wyndham-57491.
- No evidence either way, to check in Opera: wyndham-56382, 58362, 15483, 60566, 60577.
- Link STAY-6032 for the silent-failure half.

## 4. ENT-5987 (La Quinta Dallas North Central upsell not syncing): move off my plate
- Still failing: a paid late checkout on 16 November got "Cannot find charge code" for UPLCO.
- Property has had the fix in writing since 8 May (Zendesk #173444) and never replied; no Wyndham reply on record.
- Either reassign to Marta Ziaei as-is, or open one Wyndham-level ticket for the SynXis "Cannot find charge code" gap (13 Wyndham hotels in one day) and close ENT-5987 as a duplicate.
- Ask Marta whether Wyndham ever replied when handing over.