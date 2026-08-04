---
area: null
completed_at: null
contexts:
- react
created: 2026-08-03 08:59:34.598041
defer_until: null
due: null
energy: medium
id: 2026-08-03T0859-give-lautaro-feedback-on-the-managed-support-acces
order: null
output: |
  ## Agent run 2026-08-03T10:12Z

  Read the proposal, the full DM thread, the SAG PRD, and Blake's 2026-07-30
  message. Drafted feedback for Lautaro below. **Nothing sent** — needs your
  approval before it goes anywhere.

  ### Source material
  - Proposal: https://www.notion.so/canarytechnologies/Proposal-Managed-Support-Access-for-CS-3ae81468615181abbf82ea4f92ef9794
  - Group DM thread: https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785498208747889
  - Blake's position (2026-07-30, #tmp-check-in-configuration-location):
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785363226229569
  - Your typed-SAG proposal in the same channel (2026-07-30):
    https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785419100835479
  - SAG PRD: https://app.notion.com/p/4150b263e21c41c6bbf16cbe2461bbf0
  - SAG eng design: https://app.notion.com/p/11f8da83d8504e89b1f07cd06cc4145a

  ### The five things that actually matter

  1. **The flagged section is a liability, not a tone problem.** "Usability was
     never a priority... without a long term product vision" is a claim about
     past decisions that costs credibility and buys no ground. His real
     argument — the residual is structural — stands without it. Rewrite below.
  2. **Blake's 2026-07-30 message pre-empts the doc's framing.** Impersonation
     stays default; SAG for sensitive actions *including user management*;
     `/manage` acceptable "for configuration that should never be
     shown/managed by the hotel admin". As written the doc reads as re-opening
     a decision made two days earlier. But Lautaro's strongest cases (portfolio
     management, duplicate merges, bulk cross-property ops) **pass Blake's own
     `/manage` test** — reframing the ask to fit that rule turns a fight into
     an easy yes for a narrow slice.
  3. **He needs to engage with typed grants in the doc, not just in Slack.** He
     told you in-thread he doesn't think it's the right solution but never says
     why in writing. His best written objection — internal/customer actions
     mixed in the same views needing extra logic — is aimed at impersonation as
     built today and mostly dissolves under your model (no `is_staff`
     branching, plain permission checks). That's the crux and it's currently
     invisible to any reader.
  4. **The ask is unsized.** Highest-value addition by far: split the ~175 July
     tickets into (a) self-service will fix, (b) typed SAG + impersonation
     covers, (c) impossible in the hotel dashboard at any permission level.
     (c) is the size of what he's asking to build. ~30/month is a cheap yes;
     120 is a much stronger argument stated than implied.
  5. **Sequencing risk.** Stephanie is consolidating this + in-flight
     enterprise/internal-tools work + the L2 proposal into one source of truth
     (started today). Laura's L2 proposal goes to Blake "soon". Three
     overlapping proposals arriving separately is exactly the two-parallel-paths
     outcome you flagged in the thread. Recommend he lands content inside
     Stephanie's doc and makes one joint ask.

  ### Smaller catches (worth flagging before Blake sees it)
  - **Factual error:** doc says SAG creates a Property Manager user "for 24
     hours". The SAG PRD says a fixed 7-day window
     (`DEFAULT_PERIOD_LENGTH_DAYS`). Worth checking — if 7 is right it
     *strengthens* his blast-radius argument.
  - The "gathered by Claude from ticket titles, only a few validated by hand"
     caveat undercuts his best asset exactly where it needs to hold.
     Hand-validate 20–30 random tickets, quote an error rate.
  - Counts convince execs less than cost — engineering hours or median
     time-to-resolution per category.
  - Keep the "no credible source argues for impersonation-only" LLM output
     *out* of the doc. It's the easiest thing to dismiss and it'll drag the
     good data down with it. Cite SOC 2 least-privilege / JIT access directly
     or drop it.
  - The legal/opt-in section opens with "I am not sure this is possible from a
     legal standpoint" — that invites "come back when you know". Three-tier
     org opt-in is also a large surface (per-org config, approver management,
     routing) on an untested premise. He already says the proposal stands
     without it. Demote to open questions; ask Legal one question first.
  - Andrea's ask (named orgs, named workflows) is the right one — three
     concrete examples would carry a lot.

  ### Proposed rewrite of "Why this will not go away on its own"

      Self-service will absorb part of today's volume, and we should keep
      investing there. It will not absorb all of it, for two reasons.

      **The remainder is structural, not a UX gap.** A manager quits or is
      fired, someone loses their phone or gets locked out, an org restructures
      and 23 properties need reassigning at once. No amount of self-service
      polish removes these: they are by definition the cases where the
      customer cannot help themselves. As the property count grows, they grow
      with it in both volume and variety.

      **Customer-facing fixes are the slower lever.** Anything exposed to
      hotel admins has to be legible, polished, and integrated with what they
      already see. That is the right bar, and it is why those changes take
      time. Internal surfaces can close the same gaps in weeks, and keep
      closing new ones as they appear.

      User and property management grew incrementally alongside a fast-growing
      product, which is normal. The cost is that its self-service coverage is
      thinner than in areas we invested in deliberately. That is worth fixing,
      but fixing it is a multi-quarter effort, and the support load exists
      today.

  ### DRAFT message to Lautaro — NOT SENT

      Read it properly. Good doc — the problem statement is the strongest
      part. Feedback roughly in order of importance.

      **1. The section you flagged.** The issue isn't tone, it's that the
      sentence is load-bearing for nothing. "Usability was never a priority /
      without a long term product vision" is a claim about past decisions that
      costs you credibility and buys you no ground — your actual argument (the
      residual is structural) stands on its own. Suggested rewrite in a
      comment on the doc.

      **2. Blake said something two days ago your doc needs to answer.**
      https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785363226229569
      — impersonation stays the default, SAG for sensitive actions including
      user management, /manage acceptable "for configuration that should never
      be shown/managed by the hotel admin". As written the doc reads as
      re-opening that. But your strongest cases pass his own test: portfolio
      management, duplicate merges, bulk cross-property ops genuinely must
      never be hotel-visible. That subset is an easy yes under the rule he
      already stated. I'd reframe the ask: not "a new managed section", but
      "here is the set of actions that qualify under the /manage rule you
      stated, and here's who should own them".

      **3. Engage with typed grants in the doc.**
      https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785419100835479
      — a SAG carries a grant type, the grant type maps to a permission set on
      the attached user, views authorize on permissions with no is_staff
      branching. That gets you pre-defined actions only, a smaller blast
      radius, and "changed user X's role" in the audit trail instead of "had
      full access for a day". Your best written objection — internal and
      customer actions mixed in the same views needing extra logic and
      traceability — is aimed at impersonation as built today, and mostly
      dissolves under that model. You told me in the thread you still don't
      think it's right; that reasoning needs to be in the doc, because it's the
      crux. Without it, anyone who's heard the typed-grant pitch will assume
      you didn't consider it.

      **4. Size the ask.** Highest-value thing you could add: split the ~175
      July tickets three ways — (a) self-service will fix, (b) typed SAG +
      impersonation covers, (c) impossible in the hotel dashboard at any
      permission level. (c) is the actual size of what you're asking to build.
      If it's ~30 a month it's a cheap and obvious yes. If it's 120, that's
      your real argument and it's far stronger stated than implied. Right now
      the doc proposes a direction without sizing it.

      **5. Demote the legal section.** Opening the mechanism with "I am not
      sure this is possible from a legal standpoint" invites "come back when
      you know". Three-tier org opt-in is also a big surface — per-org config,
      approver management, approval routing — on an untested premise. You
      already say the proposal stands without it, so move it to open questions
      and ask Legal one question before re-raising.

      **6. Tighten before Blake sees it.**
      - Check the 24h figure — the SAG PRD says a fixed 7-day window. If 7 is
        right it strengthens your blast-radius point.
      - Hand-validate 20–30 of the July tickets and quote an error rate.
        "Approximate, gathered by Claude, only a few validated" undercuts your
        best asset exactly where it needs to hold.
      - Cost lands harder than counts: engineering hours or median
        time-to-resolution per category.
      - Andrea's ask is the right one — three named orgs and three named
        workflows would do a lot of work.
      - Leave the "nobody credible argues for impersonation-only" line out.
        Cite SOC 2 least-privilege / JIT access directly or drop it — an
        LLM-sourced consensus claim is the easiest thing in the doc to
        dismiss, and it'll take the good data with it.

      **7. On whether and when to share.** Yes — but not as a separate
      proposal, and not ahead of Stephanie. She's consolidating this, the
      in-flight enterprise and internal-tools work, and the L2 proposal into
      one doc, and Laura's L2 proposal is going to Blake soon. Three
      overlapping proposals arriving separately is how we end up with two
      parallel paths, which is the outcome I care about most here. Land your
      content inside Stephanie's doc and make one joint ask.

  ### Suggested delivery
  Send items 1–2 and 7 as the Slack reply (that's the time-sensitive part,
  given Stephanie started consolidating today), and leave 3–6 plus the section
  rewrite as Notion comments on the doc. Or send whole — your call.

  ### Awaiting your decision
  - Send as-is / edited / split between Slack and Notion?
  - Where — group DM (C0BLZ4Z9E67) or DM Lautaro directly? Item 3 is a
    disagreement with his stated view; the group DM makes it public to Connor,
    Andrea, Laura and Stephanie, which may be what you want given the
    consolidation, or may not.

project: null
source_id: https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785498208747889
tags:
- morning-gtd
- slack
time_minutes: 25
title: Give Lautaro feedback on the Managed Support Access for CS proposal
updated: 2026-08-03 13:12:43.000000
waiting_on: null
waiting_since: null
working_on: false
---

Group DM (Andrea, Laura, Connor, Lautaro, Stephanie), 2026-07-31. He explicitly asked for feedback before sharing with Blake, and specifically on the "Why this will not go away on its own" section reading as blaming product. Parked 3 days.
https://canarytechnologies.slack.com/archives/C0BLZ4Z9E67/p1785498208747889