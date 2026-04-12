---
area: null
contexts:
- computer
- calls
created: 2026-04-10 08:40:18.627606
defer_until: null
due: null
energy: null
id: 2026-04-10T0840-resolve-squatter
project: null
tags:
- focus
time_minutes: null
title: Resolve squatter
updated: 2026-04-12 12:08:00.837461
waiting_on: null
waiting_since: null
---

Situation:
  - Hotel 127384 / 02851 (Super 8 by Wyndham Laramie) needs +13072235230 (per OnboardingValue)
  - +13072235230 is currently held by hotel 124540 / 54602 (Travelodge by Wyndham London Ontario)
  - Hotel 124540 is active and has its own intended phone number in OnboardingValue

  Resolution (two-step):
  1. Move intended phone to squatter (124540): Run MoveIntendedPhoneToHotelSubaccount + ActivateIntendedPhoneNumberOperation on 124540 to give it its own intended number, freeing
  +13072235230
  2. Move +13072235230 to 127384: Run MoveExistingHotelPhoneAndReplaceOperation on 127384 (or manually move the number since the squatter should no longer hold it)

  Note: MoveExistingHotelPhoneAndReplaceOperation.perform already handles this exact scenario (lines 413–415 in wyndham_phone_number.py) when the squatter has an intended phone —
  but MoveIntendedPhoneToHotelSubaccount.can_be_started(124540) is currently failing for an unknown reason. Investigate what prerequisite is missing on 124540 before proceeding.