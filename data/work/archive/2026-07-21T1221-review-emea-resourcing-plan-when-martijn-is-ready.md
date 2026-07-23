---
area: null
contexts: []
created: 2026-07-21 12:21:32.074550
defer_until: null
due: 2026-07-22
energy: high
id: 2026-07-21T1221-review-emea-resourcing-plan-when-martijn-is-ready
order: null
output: |
  ## Agent run 2026-07-22T14:14

  Reviewed Martijn's **Capacity Plan EMEA 2026** (Notion:
  https://app.notion.com/p/canarytechnologies/Capacity-Plan-EMEA-2026-3958146861518096b54af101aef8ab01).
  Ask: grow EMEA pod 3 → 4 (one Senior eng), moving ~40% of the pod to
  strategic roadmap while keeping reactive coverage intact.

  **Verdict:** Well-structured, approvable case — but it has 3-4 holes an
  approver will poke. Support it, but push Martijn to patch these before it
  goes up, or it invites a cheaper counter-proposal.

  **1. Biggest hole — the Adil question (fix first).** The doc's own Context
  section concedes a 4th head already exists (Adil) but is on Crown Resort
  APAC work, "so the pod is effectively at three." An approver (finance/exec)
  will immediately ask *why hire net-new instead of reclaiming Adil?* As
  written, the plan hands them the cheaper answer. Needs to preempt this:
  why Adil isn't returning (APAC ownership / Crown commitment + duration),
  and reframe the ask as "restore EMEA to 4 net," not "grow to 4." Your own
  1:1 notes corroborate the strain (Adil→APAC, Martijn absorbing the gap,
  pressure spilling onto Peter) — that's real ammunition the doc omits.

  **2. Internal contradiction in the capacity math.** Claim: hire frees ~40%
  for strategic "while keeping today's reactive coverage intact." The numbers
  say otherwise:
    - Current reactive bucket (strat accounts 35 + activation 25 + boutique 15
      = 75%) × 3 eng = **2.25 eng**.
    - Proposed reactive bucket 40% × 4 eng = **1.6 eng**.
    - That's a ~29% *cut* to reactive coverage — not "intact." And the doc
      simultaneously argues activation demand is *rising* (AP / Detail /
      Hotel Hotels pipeline) and a PM will add to the queue. So the plan
      reduces reactive capacity exactly as reactive demand grows.
    - Fix: either soften "intact," dial the strategic split to something
      defensible (~1 eng / 25%), or state the explicit assumption that
      reactive load will be actively deflected/triaged down.

  **3. Quantification is thin and mis-weighted.** Only WhatsApp calling carries
  a $ figure (~$22K, mostly small properties). The items that actually justify
  the pod — GDPR PII anonymization + EMEA compliance integrations — are the
  regulatory/"we're currently non-compliant" lever and are quantified only
  qualitatively. For exec approval, put a hard number/consequence on the top
  line: blocked ARR from Danubius/IHG DPA negotiations, fine exposure, deal
  size at risk. Right now a $22K WhatsApp feature reads louder than the
  compliance obligation, which inverts the real priority.

  **4. No alternatives-considered.** Approvals reward "we looked at cheaper
  options first." Missing: (a) pull Adil back, (b) CS triage / self-serve to
  deflect reactive load, (c) borrow vertical-team capacity for a fixed-term
  compliance push, (d) drop/defer the Medium roadmap items. One short
  "alternatives considered & why rejected" block beats the implicit "just
  give us a head."

  **Smaller points:**
    - PM framing is a self-inflicted wound — doc says the incoming PM "adds to
      the queue rather than shortens it." Reframe: a PM prioritizes and
      deflects, protecting strategic capacity. That's an argument *for* you.
    - Leveling (Senior) is well-justified (autonomy cuts vertical-team review
      load; level spread aids retention). But the candidate bar (FE/BE/mobile
      context-switch, self-sufficient, owns end-to-end) is high, and
      time-to-fill + 2-3mo ramp means relief lands **H2 2026**, not now — set
      that expectation so approval isn't judged on immediate impact.
    - Sanity-check the headline "3 engineers." Worth confirming the baseline
      number is unambiguous vs. how the pod is counted elsewhere.

  **Bottom line for you:** back the ask, but before it goes up have Martijn
  (a) preempt "why not Adil," (b) fix the "coverage intact" contradiction,
  (c) put hard numbers on the GDPR/compliance top line, (d) add a one-line
  alternatives-considered. Those are exactly the four points an approver hits.

  No external writes made (no Notion comment posted) — draft review is local
  only, per protocol. Say the word if you want any of this posted as a Notion
  comment or sent to Martijn.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: review EMEA resourcing plan
updated: 2026-07-22 15:58:04.499545
waiting_on: null
waiting_since: null
working_on: false
---

§https://app.notion.com/p/canarytechnologies/Capacity-Plan-EMEA-2026-3958146861518096b54af101aef8ab01?source=copy_link