---
area: null
completed_at: null
contexts: []
created: 2026-08-05 21:26:26.201560
defer_until: null
due: 2026-08-06
energy: low
id: 2026-08-05T2126-do-first-draft-typed-sag
order: 1
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

  ---

  ## Agent run 2026-08-06T14:15 — added R5 (role visibility)

  Added a fifth requirement per your instruction: support-user roles must not be visible to hotel
  staff. Same file. Your instinct for default-roles-plus-display-config was right, and the code
  backs it harder than expected.

  ### Why the enum approach wins (evidence, not just taste)
  - **The idiom already exists, and only for default roles.**
    `PropertyStaffRoleService.should_hide_default_role` / `filter_visible_default_roles`
    (`permissions/services/property_staff_role.py:79-93`), driven by
    `Hotel.rollout_hide_property_staff_default_role`. Its docstring already claims to be
    "the single source of truth… consumed by every endpoint that surfaces default roles to the UI".
    Custom `PropertyRole` rows have **no** hidden/internal concept anywhere — we'd be inventing one.
  - **There is already a hidden default role, done badly.** `ANALYTICS_STAFF`/`ANALYTICS_MANAGER`
    never appear in the roles list endpoint because `list_create_roles.py:106-124` hardcodes a
    two-element allowlist. We'd be formalising existing ad-hoc behaviour.
  - **Custom roles demonstrably drift.** `permissions/services/deactivation.py:82,97` already creates
    customer-visible custom roles named from default-role labels.

  Proposed: `INTERNAL_DEFAULT_ROLES` frozenset in `default_role.py` **plus a classification assert**
  matching the file's existing convention, so adding a default role without deciding visibility is a
  startup failure rather than a silent leak. Then one unconditional check at the top of the existing
  `should_hide_default_role`, so all six current call sites inherit it free.

  ### Two escalation paths found — these change the sequencing
  Hiding is not just cosmetic. Nine call sites bypass the existing filter, and two are security issues:
  - `permissions/views/delete_update_role.py:52` accepts **any** `DefaultPropertyRole` as
    `replacement_default_role`, with only a permission-subset check.
  - `hotel_staff/services/assignable_roles.py:97-99` offers any default role whose permissions are a
    subset of the caller's.

  An impersonated support user under a `check_in_configuration` grant holds both the advanced
  permissions and (via the base role) user management — so the subset test passes and it could grant
  the internal role to a permanent hotel user, outliving the 24h grant. I've made rejecting internal
  roles on both paths a hard requirement and **moved the visibility work to step 1 of the rollout**,
  ahead of creating any internal role.

  Also: `HotelStaffPropertyRolesTable.vue:106-111` `isDefaultRole()` is a hardcoded two-element test
  that would misroute a third default role as a role UUID — so it *breaks*, not just leaks.

  ### Correction to the earlier draft
  I'd written that we'd need to deviate from the `default_role.py` catch-all convention and extend its
  assertion. Not so — assertion 1 is `set(Permission) == union(all role permission sets)`, which any
  new default role satisfies. Only the context-mapping assertions need a mechanical entry. No framework
  deviation required, which also retires the caveat I posted in Slack on 31 Jul.

  ### Design improvement found while verifying
  `PropertyRoleGrant` has no uniqueness constraint on `(user, hotel)` and
  `RoleService.grant_default_roles_to_user` already takes a list (`permissions/services/role.py:288-321`).
  So a type maps to a *set* of composable internal roles — `CANARY_SUPPORT_BASE` +
  `CANARY_SUPPORT_CHECK_IN_CONFIG` — rather than one monolithic role per type.

  ### New adjacent finding: the support user itself is visible
  `hotels/selectors/hotel_staff.py:22-44` excludes `canaryadmin*` but **not** `support-*` or
  `TrainingUser*`. So SAG support users appear in the hotel's own user list today, labelled
  "Property manager". Hiding the role but not the user leaves a "Support User" row with a blank role
  column, which is arguably worse. Three options written up; I lean toward keeping the user visible
  (transparency that access exists is a feature) but it's a trust call for Blake. New open questions 11-12.

  ---

  ## Agent run 2026-08-06T15:10 — adversarial review + corrections

  Reviewed the PRD against the code rather than against itself. Four of my own claims were wrong;
  all four are corrected in the document. Six design-level critiques added.

  ### Factual errors found in my own draft (all now fixed in the doc)
  1. **"Access lapses at `ends_at`" was false.** `ends_at` has NO request-time enforcement. The only
     per-request check is `impersonated_user.is_active` (`impersonation/middleware.py:61`).
     `_end_support_user_access()` runs synchronously on revoke and Linear-close, but for natural expiry
     only from the `sweep_expired()` **cron** (piggybacking `cron_deactivate_training_users`, whose
     schedule is not in this repo). So real access = TTL + up to one cron interval, and if the cron
     fails silently, access never expires. This matters because R4(c) proposed per-type TTLs as a
     security dial — a dial that isn't enforced. Added a requirement for a request-time `ends_at` check
     before any TTL below 24h ships. Also: the 60-min session cap only fires on navigation to
     `unimpersonate` — the code comment admits a session may never expire.
  2. **`assignable_roles.py` is NOT a bypass.** It already calls `should_hide_default_role()` in its
     `for default_role in DefaultPropertyRole` loop. So R5 closes it for free — there is ONE open
     escalation path (`delete_update_role.py:52`), not two. I'd inflated both the scope and the alarm.
     The sharper point survives though: role *assignment* is currently authorized by a *display* filter.
     That coupling is undocumented and one refactor from breaking, so the explicit server-side guard is
     still required — as defence in depth, not as closing an open hole.
  3. **"All three enforcement points" for requester-only was wrong — there are six.** Missing:
     `internal_support/admin.py:360-366` (control_hotel_button), `_list_for_hotel:361-374`, and
     `AccessRequestDetailPage.vue:81-92`. Only two actually grant access; four are discovery surfaces.
     Documented the asymmetry so effort gets cut from the right end.
  4. **My proposed assert was wrong.** `set(X) == A | B` permits a role in BOTH sets. Needs a
     disjointness assert too. Also noted asserts are stripped under `python -O`.

  ### New findings
  - **MFA would be theatre.** `api_gateway/views/private/validate.py:143-144` sets
    `mfa_satisfied = True` unconditionally for impersonated sessions, with a comment saying so. Since
    impersonation is the only path these permissions are used on, adding them to
    `REQUIRES_MFA_PERMISSIONS` buys nothing. Recommend not gating for v1 and raising the bypass with
    Blake separately. New question 13.
  - **The audit claim is unverified for the first consumer.** "Attribution falls out for free" only
    holds for `EventableModelMixin` models that dispatch events. Nobody has checked whether the check-in
    configurator's models do. If they don't, the accountability argument that justifies the whole SAG
    route is hollow for exactly this feature. Promoted from footnote to a requirement on ADT. Question 14.
  - **Narrowing the approver pool fights the friction goal.** I'd presented R4(a) as a pure win. Today's
    routing hits all primaries + backups — maximally available. Scoping to IM leads reduces who can
    unblock a request, against a 3-day decision TTL. Changed the recommendation to *widen, not replace*.
    Also: my "intersect type pool with segment pool" is undefined given `get_hotel_segment()` returns
    None for every hotel. Question 16.
  - **I recommended relaxing a security constraint I don't understand.** One-open-grant-per-hotel is a
    standing-access limiter; I leaned "yes, relax it" while admitting I hadn't checked why it exists.
    Flagged for downgrade to investigate-first.
  - **`reason` + `grant_type` with "one picker sets both" is the worst option** — two fields that must
    correlate, coupled only by UI convention, no enforcement. Will drift. Should be fully independent,
    or governed by a mapping with an assert.
  - **Hiding from hotel staff also hides from the support user.** `filter_visible_default_roles` doesn't
    know who's asking, so CS operating under a grant sees a blank role for itself. Functionally fine,
    cosmetically confusing — the requirement says "hidden from hotel staff" but the mechanism is "hidden
    from everyone."

  ### The main structural critique — added as §10, needs your call
  The document is bigger than the problem. One team blocked on one capability; five requirements, seven
  steps, sixteen questions, eight owners — against Stephanie saying nobody has SAG context and "let's
  just move." Proposed a v1 (R1+R2+R5+the type = six blocking questions, four of them eng calls) and a
  v2 (R3+R4 = the CS/product questions). Counter-argument stated too: R4 is where Vibhor's friction
  concern actually gets answered, so deferring it has a real cost. **This is a recommendation, not a
  decision — it's yours to make.**

  Also softened §1's "Blake, Wenjun and Vibhor all converge" — Vibhor argued for /manage on 23 Jul and
  moved conditionally. Everyone reading this was in that thread; overclaiming consensus loses them. The
  conditional framing also makes R4 look necessary rather than gold-plated.

  ---

  ## Agent run 2026-08-06T15:30 — private Notion decisions doc created

  **Created:** "Typed Support Access Grants — Decisions"
  https://app.notion.com/p/3b48146861518198ac27c246cb4baf07

  Workspace-level **private** page (no parent, not in a teamspace, not shared with anyone).
  Brief, decisions-only, no implementation detail — technical where the decision is technical.

  Structure: short context from the Slack channel (the adminland-vs-/manage debate and Vibhor's
  conditional acceptance) → 15 decisions in five groups (location/access model, capability, role
  visibility, approval/binding, corrections required to current behaviour) → v1/v2 scope split with the
  counter-argument stated → 7 open questions with owners.

  The full PRD with implementation detail, code references and the adversarial-review corrections
  stays local at `/Users/garethlloyd/projects/plans/typed-support-access-grants-prd.md`.

  Nothing posted to Slack or Linear. The Notion page is private — sharing it with Stephanie/Laura or
  linking it in the channel is still your call.

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
updated: 2026-08-06 15:30:00.000000
waiting_on: null
waiting_since: null
working_on: true
---

Check https://canarytechnologies.slack.com/archives/C0BKDAG8FMY on slack. 

Check my granola 1-1 wiht STephanie yesterday evening. 

First job is to plan the PRD with high level requirements including:
* New type field
* New mechanism for assigning permissions to roles attached to support_user, rather than just using property manager. 
* Mechanism gated on type to restrict impersonation to requester only
* Approval process varied on type