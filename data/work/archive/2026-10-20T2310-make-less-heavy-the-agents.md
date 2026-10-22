---
area: null
completed_at: 2026-10-21 09:51:29.156929
contexts: []
created: 2026-10-20 23:10:46.087992
defer_until: null
due: null
energy: low
id: 2026-10-20T2310-make-less-heavy-the-agents
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: make less heavy the agents
updated: 2026-10-21 09:51:29.156923
waiting_on: null
waiting_since: null
working_on: false
---

Measured on the smoke: 71 agents and 65M input tokens for 10 keys, with the Refute phase taking 40 of those agents and 28.5M of the cache reads. The levers, roughly in order of savings:

1. **Drop or merge refute lenses.** Four lenses per key is 56% of agents. Measured refute rates were 18% for evidence-exists, 7% for facts-and-tags, 8% for edge-direction-and-when, and claim-complete refuted nothing but added 23 claims. Merging facts-and-tags into evidence-exists cuts a quarter of all agents. Dropping edge-direction-and-when for keys whose proposal has no edges (it examined 0 for booking_invite_active_at) costs nothing on quality.

2. **Run claim-complete only on sparse proposals.** It added 2 to 3 claims per key, but the critic's complaint was that it duplicated existing claims. Gating it to proposals with fewer than four claims removes it from most keys.

3. **Lower effort tiers.** Investigate runs at high, refute at medium. The pilot B agent pass ran at low and held quality. Refute at low is the obvious trial.

4. **Fold Write into Investigate.** The investigate agent already holds the proposal; a separate write agent re-reads the README and exemplars (2.9M cache reads for 10 keys). Having the refuters' corrections applied by the investigator as a second turn needs the investigator to write YAML, which the v2 pilot avoided for a reason, so this is a bigger change.

5. **Skip the Counterpart pass per batch.** Reverse edges can be added once per model by the pair check script after the batch, which is what the pilot did by hand.

6. **Cut the Critic.** One agent but 8.9M cache reads, the single biggest agent. Sampling five entries instead of ten halves it; it is also the step that produces the amendments, so dropping it means no second pass.

7. **Prompt diet.** Every agent reads the README, vocabulary and two exemplars. A trimmed "conventions digest" file of a few hundred lines in place of the full README would cut cache writes on every agent (2.2M on refuters alone).

For Hotel specifically, the heavy-key clause I added caps the reader walk at 40, but the 11 keys with over 200 readers (name, uuid, slug_name, timestamps, state, currency, phone) are identity columns that need a meaning and tags only. A "trivial key" mode that runs a single low-effort agent and skips refutation would take those off the full pipeline.

Cheapest combination to try first: lenses merged to three, refute at low, critic on five entries. That is about 40% fewer agents and should be visible in the next usage reading.