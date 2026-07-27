---
area: null
contexts: []
created: 2026-07-23 00:26:53.484976
defer_until: null
due: null
energy: low
id: 2026-07-23T0026-review-blake-s-analysis
order: null
output: |
  ## Agent run 2026-07-23T11:04:31

  Reviewed Blake's "On-Call Ticket Categorization" sheet (https://docs.google.com/spreadsheets/d/1r0WzO7tg6_UzV5rVct6IHzFyJFWkDMMnXCN49MVqeUs/edit?gid=1488368185) — 641 of 901 on-call tickets (2026-06-22 → 2026-07-22) classified by required action, root cause, gate, and AI-fixability. Verdict: the analysis is solid and its headline claims hold up. I downloaded the full workbook, recomputed every pivot from the 641-row detail sheet, and spot-checked classifications against live Linear tickets.

  **What checks out (recomputed independently):**
  - All pivot sheets (Team×Bucket, FixTier×Bucket, Gate×Bucket, RootCause×Bucket) exactly reconcile with the detail rows. No duplicate tickets. AI-Fix tier matches the 1-5 score on all 641 rows. Weighted team totals sum exactly to 901.
  - The headline automatable segment — High tier (4-5) AND no gate — is 282/641 (44%), dominated by admin-action (110) and config-permissions (53). 85% of that segment (239/282) was human-verified, so the strongest claim rests on the best-checked data.
  - Spot-checked 4 tickets from the riskiest slice (unverified + High tier) against Linear: ONC-24173 (user/sub-portfolio creation → admin-action 5), CC-2746 (dup'd email-text request → no-work), ANA-578 (auth+contract counts per user → data-lookup), INT-10179 (hotel wrongly live → admin-action/misconfig). All four classifications are correct.
  - Real PR in only 67/641 (10%); 62 of the 93 code-fix tickets have one. Supports the thesis that actual engineering code work is a small slice of on-call load.

  **Questions/nits worth raising with Blake:**
  1. Classification error rate: of the 446 verified rows, 153 (34%) needed correction. The 195 unverified rows presumably carry a similar latent error rate. Mitigated for the headline (unverified rows are 50% Human-tier and only 43/282 of the automatable segment is unverified), but worth stating the caveat wherever the 44% number is quoted.
  2. README says "gate caps the score", but 9 approval-gated tickets score 4 (ONC-24090, ONC-24124, ONC-24259, AD-7998, CC-2750, ENT-6914, MSG-5166, MSG-5186, PAY-2864). Either soften the README or re-score.
  3. Overview weighted column: bucket values sum to 903 vs the stated 901 total (independent per-bucket rounding). Cosmetic.
  4. Sampling: within-team coverage ranges from ~100% (Enterprise, Messaging) down to ~50% (PMS Engineering, In-Stay, SDM, Tipping, Voice, Payments). The weighting corrects team mix but assumes tickets were sampled randomly *within* each team — ask Blake how the 641 were selected; if it was "most recent first" there's a recency skew.
  5. Bucket convention for dead tickets is inconsistent: 80 tickets ended Canceled/Duplicate but only 26 are no-work — some dups got bucketed by disposition (CC-2746 → no-work), others by what the request would have required. Pick one rule; as-is, no-work at 4% likely understates reducible noise.

  Nothing sent externally; no comments posted. Suggested follow-up if wanted: share nits 1/2/5 with Blake.

  ## Agent run 2026-07-23T13:19:23 (follow-up Q&A with Gareth)

  **Intent & outcome, as I'd state them:**
  - Intent: replace anecdote with data on what on-call actually is — classify the ~900/30-day ticket stream by *required action* (not the unreliable Linear labels), by *why it exists*, and by *how much an AI agent could do end-to-end today*. It's a sizing exercise for automating on-call.
  - Outcome: on-call is mostly not engineering. Only ~15% needs a code fix (10% ever produced a PR). The bulk is routine ops — admin-action 26% (dominated by process-requests: user creation, account changes) and config-permissions 20% (dominated by misconfig). ~44% of the whole load is High AI-fixable with no blocking gate, concentrated in exactly those buckets; the Oncall and Tipping Orders queues are 80–92% automatable. The irreducibly human ~30% is product decisions and vendor/approval-gated work. Practical conclusion: an agent with admin tooling (not a code-writing agent) could plausibly absorb nearly half of on-call.

  **What "Corrected" means:** the sheet stores only a boolean set during Blake's verification pass — no before/after values, so the changed field isn't recoverable from the workbook (only Google revision history or Blake could say). Inference from final values: corrected rows are 41% High-tier vs 63% for rows that passed verification untouched (and 35% vs 15% Human-tier), consistent with the initial pass over-rating automatability and verification reining it in. So the 44% headline would more likely shrink slightly than grow under full verification. Corrections were NOT just the label-lied tickets (37% lied among corrected vs 42% among unchanged). Suggest Blake record a correction-type/before→after column next time — the flag gives error rate but not error direction.

  **Which labels were most misapplied (Label Lied = 205 tickets):** the sheet doesn't record the offending label, so I joined all 205 flagged tickets back to Linear (read-only, via 5 parallel agents) and compared their live labels to Blake's ground truth:
  - **"Bug" is the main offender**: on 90 of 205 lied tickets, and only 4 of those 90 were actually defects — 42 were misconfigs, 26 knowledge gaps, 8 product gaps, 8 noise. Their real buckets: config-permissions 27, data-lookup 22, explain-answer 16. I.e. hotels/CS file config problems and how-do-I questions as "Bug".
  - **"Troubleshooting: Integration Sync" (41)** — really misconfig 19 / knowledge-gap 11 / defect only 5. **"Troubleshooting: Other" (34)** — misconfig 23. **"Troubleshooting: Message Logic" (32)** — spread across misconfig/knowledge-gap/product-gap.
  - Pattern: the taxonomy systematically dresses up misconfigurations and knowledge gaps as product defects. Matches the lie-rates by root cause (knowledge-gap 67%, misconfig 52% vs defect 18%, process-request 7%) and by team (Integrations 51%, PMS Eng & Messaging 43% vs Oncall queue 7%).
  - Caveat: Blake's flag is per-ticket, not per-label; attributing which label lied is my inference from label-vs-classification conflict. Rates are among lied tickets only (no label base-rates for the 436 clean tickets — would need another 436 Linear fetches).
  - Working files (local scratchpad, not the spreadsheet — sheet untouched): blake.xlsx, labels.json in session scratchpad.
project: null
source_id: null
tags: []
time_minutes: 5
title: REview Blake's analysis
updated: 2026-07-23 13:25:32.551737
waiting_on: null
waiting_since: null
working_on: false
---

https://docs.google.com/spreadsheets/d/1r0WzO7tg6_UzV5rVct6IHzFyJFWkDMMnXCN49MVqeUs/edit?gid=1488368185#gid=1488368185