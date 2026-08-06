---
area: null
completed_at: null
contexts: []
created: 2026-08-05 21:26:26.201560
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T2126-do-first-draft-typed-sag
order: null
output: |
  ## Agent run 2026-08-06T13:45

  **Deliverable:** first-draft PRD written to `/Users/garethlloyd/projects/plans/typed-support-access-grants-prd.md`.
  Local only — nothing posted to Slack, Notion, or Linear.

  ### Sources read
  - Slack #tmp-check-in-configuration-location (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY),
    full channel + the 4 substantive threads (Blake's directives, my 31 Jul proposal thread,
    Lea's field-level-gating thread, Vibhor's friction thread + his closing summary).
  - Granola "Stephanie Barry 1-1", 2026-08-05 21:16.
  - Full code map of the SAG / permissions / impersonation systems in the canary repo.

  ### Commitment confirmed
  Stephanie in-thread 2026-08-05: "confirming that Gareth will draft this"
  (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785955984265229).
  She said Laura is happy to see it rolling without a pre-review; only Sam has SAG context on the tools team.

  ### PRD covers the four requested requirements
  1. **New type field** — `grant_type` + a code-side `GrantTypeSpec` registry (permissions, approval,
     TTLs, requester-only, hotel-state rules). Initial types: `general_support` (today's behaviour) and
     `check_in_configuration`. Narrowing types (`user_management`, `read_only_investigation`) sketched to
     show the pattern scales both ways.
  2. **Type-derived permissions for support_user** — replaces the hardcoded Property Manager grant.
     Plus the two new check-in permissions and a `CANARY_SUPPORT` default role above Property Manager.
  3. **Requester-only impersonation, gated on type** — three enforcement points identified.
  4. **Approval varied on type** — four independent dials: approver pool, approval-required-at-all
     (auto-approve), TTLs, two-eyeballs.

  Plus: rollout sequenced in 6 independently-mergeable steps, 10 open questions with my lean on each,
  success criteria, and a linked source appendix.

  ### Findings from the code that changed/sharpened the design
  - **`reason` already exists** on the model (`no_property_manager | new_product_onboarding | other`)
    but drives no behaviour. PRD recommends a separate `grant_type` rather than promoting `reason`,
    with one UI picker setting both. Flagged as decision #1 — worth a second opinion.
  - **support_user gets the FULL Property Manager role** today
    (`internal_support/services/support_access_grant.py:494-499`). That's the concrete form of the
    "SAGs give general access to a hotel" problem I described on 23 Jul. Typing narrows as well as widens.
  - **Requester-only is a bigger gap than Stephanie's question implied.** `is_active_support_user()`
    takes no actor argument at all, AND `support_user_username` is exposed on the hotel-scoped grant GET
    with *no permission check* (`views/support_access_grant.py:102-123, :361-374`), AND Django admin's
    `control_hotel` button prefers the active grant's support user. Any staff member with
    `can_impersonate` can pick up anyone's grant and get write mode. Three enforcement points, not one.
  - **`get_hotel_segment()` is a stub returning `None`** (`services/hotel_segments.py:4-14`), so *every*
    approval request today routes to all primaries + backups. Segment routing exists but is inert —
    relevant to Stephanie's "we can set implementation managers as approvers" idea, since the plumbing
    is there and just needs a type dimension.
  - **TTLs are module constants**, not fields (`DECISION_TTL = 3d`, `ACCESS_TTL = 24h`) — trivial to
    move onto the type spec.
  - **One-open-grant-per-hotel partial unique constraint** will block a config grant when a general
    support grant is open. PRD proposes relaxing to per-hotel-per-type.
  - Two-eyeballs is enforced on approve/deny but **not** on revoke.
  - Impersonated-action audit only covers `EventableModelMixin` models that dispatch events — there is
    no blanket per-request trail. Worth knowing before we lean on "attribution falls out for free."

  ### My open question back to you
  Requester-only (decision #4) is the one place I couldn't resolve from the sources. If the requester
  goes offline mid-session, v1 as drafted forces a re-request. That's exactly the friction Vibhor is
  worried about. I lean "accept re-request" but it needs a CS-side reality check.

  ### Suggested next steps (none taken)
  - Read the draft; it's written to be reacted to, not approved.
  - If it's roughly right, the natural destination is a Notion page alongside Sam's
    "Requesting Support Access to a Hotel" doc, then a link in the Slack thread. Both need your say-so.
  - Decisions 5, 6 and 7 (auto-approve, approver pool, access TTL) need Stephanie/Vibhor before the
    tools team can size the work.
project: 2026-04-10T0840-ticket
source_id: null
tags: []
time_minutes: 5
title: Draft PRD for adding typed behaviors.
updated: 2026-08-06 13:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Check https://canarytechnologies.slack.com/archives/C0BKDAG8FMY on slack. 

Check my granola 1-1 wiht STephanie yesterday evening. 

First job is to plan the PRD with high level requirements including:
* New type field
* New mechanism for assigning permissions to roles attached to support_user, rather than just using property manager. 
* Mechanism gated on type to restrict impersonation to requester only
* Approval process varied on type