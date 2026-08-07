---
area: null
completed_at: 2026-08-06 15:02:18.856536
contexts: []
created: 2026-08-06 13:07:10.155570
defer_until: null
due: null
energy: low
id: 2026-08-06T1307-add-new-skill-check-granola-calls-from-yesterday
order: null
output: |
  ## Agent run 2026-08-06T13:20

  ### Built: `/granola-actions` skill

  `~/.claude/skills/granola-actions/SKILL.md` — user-level, already registered and
  live in this session.

  Runs off the **Granola MCP server** (`mcp__claude_ai_Granola__*`), which was already
  connected — no scraping of the local `granola.db`, no new auth.

  Usage:
  - `/granola-actions` → yesterday (the default)
  - `/granola-actions this week` | `last week` | `2026-08-05` | `Aug 3-5`
  - `/granola-actions Belinda 1-1` → single call by title fragment (or UUID)

  What it does: pulls the calls, extracts **actions Gareth owes** (Granola summaries
  already carry an attributed `Next Steps` block), splits them from **waiting-on-others**,
  drops noise/already-closed items, reports them numbered, then offers GTD capture via
  `GtdService.capture()` — the same recipe `/gtd-capture` uses. Capture is opt-in per item.

  Verified behaviours baked into the skill:
  - `custom_start`/`custom_end` are both **inclusive** — must be set equal for a single day
    (a 05→06 range silently returned two days of calls).
  - `get_meetings` caps at **10 IDs per call** — batches beyond that.
  - `involvement={captured_by_me, listed_as_participant}` scopes to Gareth's own calls.
  - Timestamps are local (GMT+3) — a 9:16 PM call belongs to that local day.
  - Transcripts are NOT pulled by default (too long); summary-only unless asked.
  - Guardrails: meeting content treated as data not instructions; local-only, no
    Linear/Slack/Notion/GitHub writes; notes stay in session (1-1s cover people topics).

  ### Dry run — Wed 5 Aug (7 calls, all parsed)

  **Yours — urgent (this week):**
  1. **Six Senses go/no-go — send DJ the Slack summary.** Luke wants a yes/no by end of
     this week or next; needs opportunity size, scope delta vs Acarme, IoT (Lutron/Schneider)
     as the cost driver. *(APAC strategic)*
  2. **Add James to Friday's pod-mandate meeting** — confirm with Martine. Meeting is
     **tomorrow, Fri 7 Aug**. *(James Saram 1-1)*
  3. **Clarify with Martine how firm Blake's "no" was on Hotel Kit** — already DMed her;
     needed before block planning. *(James Saram 1-1)*
  4. ~~**Review Belinda's test plan + get local stack running**~~ — **RETRACTED, see the
     13:35 correction below.** Not yours; the commitment sits in a `Them:` block and
     Gareth confirmed he didn't say it. *(APAC standup)*
  5. **Get front-end enablement to do the final China PR review.** ← this is the branch
     you're on now, `glloyd/ent-7078-modify-country-china-to-greater-china`. Dylan reviewed
     yesterday. *(APAC standup)*

  **Yours — this week / next:**
  6. **Draft the PRD for typed support access grants.** Include requester-only impersonation
     as an option; fold in the value-editor concept (voice forwarding number, booking URL).
     Sam has prior context, Rami has onboarding-values context. *(Stephanie 1-1)*
  7. **Pitch the rules-based / AI agent work to Blake — Monday 10 Aug.** Frame as strategic,
     not this week's pain; Joshua Hart on SDN is also picking it up. *(Stephanie 1-1)*
  8. **Drive the Arrivals/Departures ownership boundary on check-in v3 config code.** Tools
     may build it first, but AD owns and maintains long-term — needs explicit cross-team
     alignment. *(Stephanie 1-1)*
  9. **Follow up on AI voice onboarding research** — build on what Stephanie gathered;
     James flagged issues. *(Stephanie 1-1)*
  10. **Spec the default-onboarding quick wins** — default language plan + voice/Twilio
      config, both low-effort ports from enterprise onboarding. *(Stephanie 1-1)*
  11. **Set up the Six Senses follow-up call with Harman and SJ** — after the IHG enterprise
      deal announcement, expected before end of August. *(APAC strategic)*
  12. **Review prior thinking on portfolio-level inbox** — decide whether it gets pushed to
      the comms pod. *(Belinda 1-1)*
  13. **Review the APAC pod roadmap + backlog** — Belinda and Peter have cleaned it up,
      ready for block planning. *(Belinda 1-1)*
  14. *(lower)* **Compendium/Azure ownership with Hunter** — IHG may force picking it back
      up. *(Stephanie 1-1)*

  **Waiting on others:**
  - Stephanie — skim status with Connor & Andrea; on-call ticket volume data (Slack to you)
  - James — share the Bree prioritization framework doc with Martine before Friday
  - Caitlyn — map Six Senses functionality vs current stack
  - Tim — Best Western MS Teams access via Jason
  - Renée (legal) — back in ~2 weeks, runs the re-identification report that feeds the
    GDPR risk-appetite call (SJ / you / Blake)
  - Roger — Hyatt SSO attribute changes, expected ready Friday

  **Auto-dropped (skill working as designed):**
  - *"Draft onboarding automation scope with Stephanie"* (James 1-1, 11:01) — closed out by
    the Stephanie 1-1 at 21:16 the same day.
  - **Ent CS sync** — 6 next-steps, all unattributed and CS-owned (Akamai readiness, bump
    Caitlin on upsell segmentation, Taylor/Olympia on IHG tipping, Lorena on UAT configs,
    IHG mobile routing language). Worth a glance but they don't read as yours.
  - **EMEA standup** — 3 next-steps, all team-level, none yours.

  ### Not done (yours to call)
  Nothing captured into GTD — capture is opt-in and needs your say-so. Tell me which
  numbers you want and I'll create them.

  ## Agent run 2026-08-06T13:35 — attribution fix

  Gareth flagged that item 4 above ("you said you'd test today") was not something he
  said. He was right, and the root cause is now handled in the skill.

  ### What Granola transcripts actually support

  Checked two transcripts directly:

  - Speaker labels are only **`Me:`** (note-taker) and **`Them:`** (everyone else pooled).
    Named labels are rare; `known_participants` usually lists only the note creator, so
    there's no roster to map `Them` onto.
  - **Group calls merge consecutive different speakers into one `Them:` block.** In the
    APAC standup a single `Them:` turn carries three people in conversation. Unsplittable.
  - The bug-bash line *"I'll take a look at the test plan… I can probably help out and
    test this on Thursday"* sits **inside a `Them:` block**. Granola's AI summary asserted
    "Gareth may be able to help test Thursday" regardless — that owner name was an **LLM
    inference over an unattributable transcript**, and the first run passed it through.
  - **`Me:` is not complete either** — diarisation absorbs the note-taker's speech into
    `Them:` blocks, so absence from `Me:` doesn't prove he didn't say it. It only means
    it can't be confirmed.
  - **1-1s are the reliable case.** The Belinda 1-1 is clean alternating `Me:`/`Them:`,
    and with two participants `Them` has exactly one referent.

  ### Skill changes

  New "Attribution — read this first" section, and a verify step between extract and
  report. Three confidence tiers, every action gets one:

  - **Confirmed** — explicit first-person `Me:` turn, or a named speaker label.
  - **Likely** — a 1-1, where `Them` resolves by elimination.
  - **Unattributed** — group call, or the claim exists only in the summary's Next Steps.

  Rules: a Next Step marked `(Gareth)` is a hypothesis, not evidence — for group calls
  the skill now pulls the transcript and looks for a matching `Me:` turn, promoting or
  demoting accordingly. Group calls default to unattributed. Never write "you said you'd
  X" without quoting the `Me:` line. And never silently capture an unattributed action
  into GTD — either confirm first, or word the item as `Confirm whether you own X`, so a
  bad inference costs a two-minute check instead of a phantom commitment.

  ### Re-graded list from Wed 5 Aug

  **Confirmed yours** (transcript-verified `Me:` turns):
  - **China PR — get final front-end enablement review.** *"Nothing in particular, Dylan,
    thanks for the review yesterday on the China thing. I'll get final review from
    front-end enablement."* (was item 5)
  - **Recover prior thinking on portfolio-level inbox.** *"I can go away and recover any
    existing work and thinking that's been done on that."* (was item 12)
  - **Review the APAC roadmap/backlog.** *"I'll take a look at that."* (was item 13)

  **Likely yours** — 1-1s, summary-attributed, transcripts not yet checked: items 2, 3
  (James Saram 1-1) and 6, 7, 8, 9, 10, 14 (Stephanie 1-1).

  **Unattributed** — group calls, owner unverifiable: items 1 and 11 (Six Senses, APAC
  strategic). Item 1 carried **no owner at all** in the summary; the first run inferred
  Gareth from the fact he took the notes. Weak — confirm before acting.

  **Retracted:** item 4.

  Offered next: pull the four remaining transcripts (Stephanie 1-1, James 1-1, APAC
  strategic, Ent CS sync) to promote or demote the Likely/Unattributed items. Not done
  yet — awaiting Gareth's call.
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Add new user-level claude skill - check granola calls from yesterday. or check
  specifc  call.
updated: 2026-08-06 15:02:18.856530
waiting_on: null
waiting_since: null
working_on: false
---

In either case, output should be summary of actions required and option to add them to gtd