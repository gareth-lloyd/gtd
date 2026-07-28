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

  ## Agent run 2026-07-23T15:04:58

  Re-checked the Slack thread and Notion doc for movement since the Jul 14 run. Nothing posted anywhere by me. The ask is still open — you haven't replied in the thread yet, and the doc discussion has grown around you.

  ### What's new since Jul 14

  **Slack thread** (https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799): one new reply. Blake (Jul 16) says the doc "lines up well with the article Gareth posted" — your Dex Horthy / context-engineering post in #ai-eng (https://canarytechnologies.slack.com/archives/C08VCEMGYG7/p1784187754229409). So he's now explicitly waiting on your take and has handed you the hook for it.

  **Notion discussions** (all still unresolved; Blake replied to each):
  - Ian Clark on "What we're actually doing": two classes of expensive problems — designing the wrong thing (this doc) vs architecting badly — and he's not convinced a "mega harness" can do the second. Blake (Jul 16): doc doesn't deprioritize Eng Design, promised to clean up language to make each box clearly human-in-the-loop.
  - Sudarshan Muralidhar on "The one document": docs written for AI look very different than docs for humans (length, depth). Blake (Jul 16): proposes two segments — human-oriented top, AI-oriented supplemental bottom — that AI keeps coherent.
  - Sudarshan on "Nest": what does this solve vs existing prototyping tooling? Blake (Jul 13): existing prototyping loses intent — designers won't translate back to Figma, and a prototype without a spec is painful for engineers.

  **Doc content**: essentially unchanged from the Jul 14 read. Section 04 now stresses each stage is "a mix of human-in-the-loop co-piloting and heavily agentic work" — likely Blake's promised cleanup from the Ian thread. All prior draft points still apply.

  ### How this changes the draft feedback

  - Draft points 1 (postmortem cuts both ways), 2 (buried bet), 3 (no ask), and 7 (no baseline/target) are still un-raised by anyone — these are your highest-value unique contributions.
  - Points 4/5/6 now partially overlap with the Ian and Sudarshan threads and Blake's replies — better delivered as replies inside those existing discussions than as fresh comments.
  - New angle Blake explicitly invited: he claims the doc lines up with the Dex Horthy episode. Mostly true (Dex's "find the leverage points" ≈ the gates; human belongs at design; the dark-factory failure is exactly why the gates exist). But there is one direct conflict worth naming: Dex's strongest operational claim is "throw the docs away after use — nobody has found keeping specs and code in sync worth it; code is the source of truth," while the doc's central artifact is a durable spec coupled to a frozen prototype branch that must NOT drift. Either Blake thinks the coupling mechanism beats everyone else's failed attempts (worth saying how), or the spec is disposable per-project input and "coupled so the two can't drift apart" overstates it. This is the sharpest, most on-topic reply you can make and it lands as engagement, not criticism.

  ### Ready-to-adapt Slack reply (short version)

  > Finally read it properly. Big picture I'm bought in — the "human bridges a messy handoff by force of will; AI can't" line is the whole argument and it's right. Three things I'd push on:
  > 1. On it lining up with the Dex episode — mostly yes (gates = his "leverage points", human at design, his dark-factory story is the argument FOR the gates). But one real conflict: his hardest-won lesson was "nobody has found keeping specs and code in sync worth it — code is the source of truth", and our central artifact is a durable spec coupled to a frozen prototype. What's the mechanism that makes our coupling survive where everyone else's didn't? If there isn't one yet, that's fine, but the doc asserts it.
  > 2. The guest-app run is cited as proof of capability, but the postmortem shows it's really proof that spec quality is now the constraint — the swarm hit every bar the contract encoded and missed every bar it didn't. Reframed that way it's the strongest evidence for the Prototype & Spec stage you have.
  > 3. For SJ specifically: the doc has no ask (what decision/resource do you need?) and the validation bet ("faster than Figma on Nest") has no success criteria or timeframe. Execs read for those two things first.
  > Detailed nits as Notion comments.

  ### Suggested next steps
  - Watch the two Looms (still unviewable by me) — then adapt and post the Slack reply above, and drop points 4/5/6 from the Jul 14 draft as replies into the existing Ian/Sudarshan Notion discussions rather than new threads.
  - The presentation-level nits from the Jul 14 draft (jargon, unsourced 65%/8% stat, header echo) are all still valid against the current doc if you want to include them as Notion comments.
project: 2026-04-10T0840-ticket
source_id: https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799?thread_ts=1783769548.648799&cid=C0AJW6KHE1E
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 30
title: Read 'A Product Process a Machine Can Read'
updated: 2026-07-27 16:15:56.416479
waiting_on: null
waiting_since: null
working_on: false
---

Blake in #agentic-dev-leads (Jul 11): wants thoughts on both the ideas and presentation (aimed at SJ/PM/non-technical). Doc: https://pages.cnry.cloud/7yhkzegpth (Notion for comments: https://www.notion.so/canarytechnologies/A-Product-Process-a-Machine-Can-Read-39a81468615180cb8c8ad021c77f73ef) + Jason's Nest demos.
https://canarytechnologies.slack.com/archives/C0AJW6KHE1E/p1783769548648799?thread_ts=1783769548.648799&cid=C0AJW6KHE1E