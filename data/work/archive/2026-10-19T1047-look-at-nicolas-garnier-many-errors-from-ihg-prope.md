---
area: null
completed_at: 2026-10-19 16:32:22.200615
contexts:
- react
created: 2026-10-19 10:47:41.719460
defer_until: null
due: 2026-10-19
energy: medium
id: 2026-10-19T1047-look-at-nicolas-garnier-many-errors-from-ihg-prope
order: null
output: |
  ## Agent run 2026-10-19T13:05
  **Thread** (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792184430382859): Nico, Connor, and Tay talked on Fri 17 Oct. You weren't tagged. It stopped at Tay's question, which nobody has answered: **"Can we only hide for OHIP or no?"**
  - Nico says IHG's OHIP config doesn't make rates available to Canary, so the live availability and rate calls fail. Guests then get static pricing and are offered rooms that aren't available. Hotels are opening support tickets. Groundcover dashboard: https://app.groundcover.com/dashboards/7bcebc28-31f1-4666-8e38-98e9e3d7213d (the "Live Availability errors by hotel" panel; OHIP is the main source).
  - Tay: IHG isn't supposed to use these features until we have a direct CRS integration, but nothing in the product stops a hotel turning them on.
  - Nico offered to gate the features (hide them for IHG and turn them off where they're on). Tay first wanted to leave them on, then asked about hiding only for OHIP.

  **How the gate works in code (answers Tay's question):**
  - The toggles are `trusts_live_inventory`, `trusts_dynamic_pricing` and `availability_rate_code` on the addons `Configuration`. Hotels set them in adminland `frontend/adminland/src/upsells/UpsellsSettingsPage.vue:84`.
  - The toggles show only when the GrowthBook flag `in-stay-show-live-availability-status` (default **True**) is on AND the hotel has the `get_availability` PMS capability. The dynamic pricing toggle also needs `get_availability_live_rates`.
  - **Hide for all IHG, no code change:** the frontend sends `hotel_public_portfolio_identifiers` and `portfolio_uuid` to GrowthBook, so a targeting rule can turn the flag off for the IHG portfolio.
  - **Hide for IHG + OHIP only:** GrowthBook gets no PMS attribute, so this needs either (a) a small code gate or new attribute, or (b) removing the `get_availability` capability from IHG OHIP accounts in pms-gateway. I didn't check what else depends on that capability, so (b) is riskier.
  - **Hiding doesn't switch anything off.** Hotels that already enabled it keep `trusts_live_inventory=True`, and backend reads (`pricing/services/room_upgrade_quote_service.py:24`, addons selectors) don't check the flag. So a one-off prod write is also needed to set it False for affected IHG hotels. That needs explicit approval and should go through a management command, not shell.
  - Both keys are already rules-based setting keys (`rules_based_configuration/types/setting_keys.py:489-490`). Once IHG has rules (ENT-7726 binding/convention work), `trusts_live_inventory=False` for IHG would make drift alerts catch hotels that turn it back on.

  **Not done:** I didn't query Groundcover to count failing hotels or confirm the error signature. Nothing was posted anywhere.

  **Possible reply** (only if you want to join in; not sent):
  > Re hide-for-OHIP-only: the toggles are gated by the `in-stay-show-live-availability-status` GrowthBook flag + `get_availability` capability. Hiding for all of IHG is just a GrowthBook targeting rule on the IHG portfolio, no deploy. OHIP-only needs a small code change, since GrowthBook doesn't see the PMS. Either way, hotels that already enabled it stay on until we flip `trusts_live_inventory`/`trusts_dynamic_pricing` off for them.
project: 2026-08-31-ihg
source_id: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792184430382859?thread_ts=1792184430.382859&cid=C03V5P4B48P
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Look at Nicolas Garnier: many errors from IHG properties on Live Availability
  & Dynamic Pricing, looks like IHG config (11 replies)'
updated: 2026-10-19 16:32:22.200604
waiting_on: null
waiting_since: null
working_on: false
---

From morning awareness (Slack highlights).
https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1792184430382859?thread_ts=1792184430.382859&cid=C03V5P4B48P