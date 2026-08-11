---
area: null
completed_at: 2026-08-07 13:42:25.260120
contexts: []
created: 2026-08-06 20:34:33.079850
defer_until: null
due: null
energy: low
id: 2026-08-06T2034-check-transcript
order: null
output: |
  ## Agent run 2026-08-07T12:03 EEST

  Read the full doc: **Triage Agent Sync — 2026/08/05 08:30 PDT** (Gemini notes + transcript)
  https://docs.google.com/document/d/1pR_vFnbnykKd2v2vU9KVloIbG3ooAT1pCtiYngPp5xI/edit
  Transcript tab: ...&tab=t.g3443halmadm | Recording: https://drive.google.com/file/d/1sE_5XMW8zUWXqVy_Pg3BFPe_gGpwaCig/view
  Owner: Laura DeWald. 30 min. Present: Laura DeWald, Blake Vanlandingham, Dylan Moradpour,
  Julius Seporaitis, Stephanie Barry, João Bueno. Garrett Idler absent (Colorado). You were not invited —
  this is FYI/awareness, nothing is assigned to you.

  ### What actually happened (5 things)

  1. **Workup label wasn't broken — the view was.** Blake thought the `workup` label had stopped
     firing (latest ticket days old). Cause: the Linear view was excluding triage tickets and sorting
     wrong. Once corrected, 19 issues showed up. Laura is building a proper Workup view.

  2. **MCP write access is being picked up, and it's being prioritised for hotel setup — not triage.**
     Dylan got a message from Bernard: non-EPD people are getting Canary MCP access and all want write.
     Blake's ruling: deprioritise write for the *triage* agent (support team should be the implementer
     of change); prioritise the *hotel setup* use case, gated with the same controls as impersonation
     (e.g. block non-demo hotels, `is_demo` not user-mutable) so blast radius on a pre-live hotel is ~zero.
     → This is the bit most likely to touch your world (onboarding scripts / ENT hotel setup work).

  3. **A generic SQL MCP tool is in PR and about to merge (Dylan).** Motivation: people are bypassing
     the MCP entirely — standing up local MCP servers that proxy to the prod DB, or DB tunnels giving
     Claude direct database access. Dylan also wants to break up the current "very big tools" into
     smaller, more specific ones. If that lands it changes what canary-local MCP can do.

  4. **All MCP tool scoping will become authentication-based.** Blake: "we shouldn't be doing any scoping
     that is outside of the authentication token." Dylan is researching whether FastMCP's tools/list
     response can be varied per caller so the triage agent simply never sees write tools. Practical
     consequence: the tool list you get from canary-local may start differing by user.

  5. **Security posture stated explicitly** (useful context, worth internalising):
     - Slowing down data access is "security by obfuscation… AI makes that basically irrelevant."
       The real pillars are auth (Okta), audit logging, and SIEM.
     - Teleport already audit-logs all traffic in/out of the direct DB — that's why direct DB access via
       Teleport is an accepted pattern. SIEM rollout targeted late Q3 / early Q4.
     - The genuinely hard problem is *accidental exfiltration by headless agents*: agent collects PII,
       then gets talked into putting it in an outbound request. Local/interactive use is low risk
       (human watching); the worry is an unmonitored headless system someone can retry against —
       Zendesk support was named as a plausible entry path.
     - Proposed mitigation: a "breaker" that revokes internet access the moment an agent touches PII.
       Still being designed with security — the one item logged as "needs further discussion".
     - Model transport is NOT the concern ("not worried about PII going to Anthropic"). The concern is
       tool calling from the sandbox out to the world. Sandboxes currently run on **E2B, not AWS**, and
       still need holes poked for Linear, Notion, Groundcover, etc. Dylan floated Bedrock (Opus
       available; Fable not) to avoid egress to Anthropic — Blake redirected: it's the sandbox, not
       where the model runs.

  6. **Missing-info workflow.** Today a ticket missing info falls back to the legacy canary agent session
     instead of the new workup session. Agreed shape: notify on Slack (fast turnaround, DMs work well)
     *and* keep the record in the Linear ticket — Stephanie's point being that CS/support need the trail,
     and the ticket creator often isn't the person with the answer (IM or CSM is). Stephanie also has
     upstream work making fields mandatory in Zendesk + linking hotels, so less is missing to begin with.
     Julius: different teams have different anchor identifiers — investigation agent anchors on
     reservation, payments anchors on payment intent / auth form. Teams to build their own gatherers.

  ### Corrections to the Gemini notes (they're wrong in a few places)

  - **"Ingram" is "Engram"** — the memory layer. The Quick notes and Next steps say "Ingram" throughout;
    only the Decisions section gets it right. Blake gave Jason the green light to bolt Engram in as the
    memory layer for `workup` as a unit of work, plus a UI to explore the memories, targeted ~next week.
  - **Jason is credited with two next-step items but was not in the meeting** — Blake reported the
    approval on his behalf. Don't read those as commitments made in the room.
  - **"SEIM" / "seam" / "sim" = SIEM.** **"Machine Context Protocol" = Model Context Protocol.**
    **"Powerbot"/"birdie b" = Power Bird** (Rick's team; Blake sees overlapping problems).
  - Notes say "19 issues identified after correction" — accurate, but the framing "triage tickets were
    incorrectly excluded from workup labels" is off: the *label* was fine, the *view* excluded them.
  - Blake also flagged a cadence change: these move to **weekly**, and Nancy (new Head of Support) joins.
    Goal for the block: a portion of tickets resolved entirely without engineering touching them.

  ### Next steps recorded (none are yours)

  - [Laura] Build the Workup view; share the rollout doc with Blake; post projects/priorities for the
    block to Slack. (Laura OOO through Fri 2026-08-07.)
  - [Jason] Bolt Engram in as memory layer; wire the memory-exploration UI.
  - [Dylan] Auth-based access control for MCP tools to limit blast radius; land the generic SQL tool PR.

  ### Suggested follow-ups for you (not taken — your call)

  - Watch for Dylan's generic-SQL-tool PR and the auth-scoped tool list — both change canary-local MCP
    behaviour for everyone, including your monitor skills.
  - If hotel-setup write access is being built with demo-hotel guardrails, that's adjacent to the
    onboarding-script approach on ENT-6032 (IHG HotelKey pilot) — may be worth a word with Dylan
    before the shape is fixed.

  No external writes made. Nothing posted to Linear, Slack, or the doc.
project: null
source_id: null
tags: []
time_minutes: 5
title: Check transcript
updated: 2026-08-07 13:42:25.260114
waiting_on: null
waiting_since: null
working_on: false
---

https://docs.google.com/document/d/1pR_vFnbnykKd2v2vU9KVloIbG3ooAT1pCtiYngPp5xI/edit?tab=t.zi39ku8q84u3