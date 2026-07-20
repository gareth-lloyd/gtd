---
area: null
contexts:
- consume
created: 2026-07-14 11:46:51.278063
defer_until: null
due: 2026-07-14
energy: high
id: 2026-07-14T1146-read-and-give-feedback-on-blake-s-a-product-proces
order: null
output: |
  ## Agent run 2026-07-14T16:25:52

  Read the full doc (Notion version: https://www.notion.so/canarytechnologies/A-Product-Process-a-Machine-Can-Read-39a81468615180cb8c8ad021c77f73ef), Blake's Slack ask (https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799), and the related Orbital-swarm guest-app postmortem he linked in-thread (https://www.notion.so/canarytechnologies/39a81468615181b98178de2b6cbc8781). Drafted feedback below for you to adapt — NOT posted anywhere (no Notion comments, no Slack reply).

  Caveats: couldn't watch Jason's Nest Looms (loom.com/share/04568f5b61d9450190c4ff23ddda30c2 and loom.com/share/f7525e4d04a94d6097f27c0885de1dd7 — video, needs your login), and the live page (pages.cnry.cloud/7yhkzegpth) is behind Cloudflare Access, so presentation notes are from the Notion version and I never saw the diagram in section 06.

  ### Draft feedback — ideas

  Strong points worth saying back to Blake:
  - The linear-vs-compounding frame is the right opening and lands for a non-technical reader.
  - The sharpest insight in the doc is "a human bridges a messy handoff by force of will; AI can't" — that single line justifies the whole firm-stages design and deserves even more prominence.
  - Scoping Prioritize and Launch out is a genuinely good call and preempts the "is this a reorg" anxiety.
  - The gate economics logic (cheap text-vs-text iteration upstream earns the expensive downstream run) is the most exec-persuasive part.

  Pushback / gaps:
  1. **The guest-app evidence cuts both ways, and the doc only uses one side.** Section 08 cites Fable 5 one-shotting the guest iOS app as proof of capability. But the postmortem Blake himself linked shows the run shipped 67 findings (5 P0), dead controls everywhere, and an app that can't enter its main shell — precisely because the spec/contract didn't encode the demo bar ("referees verified states, not interactions"). If SJ reads both docs, the claim reads as oversold. The fix is easy and actually strengthens the thesis: cite it as proof that *spec quality is now the constraint* — the swarm hit every bar the contract encoded and missed every bar it didn't. That's the best real-world argument for the Prototype & Spec stage in existence, and it's currently left on the table.
  2. **The load-bearing bet is buried.** The "premise we're still validating" callout (design builds pixel-perfect prototypes faster than Figma on Nest) sits at the bottom of section 08. That's the whole wager — surface it earlier, and add how/when we'll know: what does the validation look like, what's the timeframe, what would make us stop?
  3. **No explicit ask.** For a doc aimed at SJ, it never says what decision or resource is being requested (blessing? FEE headcount protection? budget for model spend?). Execs read for the ask; right now it ends on "what we're doing" without "what we need."
  4. **A PM reading this can't tell what changes Monday.** Who writes the Spec — PM, design, eng? Who reviews at each gate? Even one sentence of "roles stay the same, the artifact changes" would help the stated audience.
  5. **"Coupled so the two can't drift apart" is asserted, not mechanized.** Frozen branch captures the prototype, but what actually pins spec↔prototype coupling? One sentence on the mechanism (or an honest "TBD") would head off the obvious question.
  6. **Nest drift risk is unaddressed.** A skeleton codebase beside the real one will diverge from production constraints — and "prototype looks real but can't be built that way" is exactly the intent-loss the doc is fighting. Worth one sentence on who keeps Nest honest and how.
  7. **Health layer has metrics but no baseline or target.** "So we can see whether the spend is producing output" invites "and what number would satisfy you?" Pre-commit to even rough success criteria at 3/6 months.

  ### Draft feedback — presentation (for SJ/PM/non-technical)

  - Overall: right length, good one-idea-per-section rhythm, callouts used well, quotable lines. This is close.
  - Jargon slips for the stated audience: "Golem" (unexplained), "500s" (say "customer-facing errors"), "substrate" (final callout, undefined), "contracts" (means API contracts but reads legal), "adversarial code review". The "loop engineering" callout adds little for SJ/Harman — cut or footnote it.
  - The 65% usage / 8% throughput stat needs a citation. It's the doc's only number in section 01 and an exec will ask where it's from; unsourced, it undermines the credibility of everything after it.
  - Header echo: several sections repeat the title in the bold subtitle ("Two common pitfalls" / "Two common pitfalls to avoid"). Tighten to one line each.
  - Section 04 says "three stages" then introduces two more "at the edges" — slightly confusing in text; make sure the diagram carries this (I couldn't view it).
  - The economics section would land harder with one concrete worked example in dollars: "catching a flawed spec at the gate costs ~$X of review; letting it through costs the eng design + build + fix, ~$X,000."
  - Consider moving the "What we're actually doing" callout (or a 3-line TL;DR + the ask) to the top — SJ-type readers decide in the first screen.

  ### Suggested next steps (for you, not done by me)
  - Watch the two Nest Looms before replying — Blake explicitly asked for thoughts on them and I couldn't view video.
  - Post the feedback: quick take in the Slack thread + the specific points as Notion comments on the relevant sections (the doc already has open discussions on "The one document", "Nest", and "What we're actually doing" callouts).
project: 2026-04-10T0840-ticket
source_id: https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799?thread_ts=1783769548.648799&cid=C0AJW6KHE1E
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 30
title: Read and give feedback on Blake's 'A Product Process a Machine Can Read'c
updated: 2026-07-20 14:51:21.814394
waiting_on: null
waiting_since: null
working_on: true
---

Blake in #agentic-dev-leads (Jul 11): wants thoughts on both the ideas and presentation (aimed at SJ/PM/non-technical). Doc: https://pages.cnry.cloud/7yhkzegpth (Notion for comments: https://www.notion.so/canarytechnologies/A-Product-Process-a-Machine-Can-Read-39a81468615180cb8c8ad021c77f73ef) + Jason's Nest demos.
https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799?thread_ts=1783769548.648799&cid=C0AJW6KHE1E