---
area: null
completed_at: null
contexts: []
created: 2026-08-05 11:15:30.410681
defer_until: null
due: null
energy: low
id: 2026-08-05T1115-analysis-of-blocked-reasons
order: 1
output: |
  ## Agent run 2026-08-06T15:20

  ### Where the data actually lives

  The dashboard (https://emea.cnry.land/dashboards/emea-kpis/index.html) is a **private GitHub
  Pages** site — `curl`/WebFetch get a 302 to `github.com/pages/auth`, so it can only be read in
  a logged-in browser. But it's a static page reading four JSON files, and those are fetchable:

  - Repo: `canary-technologies-corp/emea-pod-hub`
    (https://github.com/canary-technologies-corp/emea-pod-hub) → `dashboards/emea-kpis/data/`
  - `git clone` fails under org SAML SSO; `gh api -H "Accept: application/vnd.github.raw" ...`
    works.

  **Extract written to `~/projects/analysis/emea-slow-activation/`** — `raw/` (the four JSONs),
  `extract.py` (re-runnable), `out/` (5 CSVs), `README.md` (schema, refresh command, caveats).

  ### Blocked reasons — the extraction you asked for

  Snapshot `AS_OF = 2026-08-01`. Only `emea_funnel.json` carries `BLOCKED_REASON`, and only on
  `backlog` rows. Backlog = **$3,858,759 CARR / 2,313 product-rows / 455 accounts**.

  | Blocked reason | rows | CARR | % of backlog CARR |
  | --- | --- | --- | --- |
  | **(none recorded)** | 865 | $1,793,955 | **46.5%** |
  | Pilot | 624 | $1,244,681 | 32.3% |
  | Customer Internal Blocker | 264 | $292,734 | 7.6% |
  | Phased Rollout | 206 | $255,810 | 6.6% |
  | Product Blocker | 284 | $233,052 | 6.0% |
  | Property Opted Out | 70 | $38,527 | 1.0% |

  Five values, closed list. Collapsed to opportunity grain: **348 blocked opportunities across
  320 accounts**, every one with a `NOTE_SUMMARY` (→ `out/blocked_opportunities.csv`).

  ### The hidden layer worth knowing about

  The funnel rows have **inconsistent key sets**. 284 rows (all the Product Blockers) carry two
  extra fields the summary table above hides — `THEME` and `THEME_BLOCKER` — plus 1,448 rows
  carry `NOTE_SUMMARY`. These are **LLM-generated summaries of Salesforce opportunity notes**
  baked in upstream, not raw CRM fields. The themes are already a finished piece of analysis:

  | Theme | CARR | Hotels |
  | --- | --- | --- |
  | *Not a product gap (mis-tagged)* | $53,155 | 18 |
  | Guestline credit-card pass-through & tokenization | $45,224 | 16 |
  | Clock PMS two-way integration (GreenStar) | $36,464 | 5 |
  | Long-tail bespoke integrations (one-off systems) | $27,597 | 11 |
  | Oracle Opera/IHG connectivity issues | $19,788 | 2 |
  | AI automation for apartment/agency accounts | $12,878 | 2 |
  | WhatsApp/messaging setup & delivery issues | $10,456 | 3 |
  | Host PMS two-way integration (Portugal) | $10,000 | 4 |
  | GJM check-in/review/upsell feature gap | $8,196 | 2 |
  | Payment gateway integration & certification | $5,094 | 3 |
  | PMS arrivals-report ingestion capability | $4,200 | 1 |

  Note the top entry: **23% of "Product Blocker" CARR is mis-tagged** and isn't engineering work
  at all. Real actionable product gap is ~$180k — small. Product blockers are *not* the story.

  ### The story is elsewhere — three findings that matter more

  **1. Nearly half the backlog has no diagnosis.** $1.79m (46.5%) across 200 accounts has no
  blocked reason recorded. And 243 rows / $551k have no `ONBOARDING_LEAD` — **all** of which
  also have no reason, so the field looks like it's only populated where a lead exists. The
  biggest single "reason" for slow activation is that nobody has written one down.

  **2. 90-day activation rate has collapsed ~4x while signature volume went up ~9x.** From
  `emea_events.json`, per sign-cohort (all cohorts through 2025-H2 fully mature at 90d;
  2026-H1 is 72% mature):

  | Sign cohort | signed | activated ≤90d |
  | --- | --- | --- |
  | 2022-H2 | 57 | 68.4% |
  | 2023-H2 | 101 | 47.5% |
  | 2024-H1 | 199 | 43.2% |
  | 2024-H2 | 407 | 24.8% |
  | 2025-H1 | 987 | 18.4% |
  | 2025-H2 | 916 | **11.2%** |
  | 2026-H1 | 1,729 (72% mature) | 17.2% |

  Overall signed→activated lag: n=2,055, median **99d**, mean 125d, p90 278d, max 1,744d.
  By suite: GMS median 114d (n=1,531) vs SDM 25d (n=273) — GMS is where the time goes.
  Currently **2,761 signed SKU-lines never activated**; median age 182d, **811 over a year**,
  55 over two years.

  This reads as capacity-bound, not blocker-bound: bookings scaled, activation didn't.

  **3. "Pilot" is the largest *named* reason at $1.24m and is essentially two accounts.** The
  top 25 blocked opportunities are dominated by one IHG/LGH pilot cluster (Isaac Sheahan CSM /
  Sam Stead lead — "Piloting 5 properties; rollout blocked until GMS, Kiosk, Voice features
  complete") and the Grecotel/Caramel 6-month pilot (Aksel Rodriguez). Two Accor properties
  are explicitly deferred to 2027. So a third of blocked CARR hinges on a handful of pilot
  exit decisions — worth tracking as named bets rather than as a funnel category.
  (Grecotel ties to the at-risk pilot already in my notes.)

  ### Other data on that dashboard that supports a slow-activation analysis

  - `emea_events.json` (8,078 rows) — `signed`/`activated`/`churned` per account × SKU with
    `IMPLEMENTATION_LEAD`, `COUNTRY`, `MANAGEMENT_COMPANY`, `BRAND`. **The single most useful
    file**; everything in finding 2 comes from it. Supports cycle-time cuts by lead, country,
    management company, and PMS-proxy.
  - `emea_monthly.json` (743 rows, from 2018-01) — `LIVE_ARR` / `BACKLOG` / `CARR` by month ×
    product. The *only* historical view of the backlog gap; lets you show the backlog widening
    over time rather than just its size today.
  - `emea_pipeline.json` (4,482 rows) — open opportunities with `STAGE`, `PROBABILITY`,
    `CLOSE_DATE`, `CREATED_DATE`, `LAST_STAGE_CHANGE`. Pre-signature, so it sizes the
    *incoming* activation load against a capacity line that's already behind.
  - Owner concentration (blocked backlog CARR): Sam Stead $712k / 40 accts, Aksel Rodriguez
    $454k / 57, Isaac Sheahan $265k / 32, Cristina Zago $214k / **84 accts**. Very uneven
    account-count-to-value ratios — a load-balancing question.
  - Backlog by product: Guest Messaging $686k, AI Voice $520k, Kiosk $442k, Check-in $399k.
    Kiosk is notable — $442k backlog with **zero** rows tagged Product Blocker, Customer
    Internal Blocker, Phased Rollout or Opted Out. It's all `(none)` or `Pilot`.

  ### Gaps to be aware of before going further

  - Blocked reason is a **snapshot with no history** — you can't measure how long something has
    been blocked. I proxied age via first signature date at the account. A weekly capture of
    `emea_funnel.json` would fix this going forward and is cheap.
  - Age × reason cross-tab shows Phased Rollout and Product Blocker skew old (26 and 31
    accounts in the 1–2y bucket) while Pilot skews new — consistent with pilots being live
    decisions and product blockers being parked.
  - 13 SKU-lines activate before they sign (negative lag). Noise, ignorable.

  ### Suggested next steps

  1. Chase the $1.79m undiagnosed backlog — that's the analysis-blocking gap, and it may
     largely be the unassigned-lead cohort.
  2. Frame the deck around cohort activation rate (finding 2), not blocked-reason mix.
  3. Start snapshotting `emea_funnel.json` weekly so blocked-duration becomes measurable.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: Extract blocked reasons from this, ready for further analysis steps
updated: 2026-08-06 15:20:41.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://emea.cnry.land/dashboards/emea-kpis/index.html

While reviewing, see what other interesting data might support an analysis of slow activation