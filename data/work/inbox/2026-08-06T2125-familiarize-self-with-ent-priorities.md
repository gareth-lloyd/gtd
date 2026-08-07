---
area: null
completed_at: null
contexts: []
created: 2026-08-06 21:25:01.377283
defer_until: null
due: null
energy: low
id: 2026-08-06T2125-familiarize-self-with-ent-priorities
order: null
output: |
  ## Agent run 2026-08-07T12:20

  **10 ENT projects carry a Q3 block label** — 4 on "2026 Q3 Block 1", 6 on "2026 Q3 Block 2".
  (Linear project labels are literally `2026 Q3 Block 1` / `2026 Q3 Block 2`; there is no
  "Block A/B" label. There are also Q4 Block 1/2 labels already created, so the next
  planning cycle is partly staged.)

  ### Block 1 (4 projects)

  1. **Portfolio "Typing"** — Andrea Bradshaw · Implementation · Jul 1 → Aug 31 · Medium
     https://linear.app/canary-technologies/project/portfolio-typing-60798dba32e0
     Healthiest project of the set. Schema foundation 6% → 63% in the last two weeks;
     Django admin merged, backfill command up for review this week. On track.

  2. **Portfolio Reconciliation — Portfolio Membership** — *Gareth Lloyd (you)* · Product
     Definition · Jul 20 → Aug 31 · no priority set
     https://linear.app/canary-technologies/project/portfolio-reconciliation-portfolio-membership-4171e7fc6c55
     ⚠️ **Zero issues, zero status updates, untouched since Jul 7.** Target date is Aug 31
     and it's still in Product Definition with nothing scoped. This is the one item on the
     board that is yours and it is the most visibly stalled. Either it needs scoping this
     week or it needs to be honestly re-dated / dropped to Q4 Block 1.

  3. **Kiosk GTM: Kempinski** — Elena Browne · Implementation · Jul 6 → Sep 30 · High
     (shared ENT + KSK) https://linear.app/canary-technologies/project/kiosk-gtm-kempinski-7d22cbf9c005
     Moving fast: Tablet Reg Pilot 69% → 87%, Kiosk Pilot 5% → 18%. ENT pod's slice is
     loyalty auto-enrollment. Named risk: ID verification against **Thai IDs** (pilot is
     Siam Kempinski Bangkok). Kick-off with pilot property was due this week.

  4. **Revamped "Managed Context" for Wyndham** — Ryan Rogers · Eng Design · Jul 20 → Aug 31
     https://linear.app/canary-technologies/project/revamped-managed-context-for-wyndham-5dacdafdd264
     No status updates, but 10 tickets (ENT-7089…ENT-7098) all freshly written Aug 5–6 —
     so it's real work just not narrated. 1 in review, 2 in progress, rest backlog.
     Goal is raising voice-agent handle rate; ENT-7093 explicitly depends on Content Gateway.

  ### Block 2 (6 projects)

  5. **Configuration Drift Detection** — Tincho Martin Rodriguez · Implementation ·
     Jun 16 → **Jul 31 (target already passed)**
     https://linear.app/canary-technologies/project/configuration-drift-detection-364d47914acc
     Furthest along in substance: drift computed + cached per hotel, admin view/filter and
     "Recalculate now" shipped. Validated read-only against ~4,600 Wyndham hotels, ~2%
     drifting, no false positives. Remaining: nightly CronJob (in draft review), roll-up of
     drift to root-cause master flags (raw counts overstate: one hotel's "10 of 24" was
     really ~3 problems), coverage gaps, alerting.

  6. **Content Gateway** — Ryan Rogers · Implementation · Jun 1 → Aug 31 · also tagged
     "1. Aspirational" https://linear.app/canary-technologies/project/content-gateway-191c10f2fa2d
     🚩 **Externally blocked.** Core gateway 100%, separate-DB work landed, Wyndham
     compendium cutover 50% — but prod API access was promised for Jul 30 and the vendor
     sent an "indefinite delay" email instead. Still marked onTrack, which looks optimistic.
     Note this also gates ENT-7093 in Managed Context.

  7. **Migrate Embedded Reporting from Explo to Omni** — Lautaro Mena · Implementation ·
     Jun 15 → Sep 30
     https://linear.app/canary-technologies/project/migrate-embedded-reporting-from-explo-to-omni-5bf86d7f3b1e
     Hard external deadline: Explo sunsets end of 2026. Omni delivered first-cut property
     dashboards, already wired into the Manage app analytics section; all still need work.

  8. **Enterprise Rollout: Segmentation for Wyndham** — Andrés Figueira · Eng Design ·
     Jul 1 → **Jul 31 (passed)** · Low priority
     https://linear.app/canary-technologies/project/enterprise-rollout-segmentation-for-wyndham-f14fbcb66bba
     Eng design done, in review. Progress actually went *backwards* 25% → 17% (rescope).
     Includes migrating existing templated configs + letting Wyndham pre-populate segments.

  9. **IHG Scripting Changes — Pilot to Scale** — Connor Swords · Product Definition ·
     started Jul 28 · no target date
     https://linear.app/canary-technologies/project/ihg-scripting-changes-pilot-to-scale-e52e4a381d06
     15 tickets, **all still Todo/Backlog, none started.** Clusters into: translations
     (ENT-7057/7058/7059/7060), reg-card + upsell config (ENT-6979/6980/6987/7061),
     SSO roles & permissions (ENT-6985/7088), onboarding-value plumbing (ENT-7062),
     guest-journey messaging (ENT-7003/7016), branding (ENT-7015), compendium (ENT-7017).
     This is the natural follow-on to the ENT-6032 IHG HotelKey Wave 1 pilot.

  10. **Permissions Consistency: Above Property & Hotel Dashboard** — **no lead** ·
      Product Definition · started Aug 6 · no target date, no issues, no summary
      https://linear.app/canary-technologies/project/permissions-consistency-above-property-and-hotel-dashboard-8ba3a88a21ab
      Brand new (created yesterday) and completely empty. Nobody owns it.

  ### What actually stands out

  - **Two ownership gaps:** your Portfolio Reconciliation project (empty, Aug 31 target)
    and Permissions Consistency (no lead at all). Both sit in Product Definition doing
    nothing.
  - **Three target dates are already blown or absent:** Config Drift (Jul 31), Segmentation
    (Jul 31), and IHG Scripting + Permissions Consistency have no target date at all.
  - **Content Gateway is the only genuinely blocked-by-outside-party project** and it's
    still flagged onTrack — worth a health downgrade, and it has a downstream dependency
    (ENT-7093).
  - **Wyndham is the dominant theme** — Managed Context, Config Drift, Segmentation, and
    Content Gateway's compendium cutover all target Wyndham. IHG is the second cluster.
  - Reporting/Omni has the only externally-imposed hard deadline (Explo sunset, end 2026).

  No writes made to Linear.
project: null
source_id: null
tags: []
time_minutes: 5
title: Look at current ENT team Linear projects labeled for q3  block A or b. What's
  in play?
updated: 2026-08-07 12:20:00.000000
waiting_on: null
waiting_since: null
working_on: false
---