---
area: null
contexts: []
created: 2026-07-28 15:15:03.936759
defer_until: null
due: null
energy: low
id: 2026-07-28T1515-review-this-doc
order: null
output: |
  ## Agent run 2026-07-28T15:45

  Reviewed https://pages.cnry.cloud/epd-q2-recap — a self-contained interactive
  Q2 2026 EPD Quarterly Product Business Review dashboard (3 tabs: Q2 Overview,
  By Product, GTM Metrics; data from Salesforce/Maxio/Gainsight).

  ### Verified consistent
  - By Product tab sums match headline tiles: bookings $7.39M ≈ $7.4M,
    activations $7.07M ≈ $7.1M, churn exactly $882K.
  - Net New ARR $6.5M = bookings − churn. Exec-summary claims check out
    (AI Voice $964K + AI Webchat $275K = $1.24M; Kiosk $575K bookings, zero churn).
  - Churn table's per-product plans sum to its $1.0M total (86% attainment).
  - Rendering is clean (charts, tables, expandable tiles all work).

  ### Issues worth fixing before it circulates
  1. INCONSISTENCY — Churn tile says "vs Plan: $1.4M" but the Churn by Product
     table totals plan at $1.0M / 86%. One of the two is wrong.
  2. MISLEADING TILE — Total Bookings "$7.4M vs Plan: $26.1M" reads as 28%
     attainment at the very top of the page while the summary calls it a record
     quarter. Expanding the tile shows per-product plans that look annual or
     enterprise-deal-inflated (Guest Messaging plan $5.2M vs $1.7M actual,
     Upsells $4.2M vs $802K). The footnote at the bottom acknowledges this, but
     it should either sit next to the tile or the plan should be restated on a
     comparable quarterly basis. Activations plan ($7.6M) is comparable, which
     makes the bookings plan look even more out of place.
  3. FRAMING — "Churn contained" while churn is +13% QoQ, with Digital
     Authorizations +31% and Guest Messaging +41% QoQ, and several products well
     over churn plan (Check-Out 201%, Digital Compendium 287%, AI Voice 210%,
     Contactless Check-In 120%). Contained vs plan overall, yes — but the QoQ
     direction is up; a one-line driver explanation would preempt questions.
  4. TREND CHART GAP — "Quarterly Trend" plots Q2 2025 → Q1 2026 → Q2 2026,
     silently skipping Q3/Q4 2025; reads as consecutive quarters. Label the
     first bar "YoY" or include the missing quarters. (Footer also says data
     window "Q1 2025 – Q2 2026" while the chart starts at Q2 2025.)
  5. MINOR — Page <title> is "App Artifact"; name it. "Conv %" in the campaigns
     table is undefined. Several 2024-dated campaigns ("2024.04 IHG Digital
     Authorizations", "2024.04 Choice Convention") are top primary sources for
     Q2 2026 wins — worth a sanity check on campaign attribution staleness.

  No edits made anywhere; review only. I don't know who authored the page, so no
  feedback has been sent to anyone — findings are only recorded here.
project: null
source_id: null
tags: []
time_minutes: 5
title: review this doc
updated: 2026-07-29 14:30:01.491854
waiting_on: null
waiting_since: null
working_on: false
---

https://pages.cnry.cloud/epd-q2-recap