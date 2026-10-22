---
area: null
completed_at: 2026-10-21 12:46:54.670642
contexts: []
created: 2026-10-21 10:38:41.186840
defer_until: null
due: null
energy: low
id: 2026-10-21T1038-justification
order: 1
output: ''
project: 2026-10-21-config-registry
source_id: null
tags: []
time_minutes: 5
title: Justification
updated: 2026-10-21 12:46:54.670634
waiting_on: null
waiting_since: null
working_on: false
---

**Ranking: 3 → 1 → 2, but they're stages of one system, not alternatives.**

**1st: Option 3, the one-off push.** Agents have no tribal knowledge; every session starts cold, so the scarce resource is accurate, discoverable context at the point of work. Only option 3 attacks the backlog, which is where the actual problem lives. Two caveats that decide whether it pays off: intent can't be inferred from code, only behaviour, so the generated registry needs owner validation, prioritised by blast radius, or you've built a confident, hallucinated map. And make the output structured and machine-checkable (a flag manifest with declared dependencies, exclusions, defaults, owner), not prose. A manifest CI can validate is a contract; a README is a suggestion. The biggest win is probably the deletion list: dead flags, flags that are always set together, flags that should be a single enum.

**2nd: Option 1, verification.** This is where enforcement lives, and the registry is worthless unless coding, review, and debug flows actually consume it. But tests alone can't lead here because of the oracle problem: you can't write a regression test for an interaction nobody knows exists, and the combinatorial space is untestable exhaustively. Option 1 works once option 3 gives it something to check: constraint-level tests from the manifest, pairwise tests on the high-risk flags, review prompts that cite the registry entry for any flag touched.

**3rd: Option 2 standalone.** Across 100 developers it produces inconsistent, scattered, un-indexed notes, never covers the existing mess, and rots. It's the right *maintenance mode* for option 3, but only if enforced mechanically: a CI gate that fails any PR touching a flag without a registry update, with an agent drafting the entry so the cost to the human is a review, not a write.

**Other deciding factors**

* Rate of flag churn: high churn makes the maintenance gate non-negotiable and argues for spending less on the initial push and more on the enforced loop.
* Real cost isn't tokens, it's validation hours from flag owners. Budget that explicitly.
* Keep the agent entrypoint (CLAUDE.md / AGENTS.md) tiny and pointing to the registry; a giant doc agents must read every session is worse than a queryable table.
* The "hard to set up for a client" symptom is better solved by validated config schemas and named presets than by documentation. Docs explain the complexity; schemas and presets remove it.
* Ask whether the goal is to document the flags or to have fewer. If leadership wants the latter, the push should be scoped as a flag-reduction project with a registry as a byproduct.