---
area: null
contexts: []
created: 2026-07-23 15:55:47.938153
defer_until: null
due: null
energy: low
id: 2026-07-23T1555-review-omni-revamp
order: null
output: |
  ## Agent run 2026-07-23T16:20

  Reviewed the "Customer Insights Revamp" Notion doc
  (https://app.notion.com/p/canarytechnologies/Customer-Insights-Revamp-39681468615180a1aae7ddf47f7e637a).

  **What it is:** The page has no prose at all — it's just an inline database,
  "Customer Insights Metrics" (https://app.notion.com/p/49a34f4bcd234d25919de8cb5edcacfc),
  with 66 rows (65 metrics + 1 empty row) across 13 products. Columns: Category
  (New / Needs Clarification / Remove), Product, Definition, Suggested Visualization,
  Adoption-vs-ROI tag, Status, Requested By Customer. Context from Bear: Omni is our
  internal BI tool on Snowflake and Explo powers today's customer-facing insights, so
  the "omni revamp" is presumably re-platforming Customer Insights — but the doc never
  says so. No prior notes/opinions of yours on this initiative in Bear.

  **Review findings:**
  1. It's a metrics wishlist, not a design doc — no problem statement, personas
     (GM vs portfolio), prioritization, phasing, or tech approach (Explo vs Omni
     unmentioned). ~57 of 65 rows are bare names with no definition; only ~8 rows
     (the CS-submitted, customer-attributed ones) have substance.
  2. Direct contradiction to resolve: "Guest Journey Deliverability & Delivery
     Failure Reasons" is marked **Remove** (Athenaeum InterContinental, "requested in
     every weekly call") while "Guest Journey deliverability" is marked **Needs
     Clarification** asking to *show* failure reasons like "phone number not in PMS"
     (Mayfair Townhouse). Same metric, opposite asks. Showing failure reasons would
     satisfy both; silently removing it won't stop the questions.
  3. Several rows are features, not metrics: "Better Reporting Exports" (branded
     full-report download, Athenaeum), "Actionable GJ flow" (per-guest delivery
     status, Cortiina Munich), bad-phone-number report (Doyle Collection). These
     deserve a separate feature track or they'll get lost in a metrics table.
  4. Estimated-ROI metrics ("mins saved staff/guest", "time saving estimate",
     "paper savings", "# chargebacks lost") repeat across 6+ products with no
     methodology. Needs one shared, defensible formula per concept or these get
     challenged in QBRs.
  5. Double-counting risk: upsell revenue appears under Upsells, Checkout,
     Compendium, Kiosk, and Voice AI — needs attribution rules before anyone sums
     a portfolio dashboard.
  6. Already-known infeasible row kept in the list: "# plastic keys saved" (Mehul's
     note: no physical-key data from lock servers) — should be marked out of scope.
  7. Hygiene: one fully empty row; truncated metric name "% conversion rate to
     booking versus" (Webchat); Status column barely used (everything "Logged" or
     blank); no impact/effort/priority column; 6 product options have zero rows
     (Payments, Authorizations, Contracts, Analytics, Enterprise Core, Mobile SDK) —
     unclear if out of scope or just not gathered yet.
  8. Strongest signal in the data: the Check-In Funnel (drop-off per step, requested
     by Eurostars, Grecotel, DeLuna + 2 QBRs) — likely the highest-value item and
     the one with real engineering implications (funnel eventing/instrumentation),
     along with GJ delivery-failure reasons (data largely exists in Twilio status
     callbacks).

  No comments posted to Notion; review is local only. If you want, next step could
  be drafting these as Notion comments on the doc for approval.
project: null
source_id: null
tags: []
time_minutes: 5
title: review omni revamp
updated: 2026-07-24 10:42:08.183518
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Customer-Insights-Revamp-39681468615180a1aae7ddf47f7e637a?source=copy_link