---
area: null
contexts: []
created: 2026-07-23 16:07:10.991623
defer_until: null
due: null
energy: low
id: 2026-07-23T1607-review-doc-costs-to-serve
order: null
output: |
  ## Agent run 2026-07-27T14:30:00

  Read the doc (https://pages.cnry.cloud/cost-to-serve) and reviewed it. No prior
  Bear notes on it. Review below — nothing has been sent anywhere; use/adapt as
  feedback to the author.

  ### Overall
  Solid v1 framing. The stock-vs-flow distinction (active hotels vs product
  activations) is exactly right, the per-cost-center owner + lever + guardrail
  structure is good, and the data-readiness table plus "discussion drafts, not
  validated reporting" disclaimer is honest. Main gaps are in how the unit
  economics will behave once real numbers land.

  ### Substantive points (roughly by importance)
  1. **The two halves never connect.** Contribution per hotel = ARR − recurring
     cost only; get-live cost is computed but never amortized against anything.
     Suggest a payback-style metric (months of contribution to recover
     cost-to-get-live) so one-time and recurring tie together — otherwise the
     one-time number has no "so what".
  2. **Blended cost-per-activation is mix-sensitive.** Activations are treated as
     equal units, but implementation effort differs a lot by product. A shift in
     product mix moves the headline number with zero efficiency change. The doc
     says most cost centers split by product — make the by-product cut the
     primary view, blended only secondary.
  3. **New-hotel vs expansion activations should be split.** An existing hotel
     adding one product is much cheaper to activate (no kickoff, PMS already
     connected) than a new hotel's first product. Blending them distorts the
     unit cost and rewards/punishes the team for sales mix.
  4. **Integrations doesn't fit "one-time ÷ activations".** Connector *build* is
     an R&D-ish cost amortized across every hotel on that connector (their own
     "hotels per connector" lever hints at this); connector *maintenance* is
     recurring. Dumping connector-build labor into a period's activations will
     make cost-per-activation spiky and misleading. Suggest splitting build
     (amortize) vs connect-a-hotel (per activation) vs maintain (recurring).
  5. **Averages will hide the long tail.** Allocating fully loaded cost evenly
     across hotels served assumes uniform consumption; support load is famously
     Pareto-shaped. "Tickets per hotel" exists as a lever but recommend a
     distribution/outlier cut too — the actionable lever is usually the top-5%
     hotels, not the mean.
  6. **"% on support" for Engineering support is the softest input.** How is it
     measured — self-report? Suggest validating against Linear triage labels or
     time-boxed sampling before anyone anchors on that number.
  7. **Labor-only scope vs the name.** "Cost to serve" invites gross-margin
     comparisons, but COGS (hosting, Twilio/SMS, LLM inference, payment
     processing) is out of scope. Worth one explicit sentence saying this is
     labor-only and COGS is separate, before Finance runs with it.
  8. **Consistency checks worth stating:** (a) ARR-per-hotel numerator and
     denominator must both exclude enterprise; (b) segment the cost metrics
     (SMB vs mid-market), not just the levers — blended ARR/hotel across
     segments hides the economics the doc says it wants; (c) period alignment
     for the flow metric (cost incurred vs activation completed straddling
     period boundaries — fine quarterly, noisy monthly).

  ### Minor
  - "Cost-to-serve % of revenue" uses recurring cost only — name it
    "keep-running % of revenue" or similar to avoid ambiguity with the doc
    title.
  - Churned hotels' sunk get-live cost is invisible; retention is a guardrail
    only on CS. Fine for v1, worth a "future work" mention.

  Next step (yours): pass feedback to the doc author — the doc invites
  corrections but doesn't name the author; owners listed per cost center are
  Rachel Weller, Sharon, Diego Guzman, Nensy, Laura.
project: null
source_id: null
tags: []
time_minutes: 5
title: Review doc - costs to serve
updated: 2026-07-27 14:23:08.778949
waiting_on: null
waiting_since: null
working_on: false
---

https://pages.cnry.cloud/cost-to-serve