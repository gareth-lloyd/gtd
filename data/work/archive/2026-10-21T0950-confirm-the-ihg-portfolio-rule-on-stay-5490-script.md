---
area: null
completed_at: 2026-10-21 14:04:25.903923
contexts:
- react
created: 2026-10-21 09:50:10.463644
defer_until: null
due: 2026-10-21
energy: low
id: 2026-10-21T0950-confirm-the-ihg-portfolio-rule-on-stay-5490-script
order: null
output: |
  ## Agent run 2026-10-21T10:25

  **Verdict:** the "IHG Portfolio" rule was the right one and the script applied it correctly. One IHG-branded Opera hotel was missed because it is in no IHG portfolio. Nothing else is left to turn off.

  **What the script used** (PR #60834, https://github.com/canary-technologies-corp/canary/pull/60834, `onetime_disable_ihg_opera_live_availability`): hotels in any of IHG, IHG_NON_MSA, ihg_poc, ihg_conference, ihg_guest_messaging, IHG_INTERCONTINENTAL, IHG_KIMPTON or IHG_SIX_SENSES, with an enabled OPERA or ORACLE_OHIP gateway, minus Nico's 15 excluded slugs. That is broader than Nico's "IHG Portfolio". It leaves out the IHG Demo, Staging, Deactivated and MSA GMS Core/Core Plus portfolios.

  **Checked against prod**: read-only Snowflake CANARY_RAW mirror, all 3 regions, CDC rows deduped. I listed every hotel that still has live availability or dynamic pricing on and is either in an `%ihg%` portfolio or has an IHG brand name.
  - **US**: no hotel in an IHG portfolio and on Opera still has a flag on, so the script covered them all. No hotel sits only in a portfolio the script left out (MSA GMS, staging, demo, deactivated) with a flag on. **Missed: hotel 129287454 "Holiday Inn & Suites Orlando SW - Celebration Area, an IHG Hotel"**: PMS OPERA, live availability on, dynamic pricing on, in no IHG portfolio. Also outside every portfolio: 129237203 "Deactivated - Holiday Inn Express & Suites Washington DC - NoMA - Axar Hotels" (OPERA_CLOUD, live availability on). It is deactivated, so it does not matter.
  - **EU**: 13 Opera hotels in IHG portfolios still have flags on. By name, they appear to be Nico's exclusions: Milton Keynes, Birmingham NEC, Heathrow M4, Edinburgh, Guildford, Regents Park, Basildon, Cardiff, Cambridge, Glasgow Airport, Bristol Filton, Sutton and Brentwood. I could not confirm the slugs because HOTELS_HOTELSLUG is not readable in Snowflake. Only the PMS rule keeps InterContinental Almaty (HAPI_CLOUD) out of scope.
  - **AP**: none.
  - Out of scope by the PMS rule: about 14 IHG HotelKey hotels and 1 HAPI hotel in the US still have live availability on. Their rates may be closed to Canary too, which is a product question for Nico.
  - Data oddity, unrelated: "Days Inn & Suites by Wyndham Surprise" (128710) and "Days Inn by Wyndham Flagstaff I-40" (128643) are in the IHG portfolio.

  Caveat: PMS comes from `hotel.pms` in Snowflake, not the pms-gateway vendor/is_enabled the script used. The mirror lags about 25 minutes.

  **Draft reply for STAY-5490 (NOT posted, it needs your OK)**, in reply to Nico's comment https://linear.app/canary-technologies/issue/STAY-5490/upsells-script-disable-live-availability-and-dynamic-pricing-for-all#comment-78d902f6:

  > @nico IHG portfolio was the right rule. Ishwar's script used all the IHG sub-portfolios (Kimpton, InterContinental, Six Senses, messaging-only, pilot, non-MSA), and nothing in them on Opera/OHIP still has the flags on apart from your exclusions. One miss: **Holiday Inn & Suites Orlando SW - Celebration Area** (hotel 129287454, Opera) is IHG but isn't in any IHG portfolio, so it still has Live Availability and Dynamic Pricing on. Want Ishwar to flip it by hand, and should someone add it to the IHG portfolio? Separately, ~14 IHG HotelKey hotels still have Live Availability on, which is out of scope for this ticket. Flag it if their rates are also closed to Canary.

  Possible follow-ups (your call): post the reply; ask Ishwar or Nico to flip hotel 129287454; fix its portfolio membership with PortfolioService.add_hotels.
project: 2026-08-31-ihg
source_id: https://linear.app/canary-technologies/issue/STAY-5490/upsells-script-disable-live-availability-and-dynamic-pricing-for-all#comment-78d902f6
tags:
- morning-gtd
- linear
time_minutes: 5
title: Confirm the IHG portfolio rule on STAY-5490 (script already run)
updated: 2026-10-21 14:04:25.903919
waiting_on: null
waiting_since: null
working_on: false
---

Nico: "all hotels in the IHG Portfolio, correct me if there is another portfolio/brand rule to consider @glloyd". Ishwar ran it Oct 20; issue is Done. 9 new comments.
https://linear.app/canary-technologies/issue/STAY-5490/upsells-script-disable-live-availability-and-dynamic-pricing-for-all