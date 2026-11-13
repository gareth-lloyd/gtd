---
area: null
completed_at: 2026-11-12 15:20:16.451107
contexts: []
created: 2026-11-09 22:17:47.951947
defer_until: null
due: null
energy: low
id: 2026-11-09T2217-review-pitches
order: null
output: |
  ## Agent run 2026-11-10T14:23:36+0200

  Source: ENT 2026Q4B pitches, 2026-11-09 (https://app.notion.com/p/41381468615180bab875de4054d8a9b0).
  I read the AI summary and the full transcript. I could not read the three embedded slide decks
  (Notion returns them as unknown external objects), so anything only on a slide is missing here.
  Nothing was posted or edited anywhere.

  ### Outcome of the meeting
  No pitch was approved as a standalone project. Connor's direction: all four are the same theme
  ("get the fix closer to the person who knows how to fix it"), build interface-agnostic backend
  endpoints rather than new UIs, and plug into Settings Assist (Sudarshan and Steph's harness)
  instead of building a harness. One shared project for "enterprise-specific extensions of
  Settings Assist", driven by whoever is on triage rotation. Next step is Andrea messaging Laura
  and Sudarshan for time. Follow-up meeting is next week.

  ### Where you are named or touched
  - Martin's drift detection pitch says it builds on "what Gareth has been working on". That is
    the only mention of you. No action item is assigned to you.
  - My inference, not said in the meeting: the pitch (CSM-defined rules, regex shape checks,
    reusable across brands) overlaps the binding-rules / rules_based_configuration work
    (ENT-7726), and Ryan's point that rules are hardcoded and would need database support is the
    design question you are best placed to answer.
  - My inference: Staff Assist depends on an agent knowing what each setting means, which is
    what the settings field guide produces. Worth raising with Sudarshan if it has not been.

  ### The four pitches
  1. Staff Assist (Ryan). LLM agent on the Settings Assist harness for internal staff requests
     (portfolio adds, permissions), gated on the staff user's own permissions, with a one-click
     engineer approval queue for anything beyond them. Claimed: ~28 triage tickets/week, 2 of 3
     are access requests, ~3 days each. Ryan says an engineering design is already started.
     Connor's three approval tiers: engineer, brand CSM, fully automatic. Model the approval on
     Steph's Slack support-access-grant flow.
     Open: Tincho asked whether the agent gets free use of endpoints or only pre-approved flows;
     left unresolved. Andrea said some permission gates will have to loosen, Ryan said permissions
     stay as they are today. Those two positions conflict and nobody reconciled them.
  2. Drift detection with live test cases (Martin). Today's policies only check equality or set
     membership; free-form settings are unchecked. Proposal: attach runnable checks (regex shape,
     then live checks such as "PMS gateway works") shown and acknowledged in the existing drift
     screen. Connor wants evidence first: list real things that went wrong for one customer, talk
     to Ani and CSMs, then decide how flexible to make it. Andrea wants one milestone this block;
     regex is the candidate. Andrés suggested reusing segmentation condition logic. Connor also
     flagged that DB-only drift checks miss GrowthBook gating; Ryan pushed back on depending on
     GrowthBook itself.
  3. User access diagnostics UI (Andrés). Internal checklist page per user: SSO role attributes
     received, duplicate or blocked accounts, later actions (merge accounts, copy access, rebind
     SSO name ID). Estimate: ~25 tickets/quarter saved read-only, ~100 with actions. Direction:
     locked-down backend API first with audit logs, UI and LLM on top.
  4. Portfolio health dashboard (Andrea). One page in Manage per portfolio: configuration
     progress and failures, plus live health (drift findings, health checks, hotel table), with
     Slack alerts when a hotel changes health state. Must be generic across IHG, Wyndham and
     others. Least discussed; ran out of time. It is a new UI, which is the thing Connor said he
     is less excited about, and that tension was not addressed.

  ### Corrections to the Notion summary
  - Action item "Connor Swords to grab 15 minutes with Sudarshan and Steph" is wrong. Connor
    asked Ryan to do it; Ryan agreed.
  - The numbers disagree between pitches: Ryan says two thirds of triage tickets are access
    requests, Andrés says about half. Ryan's "3 days, or 32 hours" also does not add up unless
    it means working hours. At 28 tickets/week, Andrés's 100 tickets/quarter is under a third of
    volume. Worth one agreed baseline before anyone sizes these.
  - The transcript's speaker labels blur Connor and Ryan in several places, so attributions in
    the summary's Staff Assist feedback section are unreliable.

  ### My read
  - Pitches 1 and 3 are one project with two front ends. The backend action layer (endpoints,
    permission checks, audit logs, approval queue) is the real deliverable, and it is useful even
    if Settings Assist slips.
  - Biggest risk: everything is gated on a harness another team owns, and that conversation has
    not happened yet. "Triage engineer drives it in downtime" has, by Andrea's own account, been
    proposed before and not done.
  - Pitch 2 has the clearest small first step (regex policy type) but the CSM-defined, dynamic
    rules part is a much larger change than the pitch implied.

  ### If you want to act
  - Talk to Martin about how live test cases sit on the existing rules work before he picks the
    milestone.
  - Tell Andrea or Connor the "15 minutes with Sudarshan" action belongs to Ryan.

  ## Agent run 2026-11-10T14:46:54+0200 (looking for substance beyond the transcript)

  The three slide embeds on the meeting page are unreadable through the Notion API (they fetch
  as blank blocks). Searching Notion, Slack and Drive turned up one real pitch document:

  - Ryan's "Staff Assist: self-service assistant for Canary staff (research draft)"
    (https://app.notion.com/p/40d814686151810aa5f7e52eb21e8291), read in full. It is a full
    engineering design, updated Nov 6 after a code-level review of master.

  Nothing written was found for Andrés's or Andrea's pitches (Andrea called hers "quick Claude
  slides"). For Martin's, the only related doc is the separate "Eng Design: GJM Drift Detection"
  (https://app.notion.com/p/41381468615181089aa2d0e08023625a, ENT-8066), which is up for review
  but is not the live-test-cases pitch. I did not read it.

  ### What Ryan's doc adds
  - Numbers, sourced from Linear: 131 of 232 staff-filed ENT tickets (56%) over Aug 21 to Nov 2
    were identity, access or portfolio requests, plus 67 Oncall access-request tickets in a
    month. Together ~28 a week from 37+ requesters. 66% of SLA-bearing ENT tickets are in this
    group. Golem takes first pass on about half of Enterprise triage; 58 of 134 graded runs
    (43%) were used as-is, but an engineer still runs every change.
  - Safety model: the model never writes. It only reads and prepares; a person approves an
    immutable before/after plan with a required reason, and the write runs through a
    staff-gated endpoint under the approver's own request. Model-written scripts are rejected.
  - Most of the needed staff endpoints do not exist: hotel role grants, hotel user and
    portfolio user creation, email change, reactivate, merge, SSO org edits, feature groups.
    Only portfolio hotel and portfolio user endpoints exist today.
  - It is not just "extensions on the harness". Settings Assist assumes a hotel everywhere, so
    Staff Assist needs a host seam in Settings Assist core (~40 call sites plus a migration),
    sequenced after TOOL-975 and TOOL-972. The Resolution Agent project plans no non-hotel
    scope, so this needs their agreement first.
  - "Saved queries" are the delegated-approval queue: separate entity, 7-day deadline, Slack DM
    to eligible approvers, no self-approval, preview rebuilt as the approver.
  - Permissions are a prerequisite: Google-group permissions only express view/add/change/delete
    and the login sync never removes one, so custom action permissions and Blake's sign-off are
    needed.
  - Seven milestones, unsized. Milestone 2 (staff endpoints for hotel access and portfolios) is
    useful without the assistant. Pilot is milestones 1 to 5. Merge, deactivate and SSO come
    last because they are irreversible or undone by SSO login.

  ### Corrections to my first run
  - I said the triage numbers disagreed between Ryan and Andrés. With the doc they roughly
    agree: 56% of staff-filed ENT tickets, 66% of the SLA ones. The 28 a week is access-type
    tickets across ENT and Oncall, not total triage volume.
  - Connor's "build into the harness, don't build the harness" understates the work: the doc
    requires changes inside Settings Assist core that another team must accept.
  - Milestone 2 is the same backend layer Andrés's pitch needs, which supports treating
    pitches 1 and 3 as one project starting there.
project: null
source_id: null
tags: []
time_minutes: 5
title: review pitches
updated: 2026-11-12 15:20:16.451097
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/41381468615180bab875de4054d8a9b0?v=5f62f3dba7234433870e5cfeb927403f&source=copy_link