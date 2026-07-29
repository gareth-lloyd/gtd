---
area: null
contexts: []
created: 2026-07-28 16:02:21.621849
defer_until: null
due: null
energy: low
id: 2026-07-28T1602-claude-analysis-of-sso-login
order: null
output: |
  ## Agent run 2026-07-28T19:30:00+03:00

  Identified the linked email as the Caesars Okta SSO thread "Re: [EXTERNAL] Re: PDF of
  SAR document - Canary" (latest message Jul 27, Dianna Kertz nudging Caesars).
  Gmail: https://mail.google.com/mail/u/0/#inbox/FMfcgzQXKWfFDprDcDHMtDNKTjBKhTDx

  ### Where the SSO login stands
  - Jun 30: Sean Truxal (Caesars Identity Eng) assigned testers Cat Hudson + Kristie
    Thompson-Leflore to the Okta app; sandbox login is
    canarytechnologies.com/sso/login/caesars-sandbox.
  - Jul 2: Cat signed in via Okta and got "No Hotel Access".
  - Jul 2: Lautaro checked our logs: SAML login itself WORKS; the Okta app only sends
    first_name/last_name/email — no `hotels`/`roles` attributes, so we can't grant
    property or permissions. Sandbox accepts exactly hotels=caesars-sso-sandbox and
    roles in {front_desk_staff, general_manager, analytics_staff}.
  - Jul 7: Sean said Caesars internal must (1) decide which role groups to pass
    (created via CNOW tickets) and (2) pick a hotel identifier; he floated their
    three-letter property abbreviations.
  - Jul 8: Lautaro confirmed any unique identifier works for the hotel key.
  - Jul 15 → Jul 27: Sean asked Caesars internal for input; silence; Dianna nudged.

  ### Analysis
  - Nothing is blocked on Canary. The blocker is two Caesars-internal decisions
    (role groups + hotel identifier), stalled ~3 weeks. The testers are payroll
    staff, not IT, and no decision owner is named — that's why it's drifting.
  - Key unblock: sandbox testing does NOT need the production identifier decision.
    The sandbox only accepts the fixed values above, so Sean could statically map
    hotels=caesars-sso-sandbox and a test role for Cat/Kristie in the Okta app
    today and testing completes now; the identifier scheme only matters for the
    production hotel_mapping later. Worth suggesting this explicitly on the thread.
  - For production later: three-letter codes are fine — Organization.hotel_mapping
    maps IdP keys → Hotel.sso_hotel_id, and PR #49608 (ENT-6760, mapping validation
    on save, https://github.com/canary-technologies-corp/canary/pull/49608) will
    catch typos/unresolvable codes when we configure it.
  - Related hardening already merged that affects this exact failure mode:
    PR #50460 (missing hotels attribute now skips provisioning instead of
    destructive sync, https://github.com/canary-technologies-corp/canary/pull/50460)
    and PR #51135 (ENT-6940, fail SSO login on duplicate accounts,
    https://github.com/canary-technologies-corp/canary/pull/51135).

  ### Suggested next action (not sent — needs your approval)
  Reply to the thread (or feed Dianna/Lautaro the line): "For sandbox testing Sean
  can hard-set hotels=caesars-sso-sandbox and roles=general_manager for Cat and
  Kristie in the Okta app now — no need to wait on the group/identifier decision;
  that decision only gates production rollout, where three-letter codes work for us."
project: null
source_id: null
tags: []
time_minutes: 5
title: Claude analysis of SSO login
updated: 2026-07-28 16:22:09.692901
waiting_on: null
waiting_since: null
working_on: false
---

email from jan last year