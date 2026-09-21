---
area: null
completed_at: 2026-09-21 13:52:32.066949
contexts:
- consume
created: 2026-09-18 00:00:00
defer_until: 2026-09-21 09:00:00
due: null
energy: low
id: 2026-09-18T0000-review-this-week-s-eng-leads-recording
order: null
output: |
  ## Agent run 2026-09-21T11:32 — Eng Leads, Thu 2026-09-17 (~42 min)

  Source: Zoom transcript + chat in ~/Downloads (`GMT20260917-155914_Recording.transcript.vtt`,
  `GMT20260917-155914_RecordingnewChat.txt`, audio `.m4a`). Reviewed from the transcript and chat,
  not the audio; the transcript is auto-generated, so names/terms flagged "(sic)" are unverified.
  You did not speak in this meeting. A `.crdownload` (71 MB, probably the video) was still
  downloading at 11:32 — not needed for this summary.

  ### Most relevant to you

  1. **Blocked-by-CS tickets clogging triage (main discussion, ~11 min).** Ian: PMS triage has 22
     tickets, 10 blocked waiting on a response. Andrea noted in chat "ENT added this recently"
     (a Blocked status). Outcomes:
     - General advice: use a real **Blocked status** instead of a blocked label (Laura/Blake: works
       much better for on-call). Caveat from Matías and Blake: nobody reviews a Blocked column unless
       you build it into your process, so tickets rot there.
     - **Laura and team own the macro fix**: WorkUp asks the requester for missing info via Slack DM
       (planned next block); idea of WorkUp/Lettuce-style bot pinging the creator of blocked
       tickets and **auto-closing if no response** (Andy; Laura agreed). Ian: if automating,
       standardize team Linear setups so the automation works everywhere.
     - Sudarshan: CS-created tickets are routinely lower quality than Zendesk/support ones. Laura:
       CS does not use Zendesk, they have their own Linear accounts; her ideal is CS not in Linear
       at all. Laura asked teams to push CS back to the issue form:
       https://www.canarytechnologies.com/manage/issues
     - Martijn (chat): should any non-bug come straight into Linear at all? Suggested Slack +
       PM in CC, or #product-questions / #emea-cs.
     - Laura (chat): **Claude-created tickets are using labels they shouldn't** — worth checking
       against anything you/Golem create in ENT.
  2. **WorkUp direction — overlaps your Workup/TypeSafe backtest.** Blake: WorkUp's follow-up /
     clarification mechanism is "the best place to invest"; prior tickets are effectively the
     knowledge base, and WorkUp **dedup / prior-art lookup** came up as the answer to ~3 separate
     issues. Laura wants to **vectorize Linear** because the MCP/API is slow. Andy: Linear **CLI is
     an order of magnitude faster than the MCP**; Ian: GraphQL API is good. Garrett (chat):
     OpenSearch team "is interested in connecting". Your Jev blind-pass/dedup results look directly
     relevant to Laura here.
  3. **Knowledge-base gap for CS.** Yasmin: payments engineers act as a stopgap explaining product
     to CS; no place to accumulate answers. Matías: a support-maintained Canary Knowledge Base
     exists but CS doesn't read it. Bernard: security is writing CS runbooks, e.g.
     https://app.notion.com/p/canarytechnologies/Generic-Suspected-Data-Breach-Calls-Support-Intake-Runbook-3bb814686151815b9030c8d7268e863e
     Same shape as the enterprise KB / `enterprise:work-ticket` playbook.
  4. **OHIP optimizations (Ian)** — high-risk item dropping off the list after this week; winding
     down. "At the edges we might miss a few updates"; extra vigilance requested. Relevant to
     Wyndham/IHG OHIP monitoring.
  5. **RDS migration to main VPC (Aditya)** — **Gateway rollout this week (w/c 2026-09-21)**, expect
     ~5–10 min read-only during switchover, same as EU. Canary follows after.
  6. **Check-in V3 migration** for arrivals and departures is under way; watch for check-in issues.
     Dashboard: https://www.canarytechnologies.com/canary-admin/guest-experience/migration-dashboard/

  ### AI tooling budget (Blake)

  - Exploring Codex and Grok alongside Claude. All three vendors have a $100 tier, so the
    cost-neutral option is dropping Claude 20x ($200) to the $100 plan plus $100 on another vendor.
  - Open question: how many people would hit limits on $100. Blake likely to send a **survey asking
    for usage screenshots**. Ishwar argued for just trialling $100 instead (In-Stay hit limits
    almost immediately on $100 when Fable launched and went back to $200); he offered In-Stay as
    guinea pig next billing cycle if they can bump back up.
  - Cost-neutral = fast; anything more needs approvals and is slower. Finance is open to it. Blake
    wants an answer within days. Cursor is already in budget — IT ticket. No aggregator gives
    subscription-level rates.

  ### IT / security

  - **Loom is being deprecated by 2026-11-20** (renewal is the 22nd). Atlassian killed the free
    Creator Lite licences; bill projected ~$5k/month. Replacements: Slack clips (5-min limit),
    "Shotter" (sic — probably Shottr; Alan noted Cap is also OSS), macOS built-in capture, back up
    to Google Drive. Chris is writing an SOP for bulk-downloading existing Looms; announcement at
    Canary Huddle next week. **Action for you: back up any Looms you want to keep before Nov 20.**
  - **1Password**: share links require named emails by design (audit trail). For team secrets use a
    shared team vault; vault creation is disabled for users (vault sprawl) — file an IT ticket.
    1Password for local dev secrets rollout (follow-up to Bernard's thread about a local secrets
    commit) is targeted for Q4; owner was unclear in the transcript.

  ### People / org

  - **Design**: Miguel is leaving, down to two designers. Blake: product and engineering get
    licence to pitch in on design short term; strong late-stage designer candidates, backfill
    expected soon. Holding at minimum headcount until a Head of Design is hired — no late-stage
    candidates for that role. They want strong visual + executive communicator (works closely with
    "SJ" (sic)) + hands-on/AI-aware, and keep finding two of three. Blake wants teams to explicitly
    deprioritize rather than quietly try to absorb the gap; raise specific problems with him.
  - No new hires; one transition on Z's side (performance). Diana Perez Afanador welcomed to the
    group.
  - Temperatures: more yellows than usual in lead temp — block planning plus perf reviews piling up
    (several +1s). Laura: design-doc "whiplash" (Bernard commented after approval, cost a day,
    resolved). Stephen: solo scramble on a **Radisson call-centre RFP** demo (entered late in
    round 3), submitted 2026-09-16. Lorena: post-certification slow because getting reservations
    from the hotel is slow.
  - All-hands: no feedback, keeping the current format. Yasmin wants to understand how kiosk /
    owning-check-in strategy shifted with the team changes, and the payments story.
  - **Lettuce** (Slack bot): DMs open items due each business day at 09:00; in the last 3 business
    days it DMs you and your manager together. Andy: the way to stop it is to do the items.
  - Friday demos (2026-09-18): Amanda dashboard enhancements (Huddle); show & tell — Tommy physical
    access event sources, Eugenio cross-repo hardware / Dallas rail farm test automation, Renan
    global OAuth login, Jason "Engram mount" (sic).

  ### Possible follow-ups (your call — nothing sent or created)

  - Share the Workup/TypeSafe dedup and blind-pass findings with Laura, given dedup/prior-art and
    "vectorize Linear" are now her team's stated direction.
  - Check whether ENT's Blocked status has a review step, since the known failure mode is tickets
    rotting there.
  - Check labels on Claude/Golem-created ENT tickets against Laura's comment.
  - Back up Looms before 2026-11-20.
  - Be aware of the Gateway RDS switchover read-only window this week when reading enterprise
    monitors.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review this week's Eng Leads recording
updated: 2026-09-21 13:52:32.066942
waiting_on: null
waiting_since: null
working_on: false
---

Watch this week's Eng Leads meeting recording (meets Thursdays; recording usually posted Thursday evening/Friday).

The files are in my downloads folder