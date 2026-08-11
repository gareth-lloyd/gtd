---
area: null
completed_at: 2026-08-07 13:42:16.837025
contexts: []
created: 2026-08-06 21:25:01.377283
defer_until: null
due: null
energy: low
id: 2026-08-06T2125-familiarize-self-with-ent-priorities
order: null
output: "## Agent run 2026-08-07T12:20\n\n**10 ENT projects carry a Q3 block label**
  — 4 on \"2026 Q3 Block 1\", 6 on \"2026 Q3 Block 2\".\n(Linear project labels are
  literally `2026 Q3 Block 1` / `2026 Q3 Block 2`; there is no\n\"Block A/B\" label.
  There are also Q4 Block 1/2 labels already created, so the next\nplanning cycle
  is partly staged.)\n\n### Block 1 (4 projects)\n\n1. **Portfolio \"Typing\"** —
  Andrea Bradshaw · Implementation · Jul 1 → Aug 31 · Medium\n   https://linear.app/canary-technologies/project/portfolio-typing-60798dba32e0\n
  \  Healthiest project of the set. Schema foundation 6% → 63% in the last two weeks;\n
  \  Django admin merged, backfill command up for review this week. On track.\n\n2.
  **Portfolio Reconciliation — Portfolio Membership** — *Gareth Lloyd (you)* · Product\n
  \  Definition · Jul 20 → Aug 31 · no priority set\n   https://linear.app/canary-technologies/project/portfolio-reconciliation-portfolio-membership-4171e7fc6c55\n
  \  ⚠️ **Zero issues, zero status updates, untouched since Jul 7.** Target date is
  Aug 31\n   and it's still in Product Definition with nothing scoped. This is the
  one item on the\n   board that is yours and it is the most visibly stalled. Either
  it needs scoping this\n   week or it needs to be honestly re-dated / dropped to
  Q4 Block 1.\n\n3. **Kiosk GTM: Kempinski** — Elena Browne · Implementation · Jul
  6 → Sep 30 · High\n   (shared ENT + KSK) https://linear.app/canary-technologies/project/kiosk-gtm-kempinski-7d22cbf9c005\n
  \  Moving fast: Tablet Reg Pilot 69% → 87%, Kiosk Pilot 5% → 18%. ENT pod's slice
  is\n   loyalty auto-enrollment. Named risk: ID verification against **Thai IDs**
  (pilot is\n   Siam Kempinski Bangkok). Kick-off with pilot property was due this
  week.\n\n4. **Revamped \"Managed Context\" for Wyndham** — Ryan Rogers · Eng Design
  · Jul 20 → Aug 31\n   https://linear.app/canary-technologies/project/revamped-managed-context-for-wyndham-5dacdafdd264\n
  \  No status updates, but 10 tickets (ENT-7089…ENT-7098) all freshly written Aug
  5–6 —\n   so it's real work just not narrated. 1 in review, 2 in progress, rest
  backlog.\n   Goal is raising voice-agent handle rate; ENT-7093 explicitly depends
  on Content Gateway.\n\n### Block 2 (6 projects)\n\n5. **Configuration Drift Detection**
  — Tincho Martin Rodriguez · Implementation ·\n   Jun 16 → **Jul 31 (target already
  passed)**\n   https://linear.app/canary-technologies/project/configuration-drift-detection-364d47914acc\n
  \  Furthest along in substance: drift computed + cached per hotel, admin view/filter
  and\n   \"Recalculate now\" shipped. Validated read-only against ~4,600 Wyndham
  hotels, ~2%\n   drifting, no false positives. Remaining: nightly CronJob (in draft
  review), roll-up of\n   drift to root-cause master flags (raw counts overstate:
  one hotel's \"10 of 24\" was\n   really ~3 problems), coverage gaps, alerting.\n\n6.
  **Content Gateway** — Ryan Rogers · Implementation · Jun 1 → Aug 31 · also tagged\n
  \  \"1. Aspirational\" https://linear.app/canary-technologies/project/content-gateway-191c10f2fa2d\n
  \  \U0001F6A9 **Externally blocked.** Core gateway 100%, separate-DB work landed,
  Wyndham\n   compendium cutover 50% — but prod API access was promised for Jul 30
  and the vendor\n   sent an \"indefinite delay\" email instead. Still marked onTrack,
  which looks optimistic.\n   Note this also gates ENT-7093 in Managed Context.\n\n7.
  **Migrate Embedded Reporting from Explo to Omni** — Lautaro Mena · Implementation
  ·\n   Jun 15 → Sep 30\n   https://linear.app/canary-technologies/project/migrate-embedded-reporting-from-explo-to-omni-5bf86d7f3b1e\n
  \  Hard external deadline: Explo sunsets end of 2026. Omni delivered first-cut property\n
  \  dashboards, already wired into the Manage app analytics section; all still need
  work.\n\n8. **Enterprise Rollout: Segmentation for Wyndham** — Andrés Figueira ·
  Eng Design ·\n   Jul 1 → **Jul 31 (passed)** · Low priority\n   https://linear.app/canary-technologies/project/enterprise-rollout-segmentation-for-wyndham-f14fbcb66bba\n
  \  Eng design done, in review. Progress actually went *backwards* 25% → 17% (rescope).\n
  \  Includes migrating existing templated configs + letting Wyndham pre-populate
  segments.\n\n9. **IHG Scripting Changes — Pilot to Scale** — Connor Swords · Product
  Definition ·\n   started Jul 28 · no target date\n   https://linear.app/canary-technologies/project/ihg-scripting-changes-pilot-to-scale-e52e4a381d06\n
  \  15 tickets, **all still Todo/Backlog, none started.** Clusters into: translations\n
  \  (ENT-7057/7058/7059/7060), reg-card + upsell config (ENT-6979/6980/6987/7061),\n
  \  SSO roles & permissions (ENT-6985/7088), onboarding-value plumbing (ENT-7062),\n
  \  guest-journey messaging (ENT-7003/7016), branding (ENT-7015), compendium (ENT-7017).\n
  \  This is the natural follow-on to the ENT-6032 IHG HotelKey Wave 1 pilot.\n\n10.
  **Permissions Consistency: Above Property & Hotel Dashboard** — **no lead** ·\n
  \   Product Definition · started Aug 6 · no target date, no issues, no summary\n
  \   https://linear.app/canary-technologies/project/permissions-consistency-above-property-and-hotel-dashboard-8ba3a88a21ab\n
  \   Brand new (created yesterday) and completely empty. Nobody owns it.\n\n### What
  actually stands out\n\n- **Two ownership gaps:** your Portfolio Reconciliation project
  (empty, Aug 31 target)\n  and Permissions Consistency (no lead at all). Both sit
  in Product Definition doing\n  nothing.\n- **Three target dates are already blown
  or absent:** Config Drift (Jul 31), Segmentation\n  (Jul 31), and IHG Scripting
  + Permissions Consistency have no target date at all.\n- **Content Gateway is the
  only genuinely blocked-by-outside-party project** and it's\n  still flagged onTrack
  — worth a health downgrade, and it has a downstream dependency\n  (ENT-7093).\n-
  **Wyndham is the dominant theme** — Managed Context, Config Drift, Segmentation,
  and\n  Content Gateway's compendium cutover all target Wyndham. IHG is the second
  cluster.\n- Reporting/Omni has the only externally-imposed hard deadline (Explo
  sunset, end 2026).\n\nNo writes made to Linear.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Look at current ENT team Linear projects labeled for q3  block A or b. What's
  in play?
updated: 2026-08-07 13:42:16.837019
waiting_on: null
waiting_since: null
working_on: false
---