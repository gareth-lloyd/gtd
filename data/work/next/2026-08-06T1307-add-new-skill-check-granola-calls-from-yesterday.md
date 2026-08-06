---
area: null
completed_at: null
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
  4. **Review Belinda's test plan + get local stack running** — bug bash is **Fri 7 Aug**,
     you said you'd test **Thursday = today**. Martine has the management command.
     *(APAC standup)*
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
project: 2026-04-16T1351-ship
source_id: null
tags: []
time_minutes: 5
title: Add new user-level claude skill - check granola calls from yesterday. or check
  specifc  call.
updated: 2026-08-06 13:20:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

In either case, output should be summary of actions required and option to add them to gtd