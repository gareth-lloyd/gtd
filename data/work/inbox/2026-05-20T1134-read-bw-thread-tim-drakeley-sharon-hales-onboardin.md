---
area: null
contexts:
- consume
created: 2026-05-20 11:34:33.413316
defer_until: null
due: null
energy: low
id: 2026-05-20T1134-read-bw-thread-tim-drakeley-sharon-hales-onboardin
order: null
output: |
  ## Agent run 2026-05-20T11:50:00

  Read full 46-reply thread in #C07BX379GQK (BW Hotelkey integration).

  **Sharon Hales' trigger:** Got Hotelkey requests for 4 BWH hotels that were NOT on the existing tracking sheet (https://docs.google.com/spreadsheets/d/1Rb8rJC_tDnSr94xPvFTzQ7i6N24fgxQQAuzZQsY-R5Q/). First go-live was 5/20.

  **Process for BW↔Hotelkey credentials:** We (Canary) generate UN/PW → send to Hotelkey → they return their PW for the integration side.

  **Tim Drakeley's role (the prompt's claim, confirmed):** Tim replied (msg ts 1778854992.276979) "I'm not too sure why we'd get requests outside of this sheet. I'll have to defer to Melissa on that one." So Tim handles the sheet; anything off-sheet goes to Melissa Fairchild.

  **Melissa took over the off-sheet work:**
  - Confirmed 3 of 4 hotels were already active Canary users (so BW goes officially live on integration once we flip them).
  - 1 hotel (BW 41115) is a brand-new property, not yet in BW's master list — she built initial config.
  - Created an internal rollout mastersheet: https://docs.google.com/spreadsheets/d/1Yjid0XdYRyDkZPFJdwd1X5eSN5m4ZtzF2m66yXw8ga4/
  - Generated UN/PW, added them, and asked whether to also plug into gateway or wait for script-based upload.

  **Wyndham→BW rebrand item (this is the connected GTD task):**
  - Msg ts 1778867385.980589, Melissa: one of the 4 properties is a Wyndham rebrand to BW. Property was never cut from Wyndham portfolio; SFDC has already rebranded to BW.
  - Hotel: https://www.canarytechnologies.com/canary-admin/hotels/hotel/127838/change/
  - She asked me to remove from Wyndham portfolio. **TODO for me on the other GTD item:** use PortfolioService.remove_hotel (per [[feedback_portfolio_service]]), not PortfolioHotel directly.

  **My state on 5/19:**
  - Manually ran the opt-out batch (msg 1779195390).
  - Told Melissa to try Django admin "create from csv" for the onboarding values — she got most of the way but is blocked on Hotelkey sending their UN/PW back.
  - Cc'd Taylor Kirch — plan is to standardize this same flow for IHG.
  - PMS onboarding value confirmed: `HOTELKEY` (BW calls it "Atlas"; we picked HOTELKEY so it's not BW-specific and IHG can reuse).

  **Open action items from the thread (not for this task — these may need separate GTD items if not already captured):**
  1. Hotel 127838 — remove from Wyndham portfolio for BW rebrand (linked Wyndham→BW item).
  2. Last message (1779211107.112829): Melissa asked "can we add BW reg card to HOTELKEY" — appears unanswered. May need follow-up.
  3. Connor was going to ask Jason on Monday whether BW's Atlas migrations can come through Canary's standard feed (so we stop discovering hotels off-sheet) — unclear if that happened.

  **Why the thread matters for the rebrand item:** confirms that hotel 127838 is mid-transition (SFDC says BW, Wyndham portfolio still has it, new Hotelkey integration being set up under BW). Removing it from Wyndham portfolio is the explicit ask from Melissa.

  No external writes performed. Read-only research only.
project: null
source_id: https://canarytechnologies.slack.com/archives/C07BX379GQK/p1778854992276979?thread_ts=1778842566.238089&cid=C07BX379GQK
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: 'Read BW thread: Tim Drakeley / Sharon Hales onboarding sheet'
updated: 2026-05-20 11:50:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Best Western onboarding sheet thread — Tim defers requests outside the sheet to Melissa. Context for the Wyndham→BW rebrand item. https://canarytechnologies.slack.com/archives/C07BX379GQK/p1778854992276979?thread_ts=1778842566.238089&cid=C07BX379GQK