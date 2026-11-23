---
area: null
completed_at: null
contexts: []
created: 2026-11-20 13:43:23.256503
defer_until: null
due: null
energy: null
id: 2026-11-20T1343-next-steps-on-ent-5697-wyndham-addon-charges-fail
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Next steps on ENT-5697 (Wyndham addon charges fail on missing cashier_id)
updated: 2026-11-20 14:15:40.592100
waiting_on: null
waiting_since: null
working_on: false
---

ENT-5697: https://linear.app/canary-technologies/issue/ENT-5697

## Where it stands (2026-11-20)
- Untouched in today's ticket clean-up: still In Review, assigned to me, Enterprise team.
- Not related to STAY-6032. It is now related to STAY-6027 instead of ENT-5695, because closing ENT-5695 as a duplicate moved its links.
- Only comment on the ticket is my 2026-04-09 investigation. Its numbers are stale (937 hotels, 125 chains missing a cashier ID).

## Next steps
1. Decide the destination: PMS Engineering team (key PMS), Integrations team (key INT), or keep it in ENT and assign Drew Delianides.
2. Post the handover comment below and move or reassign the ticket.
3. Relate STAY-6032 (https://linear.app/canary-technologies/issue/STAY-6032) for the silent-failure half.
4. Whoever takes it still needs the cashier ID values per chain from Wyndham; the tools only write them.

## Research to hand over (validated read-only 2026-11-20)
- 479 enabled Wyndham OHIP configs across 83 chains have no cashier ID.
- Largest chains first: WHRMID3 (113 of 115), WHRFUL3 (47 of 61), WHRLT3 (36 of 37), WHRMP18 (27), WHRMP31 (16).
- Cashier ID 0 is rejected ("Invalid Cashier") at wyndham-58739, wyndham-60260, wyndham-57491. This answers the April open question about the seven chains set to '0' (WHREX06, WHRMP60, WHRMP65, WHRMP68, WHRMP69, WHRMP71, WHRMP72): 0 is not a safe value.
- No evidence either way, to check in Opera: wyndham-56382, wyndham-58362, wyndham-15483, wyndham-60566, wyndham-60577.
- Tools exist: bulk edit by chain code (canary#51248) and create cashier ID (canary#50093), written by Drew Delianides and Lei Ferretti.
- Root cause from April: the cashier ID is missing at chain-code level in the OnboardingValue OHIP credentials (kind OHIP_CREDENTIALS_BY_CHAIN_CODE), so every hotel on the chain fails with "Cannot post billing charge without `cashier_id`".
- Working chains for reference, as of April: WHRMID 5035, WHRF01 3809, WHRFULL 793, WHRMP10 128, WHRFLQ1 30, WHRMP3 184.
- The failure is silent to staff; STAY-6032 covers telling the hotel.

## Draft handover comment (not posted)
Handing this to PMS Engineering. Re-validated on 2026-11-20:

- 479 enabled Wyndham OHIP configs across 83 chains have no cashier ID.
- Largest chains first: WHRMID3 (113 of 115), WHRFUL3 (47 of 61), WHRLT3 (36 of 37), WHRMP18 (27), WHRMP31 (16).
- Cashier ID 0 is rejected ("Invalid Cashier") at wyndham-58739, wyndham-60260 and wyndham-57491.
- No evidence either way, to check in Opera: wyndham-56382, wyndham-58362, wyndham-15483, wyndham-60566, wyndham-60577.
- The tools exist: bulk edit by chain code (canary#51248) and create cashier ID (canary#50093), written by @drew and @lei.
- The silent-failure half is tracked in STAY-6032.