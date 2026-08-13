---
area: null
completed_at: null
contexts:
- react
created: 2026-08-13 07:57:17.250687
defer_until: null
due: 2026-08-13
energy: medium
id: 2026-08-13T0757-reply-to-bryan-in-epd-enterprise-re-blocking-marke
order: null
output: |
  ## Agent run 2026-08-13T08:03

  ### Where the thread actually landed (read all 17 replies)

  Thread: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786541314665829

  The incident itself is closed — you do NOT need to reply about the Wyndham pop-up:
  - Connor traced it to AppCues flow https://studio.appcues.com/flows/9fb6d0f7-b608-4e73-8702-1f00c0265ef9/settings
  - Root cause: the campaign excluded Wyndham hotel slugs but missed Wyndham UAT, which
    uses the `staging-wyndham-{SiteID}` slug format. Connor fixed the flow's targeting.
  - Jen Aceto turned the AppCue off; only UAT sites saw it, no live properties.
  - Marta confirmed in #wyndham and told Jen it was UAT-only:
    https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1786540137794179
  - Bryan approved adding Marriott, Hyatt, Drury, Four Seasons to the "Enterprise"
    AppCues segment (accepting reduced marketing reach).

  ### The one open question — and it's aimed at us

  Bryan's last message (https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786556372559249):
  "its a bummer we cant have a hard block on excluding brands". Connor said earlier
  "I don't think we have a blanket way to disable these" and put ownership on the
  campaign creator. **That's the gap worth your reply — and the answer is that a hard
  block IS buildable, and it's small.**

  ### What I verified in the codebase

  `frontend/packages/shared/utilities/analytics/CanaryAnalytics.ts`

  1. **AppCues loads unconditionally in prod.** Constructor line ~42:
     `if (process.env.VUE_APP_ENV === "production") { _initAppcues(); }` — fires before
     the hotel is even known (`setHotel()` is called later). There is no brand, portfolio,
     or hotel gate anywhere in the client. Connor is right that today there's no blanket
     switch: 100% of targeting lives inside AppCues.

  2. **We already push brand + portfolio properties to AppCues.** `getAppcueUserProperties()`
     merges hotel props with a `hotel_` prefix, including:
     - `hotel_parent_brand_name` (from `saleforce_hotel_metadata.parent_brand_name`)
     - `hotel_portfolios` (from `hotel.portfolio_identifiers`)
     - `hotel_id` (= `slug_name`), `hotel_is_demo`, `hotel_is_active`
     So segments can key off brand/portfolio from our own data instead of hand-maintained
     slug lists. Slug-prefix matching is precisely what failed here.

  3. **We already detect staging hotels — we just don't apply it to AppCues.**
     `isStagingHotel()` (line ~445) checks `slug_name.startsWith("staging-")` and is used
     to suppress *Amplitude* tracking (`track()` line ~548). It is NOT applied to the
     AppCues `identify()` path. Suppressing AppCues on all `staging-*` hotels would have
     prevented this exact incident regardless of brand list, and UAT is arguably the worst
     place for a marketing pop-up since that's where customers do acceptance testing.

  ### Draft reply — NOT POSTED, needs your review/approval

  Suggested as a thread reply to Bryan in #epd-enterprise:

  ---
  Bryan — on the "bummer we can't have a hard block": we can, and it's not a big lift.
  Two things, and they're independent.

  1. Short term, no eng needed: the enterprise segments should key off
  `hotel_parent_brand_name` and `hotel_portfolios` rather than hotel slug patterns.
  We already push both to AppCues on every identify, straight from our own data. The
  slug approach is exactly what broke here — `staging-wyndham-*` didn't match a
  "starts with wyndham" filter. Connor's caveat about SFDC accuracy applies to
  parent_brand_name; portfolios are managed in-product so they're the more reliable of
  the two.

  2. The actual hard block: today AppCues initialises for every production user before
  we even know which hotel they're in, so whether a campaign reaches Wyndham is decided
  entirely inside AppCues by whoever built the campaign. If we gate initialisation on a
  hotel-level flag from the backend, a mis-targeted campaign physically can't render for
  those brands — it stops being a targeting rule someone can forget. That's the version
  that survives human error, and it's roughly a small frontend change plus a flag.

  Separately I'd suppress AppCues on all UAT/staging hotels outright, whatever the brand.
  We already detect staging properties for our analytics and just don't apply it here.
  That alone would have caught this one.

  The decision I need from you: who owns the blocked-brand list and where does it live —
  Salesforce, portfolio config, or a fixed enterprise portfolio set in our own DB? That
  determines whether this is a day or a week.
  ---

  ### Notes / open questions for you

  - Connor's position ("this needs to be owned by the campaign creator, not the product
    team, because sometimes we DO want these going to brands") is reasonable and the
    draft doesn't contradict it — a backend flag still allows deliberate enterprise
    campaigns, it just makes the default safe rather than relying on correct setup.
  - No Linear ticket exists for this yet as far as I can tell. If you want the hard block
    built, it probably needs one.
  - Nothing was posted anywhere. No Slack message sent, no ticket created, no code changed.
project: null
source_id: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786541314665829
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to Bryan in #epd-enterprise re: blocking marketing pop-ups for enterprise
  brands'
updated: 2026-08-13 08:03:02.360313
waiting_on: null
waiting_since: null
working_on: false
---

Bryan @-ed me, Connor and Andrea: block App Cues marketing/sales/new-product pop-ups for Wyndham, BWH, IHG, Four Seasons, Drury, Marriott, Hyatt and route all pop-ups through the enterprise team for approval. Marta escalated the same day in #wyndham ("can we disable this pop up asap?" — a live pop-up referencing another customer). 17 replies already.
https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1786541314665829