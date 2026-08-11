---
area: null
completed_at: 2026-08-10 17:07:26.167042
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

  ## Agent run 2026-08-07T15:53 — conclusions

  Went back through the data to test the first pass rather than extend it. Two of my earlier
  claims did not survive. Conclusions below, then the corrections.

  ### The conclusion

  **EMEA activation is a queueing problem running at a structurally sub-critical service rate.
  It is not a blocker problem, not a capacity-never-scaled problem, and not a portfolio-deal
  mix problem — I tested all three and all three are second-order.**

  Trailing 12 months (2025-08-01 → 2026-08-01): **2,635 SKU-lines signed, 1,157 activated.**
  Net +1,478 to the backlog. **Activation throughput must rise ~128% just to hold the backlog
  flat**, before any talk of reducing it.

  Steady-state WIP = inflow ÷ service rate ≈ **7,300 open lines against 2,755 today**. On
  current inflow and current service rate the backlog is at ~38% of its equilibrium size and
  has roughly **2.7x still to grow before it stabilises** — with no further deterioration
  assumed. The problem gets substantially worse from here on autopilot.

  ### Why it is not the three obvious explanations

  **Not blockers.** Named blocked reasons total $650k of $3.86m backlog CARR (17%). Strip the
  mis-tagged theme and genuinely actionable product gap is ~$180k — **4.7% of backlog**.
  Clearing every product blocker in the dashboard would not move the aggregate.

  **Not "capacity never scaled" — I got this wrong first time.** Activation throughput scaled
  ~10x (102 lines/half in 2024-H1 → 1,013 in 2026-H1). The activated:signed ratio has been
  stable at **48–58% since 2024**. The team did scale. But a persistent ~45% shortfall applied
  to a 9x-growing base compounds: WIP went 77 → 2,802 lines (36x) while throughput grew 14x.
  The deficit is structural, not a capability failure.

  **Not deal mix.** Large portfolio batches do activate worse — 365d activation is 67–68% for
  1–4 hotel deals vs **27–35% for 10+ hotel batches** — and the mix genuinely shifted (0% of
  signings in 10+ hotel batches in 2022 → 35% in 2026-H1). But shift-share (2024-H1 → 2025-H2,
  180d horizon, 60% → 28%) attributes only **-5.6pp (18%) to mix and -30.6pp (98%) to
  within-segment deterioration**. Single-hotel deals alone fell from 70% → 32%. The rot is
  everywhere, not in the enterprise segment.

  ### Corroborating: the team is grinding an aging queue

  Median age of work at the moment it activates: 47d (2024-H1) → **122d (2026-H1)**. Share of
  activations that are on work over 180 days old: 10% → **36%**. Backlog as a share of CARR:
  20% (2024-01) → 33% (2026-07), with backlog ARR growing 30x against LIVE_ARR's 15.6x.

  Little's Law implies a wait of 600–1,200 days against an actual median lag of ~100d — the gap
  means the queue is emphatically **not FIFO**. Work is being selected, and a large aged
  population is being passed over repeatedly.

  ### Two corrections to my 2026-08-06 output

  **1. There is no "point of no return", and the terminal-rate figures were wrong.** I reported
  terminal activation of ~46% for 2025 cohorts and, in working, a 2.5% conversion rate for
  lines open past 365 days. Both were right-censoring artifacts — lines that reach 365 days
  late in the window have almost no remaining observation time, so they can only ever look
  dead. Re-run requiring a full observation window after each age threshold:

  | still open at | activates within next 12mo |
  | --- | --- |
  | 180 days | 37.5% |
  | 270 days | 36.4% |
  | 365 days | **35.9%** |

  The hazard is **flat at ~36%/yr, not cliff-shaped**. Aged backlog is a slow-converting
  annuity, not dead stock. A model of "~25% activate by 90d, then flat 36%/yr" reproduces the
  observed 2024-H2 (62.4% obs vs 60.8% model) and 2025-H2 (45.2% vs 42.3%) cohort curves.
  Forward projection of today's open backlog: ~43% activates within 1y, ~64% within 2y, ~77%
  within 3y. So my "$2.1m at risk" number should be retired — the money mostly arrives, just
  ~23 months late at the median.

  That reframes the ask. The problem is not write-off risk, it is **cash-flow timing and
  compounding WIP**.

  **2. "Slow activation drives churn" is not supported here — but the data cannot see it.**
  Only 5 SKU-lines ever churned without first activating. Churn rate by activation speed is
  non-monotonic (17.5% for ≤30d vs 2.3% for 181–365d) and confounded by tenure. No usable
  signal. **However**: `emea_events.json` has no "abandoned" event type, so signed-not-activated
  is an absorbing state that can only exit via activation. Dead backlog is structurally
  invisible and reported CARR is inflated by an unknown amount. Absence of evidence, not
  evidence of absence.

  ### One data trap worth knowing

  The LIVE_ARR jump from $2.1m (2025-10) to $5.0m (2026-01) is **three Wyndham Global Solutions
  lines worth $2.76m** (AI Voice + AI Webchat, booked at parent-brand level). Any ARR-weighted
  activation statistic spanning 2026-H1 is dominated by those three rows. Count-based analysis
  is unaffected and is the honest lens for throughput. Signed ARR itself is not badly
  concentrated (top 10 lines = 11.3% of trailing-12mo signings), and the median hotel-level
  line is **$893** — the backlog is thousands of small lines, not a few big ones.

  ### What follows from this

  - **The binding constraint is service rate, and unblocking cannot reach it.** Named blockers
    are 17% of backlog; the gap to be closed is 128% of current throughput. These are not the
    same order of magnitude. Any plan built on clearing blockers will miss.
  - **Three levers actually sized to the problem**: raise service rate structurally (self-serve
    activation, cut per-property touch time); reduce the unit of work (fewer SKU-lines
    committed at signature — a hotel signing 6 products creates 6 queue items); or reshape
    inflow (phased activation commitments on portfolio deals rather than all-lines-at-signature).
  - **Portfolio deals are still worth a specific policy** even at 18% of the effect — they are
    the cleanest place to apply phased activation, and the batch-size gradient is steep.
  - **The $1.79m undiagnosed backlog is now the top data task**, unchanged from yesterday. With
    blockers ruled out as the aggregate driver, the undiagnosed half is where any remaining
    surprise lives.

  ### Confidence and caveats

  - Throughput, WIP, cohort and hazard figures are count-based and I consider them solid.
  - The 36%/yr hazard is measured on 2024-H2 + 2025-H1 and assumed stable forward. If service
    discipline changes it moves. It is the single load-bearing assumption in the projection.
  - 2026-H1 cohort rates are 72% mature at 90d and less beyond; the apparent 180d rebound to
    53% rests on the January slice only and should not be read as recovery.
  - Equilibrium WIP assumes inflow holds at the trailing-12mo rate. `emea_pipeline.json`
    (4,482 open opportunities) suggests inflow rises rather than falls, which makes the
    projection conservative.
  - All analysis re-runnable from `~/projects/analysis/emea-slow-activation/`. No external
    writes made.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: Extract blocked reasons from this, ready for further analysis steps
updated: 2026-08-10 17:07:26.167024
waiting_on: null
waiting_since: null
working_on: false
---

https://emea.cnry.land/dashboards/emea-kpis/index.html

While reviewing, see what other interesting data might support an analysis of slow activation