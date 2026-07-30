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

  ## Agent run 2026-07-29T15:52:03+03:00

  Re-assessed with the correct source email: the Dec 2024 - Jan 2025 thread
  "Re: Re-authentication flow for SSO providers" (Blake/Aman/Brad/Charles/Gareth) —
  this, not the Caesars Okta thread, is the "email from jan last year". Question:
  pci_heartbeat still has exceptions for Wyndham + Best Western — impact? remove?

  ### Current state of EXCLUDED_SSO_ORG_SLUGS (["wyndham", "bestwestern"])
  - Used in two places: validate_pci_session (backend 401 enforcement on CC reveal,
    user management, check-in dashboard card, hotel-staff endpoints) and
    HeartbeatView (tells the frontend active/idle).
  - Marriott, Four Seasons cut from the list Jan 2026 (#36692, by Gareth); Drury
    removed 2025 (#28242). Only wyndham + bestwestern remain.

  ### Finding 1: the Best Western entry is a typo no-op
  Real SSO org slug is `best-western` (hyphenated; confirmed in prod logs — no
  `bestwestern` slug exists). The exclusion has NEVER matched. BW (877 SSO
  login-redirects/7d) has had full PCI idle enforcement all along, with no known
  complaints. Removing the entry changes nothing in behavior.

  ### Finding 2: the Wyndham exemption is half-dead (heartbeat regression)
  PLAT-1424 (commit e007d23a3f5, Dec 3 2024) inserted `if authenticated_user.is_staff:`
  between the exclusion `if` and the idle-check `elif` in heartbeat.py, breaking the
  chain: for non-staff excluded users the second chain overwrites status back to IDLE.
  So for ~20 months the frontend has been told "idle" for Wyndham users and has been
  showing them the SSO re-auth modal before CC reveals anyway. Only the backend
  hard-block (validate_pci_session) still honors the exemption.

  ### Empirical impact (7d prod logs)
  - `validate_pci_session.excluded_hotel`: 2,872 hits, all wyndham, across 543
    hotels. Only 5 requests (0.17%) had session age >15 min; median age 5s, p95 142s.
    I.e. the exemption almost never actually exempts anyone — the (accidentally live)
    modal UX already forces re-auth first.
  - Wyndham completes /sso/login_redirect/wyndham ~919x/7d; reauthentication_success
    page ~7.3k hits/7d overall — the SSO re-auth popup flow demonstrably works for
    Wyndham.

  ### Recommendation: remove the exception
  - User-visible impact ~zero: Wyndham already sees the re-auth modal; removal only
    closes the backend enforcement hole (~5 requests/week would newly 401 with
    pci_reauthentication_required, which the axios interceptor handles by showing
    the same modal).
  - Closes the PCI DSS 4.0 Req 8.2.8 gap on our largest SSO org (89k requests/day).
  - The product sign-off the old thread was waiting on (Brad's customer calls) never
    happened — but 20 months of the modal accidentally live for Wyndham with no
    complaints is stronger evidence than those calls would have been.
  - Cleanup scope: delete pci_session/constants.py, both exclusion branches + TODOs,
    the excluded_hotel log; while there, fix the broken if/elif chain in heartbeat.py
    (keep the is_staff branch — PLAT-1767 still open).
  - Watch after removal: 401 rate on pci-guarded endpoints for wyndham
    (expect ~5/week).
project: null
source_id: null
tags: []
time_minutes: 5
title: Claude analysis of SSO login
updated: 2026-07-29 15:52:03.622381
waiting_on: null
waiting_since: null
working_on: false
---

email from jan last year