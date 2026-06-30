---
area: null
contexts:
- consume
created: 2026-06-29 11:06:11.017230
defer_until: null
due: null
energy: low
id: 2026-06-29T1106-review-compendium-aem-integration-doc
order: null
output: |
  ## Agent run 2026-06-29T14:53Z — Review of AEM→Wyndham Compendium design doc

  **Doc:** "Adobe Experience Manager Integration for the Wyndham Compendium" (Notion, status REVIEW ME!)
  https://app.notion.com/p/canarytechnologies/Adobe-Experience-Manager-Integration-for-the-Wyndham-Compendium-3838146861518023a5d9dd280a380367
  **Ticket:** ENT-6353 [Eng Design] AEM Integration — In Review — https://linear.app/canary-technologies/issue/ENT-6353/eng-design-aem-integration
  **Project:** "CMS Gateway - Enable Canary to retrieve content from Customer CMSs" (so the generic framing is a stated project goal, not author scope-creep).
  **Author:** Ryan Rogers. **Existing feedback:** one round of inline discussions already resolved in-doc; one reviewer already approved ("love where this ended up"). My pass below is complementary — not re-raising settled points.
  **Source Slack ping:** https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781820216676709

  ### Overall verdict
  Strong, well-researched design — recommend approving the *direction* with the concerns below addressed (most can be resolved in the design, none are show-stoppers). The architecture is sound and the doc is honest about what's unknown. I verified the load-bearing code claims against the repo (subagent sweep): 9/10 exact, 1 off by ~5 line numbers (the rollout recipe is at rollouts.py:118–126, doc says ~113-120), and the one "false" claim is the proposed `content_gateway/` app being net-new (expected). CODEOWNERS confirms the ownership argument: `compendium/ @pod-in-stay`, `onboarding/ @pod-enterprise`, `hr_gateways/ @pod-tipping` — so placing the core in an ENT-owned app and only crossing into compendium.* through the existing ENT provider is correct. Note: the section it creates today is titled "Wyndham Offers" (line 258), confirming the doc's planned "Wyndham Rewards Offers" retitle.

  ### Strengths
  - Excellent problem framing — the manual-transcription / manual-S3-upload / no-expiry / no-self-serve pain is concrete and the design targets each.
  - Right core architecture: fetch-once-into-snapshot-then-populate, not call-AEM-per-hotel (correctly rejected: ~500 calls/rollout, no last-known-good).
  - Genuinely low blast radius — per-hotel write path, models, rollout, guest API all unchanged; only the offer *source* and image acquisition change.
  - Robust safety story: last-known-good fallback, never-wipe-on-empty, atomic generation commit, draft→approved human gate, clean DRAFT/APPROVED vs AEM-publish terminology split.
  - Leans on real, verified repo precedents (hr_gateways sync, gql/Expedia client, mulesoft Network+plugin, ImageService hash-dedup, EncryptedCharField).
  - Failure-modes table + alerting/runbook section are unusually complete for a design doc.

  ### Substantive concerns / questions (ordered by importance)
  1. **YAGNI on the generic framework — biggest call.** Phase 1 has exactly ONE concrete wiring (AEM→Wyndham), yet the doc models the full abstraction: SourceConnector/SourceConfig/SourceMapper/SourceSnapshot/ContentGatewayService + target_kind + scope_kind/scope_key + a registry. The second consumer (Best Western, credit-card offers) is explicitly speculative ("no BW input yet"). Abstractions guessed from one example are usually wrong on the second. The Phase-5 principle "if the core needs edits to fit BW, the abstraction is wrong" is nice but unfalsifiable until BW is real. **Ask:** which generic machinery is actually built in phase 1 vs. deferred? Recommend building the Wyndham path concretely behind clean seams and deferring the full registry/target_kind/scope dimensions until consumer #2 exists. The project being named "CMS Gateway" justifies the *intent*, not necessarily building all of it now.

  2. **The /manage self-serve UI is large net-new scope coupled to the MVP goal.** The fetch-button + preview + diff-against-live + approve flow (staff-gated internal_support, MFA, snapshot/diff rendering) is meaningful FE+BE work, and the doc admits it's net-new. The core goal ("remove Canary eng from the content loop") is achievable in phase 1 with a CLI sync + manual staged rollout (eng-run); the /manage UI is what makes it *ops* self-serve. **Ask:** can phase 1 ship CLI-only and defer the UI? If the UI slips, eng is still in the loop. Worth an explicit MVP-cut decision rather than bundling.

  3. **Empty-result safety rail conflicts with "liveness = publish/unpublish".** Two stated principles tension: (a) "publish-tier query returns only live offers, snapshot mirrors exactly what Wyndham publishes — no date logic our side"; (b) "AEM empty → do NOT wipe; require an explicit 'intentionally empty' signal." If Wyndham legitimately unpublishes all offers (all promos ended), the design is built to *not* reflect it — contradicting the mirror principle. **Ask:** define the "intentionally empty signal." The whole point is Wyndham controlling liveness, but the safety rail blocks the one legitimate empty state. Probably fine to require operator confirmation, but it must be specified.

  4. **HTML from an external CMS is an injection/sanitization surface.** Today description_i18n HTML is hand-authored by a Canary engineer (trusted). Post-integration it's AEM/Wyndham-authored and rendered in the guest app. The doc treats Description/T&C format as a *formatting* decision (plain/Markdown/HTML, concatenate T&C?) but misses the *security* angle: HTML pulled from AEM should be sanitized/whitelisted before store/render. **Ask:** add an explicit sanitization step; don't trust-pass AEM HTML into the guest surface.

  5. **Akamai machine-auth is genuinely blocking and gates real testing.** Blocking-OQ-1 (SVCRUN-21704) means the connector can't be validated against *publish* until the request pattern is agreed with Wyndham, and even FQA-author needs an AssistNet ticket. The doc's "just a plain authenticated GET" may be optimistic — server-to-server behind Akamai edge protection can be more than a header. This is the single biggest schedule risk; the doc flags it well but could state plainly: **nothing on the real read path can be built/tested until SVCRUN-21704 lands; Phases 1–2 are FQA-author-only.**

  6. **Cutover fallback can silently serve stale content.** "Keep hardcoded WYNDHAM_OFFERS as fallback when no snapshot exists" is a sensible net, but a months-old constant = expired promos, which is exactly the "no expiry" pain this solves. Between Phase 3 (cutover) and Phase 4 (decommission) there's a window. **Ask:** alert/log loudly whenever the fallback path is hit, and define when "no snapshot" is ever expected post-cutover.

  7. **Ordering gap is product-visible and should block cutover, not follow it.** Carousel order has no AEM source field (marked GAP); fallback "order by fragment path / title" is arbitrary and won't reflect Wyndham reordering. It's in the Wyndham questions list — good — but emphasize it needs an explicit sort field resolved *before* cutover.

  ### Minor notes
  - **Section retitle "Wyndham Offers" → "Wyndham Rewards Offers"** is a guest-visible copy change riding along with infra work — confirm product signed off. (Lookup is by slug "wyndham-offers", title is display-only, so no functional break — confirmed against provider line 258.)
  - **Images leaving the sensitive bucket** ("never sensitive, just parked there") — quick confirm with whoever originally placed them there that there's no compliance reason.
  - **scope_kind/scope_key** is speculative for a single global Wyndham set — same YAGNI note as #1; leave a seam, don't model the full key now.
  - Fix the minor line-number drift (rollout recipe is 118–126, not ~113-120) if the doc is meant to stay a precise code reference.

  ### Suggested next step
  These are review comments, not blockers to the doc's approval. If you want, I can post a condensed version as a Notion comment on the doc or as an ENT-6353 comment — but I have NOT posted anything externally; say the word and I'll draft the exact text for your approval first.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781820216676709
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Review Compendium AEM integration doc
updated: 2026-06-29 16:05:40.043578
waiting_on: null
waiting_since: null
working_on: false
---

Ryan Rogers: Adobe Experience Manager integration for the Wyndham Compendium doc ready for review (reviews can wait but flagged for early look). https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1781820216676709