---
area: null
contexts: []
created: 2026-05-05 14:42:49.093231
defer_until: null
due: null
energy: low
id: 2026-05-05T1442-read-ihg-notes
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: Read IHG notes
updated: 2026-05-07 12:32:05.631724
waiting_on: null
waiting_since: null
working_on: false
---

# Blake's doc — short version

## The doc
Internal prep for an IHG working session. Response to Monica Bryson's 2026-05-01 email with 7 questions about making Canary "appear hosted on an IHG domain."

## Core reframe (lead the call with this)
IHG is quoting a Canary spec doc that was written for their **mobile app team** (WebView in the iOS app), not for embedding in `www.ihg.com`. The "Custom SDK" line they're fixated on is a 2-sentence non-normative aside — no JS SDK exists.

## Recommended answer
**Custom subdomain CNAME** (e.g., `checkin.ihg.com`). 63 customers live on it. Cleanest match for Monica's stated goal of "guest confidence." True in-page embed in `www.ihg.com` is greenfield (new CSP, missing `check_out_*` URLs, new design, PCI scoping).

## The 7 answers
1. **JS SDK for DCO** — No.
2. **Web Component** — No. Probe why they need it vs an iframe.
3. **`check_out_iframe_url`** — Doc means *mobile WebView*. Also: spec promises `check_out_*` URLs that the code doesn't return. Fix one or the other.
4. **Redirect callback** — Doesn't exist. Today's model is server-side webhooks (HMAC-signed). Could build it on existing HMAC infra.
5. **Locale** — Both `?lang=` and in-flow selector work. Caveats: DCI/DCO use different precedence chains; **mid-flow change doesn't persist back** (post-checkin comms stay in original language); `external_urls` doesn't accept locale.
6. **China** — No infra (no CDN, no ICP, no region). Legal posture covered (PIPL doc). Won't scale. **Leadership re-decision pending** — commit nothing beyond "joint discovery."
7. **Figma** — None. Sprint-planning blocker. Ask if IHG owns design or Canary leads.

## Cross-cutting
- **DCO is contractually paused/sunset** for IHG outside the GXP pilot (per DJ Singh) — confirm before committing roadmap.
- **Doc-vs-code gap** in `external_urls` needs fixing regardless.
- **No other client wants web embedding** — if we build a JS SDK, scope it as a generic product or accept it'll become IHG-bespoke.

## China sub-thread
Second enterprise asking in 2026. Harman shut down Wyndham on Apr 23; Bryan made the cross-account counter-case (Wyndham + IHG + Accor + Marriott/Hilton); AJ tagged for legal review. Unresolved. Three options: hold no / HRS+Tencent partner / build in-region.

## Attendees
- **Canary**: Caitlyn, Vibhor (embed/CSP/doc gap), Sharon (China/payments), Blake (SDK roadmap, DCO).
- **IHG**: Monica, web lead, security/compliance, design lead. Worth pulling in IHG's mobile-app team since the original doc was theirs.

## Bottom line
Reframe. Push subdomain. Be honest: no JS SDK, no Web Component, no redirect callback, no China infra, locale persistence broken, DCO paused. Don't commit on China.