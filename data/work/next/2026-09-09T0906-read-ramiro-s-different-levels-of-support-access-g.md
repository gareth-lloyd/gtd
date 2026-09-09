---
area: null
completed_at: null
contexts:
- deep
created: 2026-09-09 09:06:25.480349
defer_until: null
due: 2026-09-09
energy: high
id: 2026-09-09T0906-read-ramiro-s-different-levels-of-support-access-g
order: null
output: |
  ## Agent run 2026-09-09T10:12:57.990976

  Read the full design (Notion, last edited 2026-09-09T04:10Z, status WIP) and verified its
  claims about existing code against backend/canary on master. Overall: the doc is accurate
  about the current architecture, the milestone sequencing is right, and the "Alternative
  solutions" reasoning holds up. Findings below are ordered by how much they should change
  before Ramiro's final pass.

  ## 1. BLOCKING — "requester binding is the whole gate" is not correct

  The doc says: threading the acting staff user into `is_active_support_user` and
  `get_active_support_user_for_hotel` and comparing against `requested_by` "is the whole
  gate." Both call sites disagree.

  **`impersonation/views/impersonation.py:47-52`** — `is_active_support_user` is NOT the
  access gate. It is one clause of the `can_impersonator_write` OR:

      can_impersonator_write = (
          request.user.has_perm("impersonation.can_impersonate_without_impersonation_access_code")
          or is_training_user(user)
          or SupportAccessGrantService.is_active_support_user(user=user)
      )

  Making that clause return False for a non-requester does not refuse impersonation — it
  downgrades it to the access-code path. The support user is created with a `UserProfile`
  (`_provision_support_user`, support_access_grant.py:498), so it has an
  `impersonation_access_code`; and it is `is_staff=False`, so the
  `is_superuser or is_staff -> PermissionDenied` guard below never fires. Net effect: a
  colleague with `impersonation.can_impersonate` still opens a read-only session as someone
  else's support user, and anyone holding
  `can_impersonate_without_impersonation_access_code` gets full write regardless, because
  that clause is first in the OR. Requester binding needs an explicit refusal in the view,
  not a change to how `can_impersonator_write` is computed.

  **`hotels/views/views.py:1424`** (`_find_or_create_user_to_impersonate`, the
  `control_hotel` path) — a `None` return does not refuse either. It falls through to
  selecting a real property-manager user at the hotel, or creating a new one. So binding on
  this path silently substitutes a regular PM impersonation for the support user rather than
  denying. The Milestone 1 text ("refuse a mismatch and log it") is the right behaviour; the
  architecture section's "comparing against `requested_by` is the whole gate" is what needs
  rewording, and both call sites need the explicit refusal spelled out.

  **Third lookup the doc doesn't name**: `has_temporary_support_access`
  (support_access_grant.py:460) also resolves support-user status and gates support-only
  product actions such as adminland Voice Setup. It takes the impersonated user rather than
  the actor so it isn't a binding hole, but "the two support user lookups" should be three.

  ## 2. BLOCKING — dropping the constraint leaves support-user selection non-deterministic

  `get_active_support_user_for_hotel` (line 442) uses `.first()` with **no `order_by`**.
  That is safe today only because `support_access_grant_one_open_per_hotel` guarantees at
  most one row. The doc drops that constraint and replaces it with an *implicit* assumption
  that (hotel, requester) is unique — but nothing enforces it. Two grants from the same
  requester on the same hotel with different reasons produce two support users with
  different role sets, and `.first()` picks arbitrarily. Concretely: request a DEFAULT grant
  and a CHECK_IN_CONFIGURATION grant on the same hotel, impersonate, and which role set you
  get is up to the planner.

  Fix is small: replace the dropped constraint with a partial unique on
  (hotel, requested_by) for pending/active, or order the lookup deterministically. Worth
  noting the codebase already treats this as a known trap — see the
  "Slice rather than `.first()` to avoid an implicit ORDER BY pk" comment in
  `tasks/slack_interactivity.py:85`.

  ## 3. The segment-deprecation metric cannot answer the question it is being asked

  The doc keeps segments "for now" and plans to "measure % of requests resolved without a
  segment" to decide whether to delete them. But `get_hotel_segment` is still a stub
  returning `None` for every hotel (`services/hotel_segments.py`) and this design explicitly
  does not implement it. So after the group step lands, the segment branch will never fire —
  not because segments are unnecessary, but because the input is hardcoded to None. The
  metric will read 100% "resolved without a segment" by construction and cannot distinguish
  "segments are dead" from "the stub was never filled in." Either implement
  `get_hotel_segment` or state that the deprecation call is really a call about whether
  anyone will ever implement it. As written the measurement is decorative.

  ## 4. Narrowing the DM list also narrows who can approve from Slack — unnamed

  `_compute_authorized_approver_emails` has two call sites, not one:
  - `support_access_grant_slack.py:314` — who gets DMed
  - `tasks/slack_interactivity.py:90` (`_is_authorized_approver`) — who may click Approve/Deny

  Today they are deliberately the same list. The design narrows resolution to a single group
  leader (or a single segment primary, or backups only), which silently narrows Slack-button
  authorisation to the same one person. Not a lockout — the API view
  (`views/support_access_grant.py:530`) and Django admin (`admin.py:196`) both go straight to
  `SupportAccessGrantService.approve` with only the change permission plus the enterprise
  gate — but it is a real behaviour change the doc never states. Also note the pseudocode
  changes the signature from `(hotel)` to `(grant)`, since the group step needs
  `requested_by`; both call sites have to change and the authz one only has a grant in hand
  anyway. Decide explicitly: does authorisation narrow with routing, or stay broad while only
  notification narrows?

  ## 5. Google Groups: a requester is in many groups, and resolution is unordered

  `GoogleGroups` (backend/shared/shared/auth/google_groups.py) is a flat enum of ~28 entries
  with heavy overlap, including `WHOLE_TEAM = team@canarytechnologies.com`, which everyone is
  in. A typical CS person matches `team@`, `cs@`, `cs-ops@`, and `support-team@`
  simultaneously. The design enforces one leader *per group* but says nothing about a
  requester matching several, and the pseudocode resolves it with:

      SupportAccessApprover.objects.filter(is_active=True, google_group__in=group_emails).exclude(...).first()

  `.first()` with no `order_by` — arbitrary leader, and it can flip between deploys. Needs
  either a precedence ordering over groups or a curated subset of `GoogleGroups` allowed as
  `google_group` choices. `team@` in particular must not be selectable, or one person becomes
  the default approver for the entire company.

  Verified as correct: the staff sync does map every `GoogleGroups` member to a Django
  `Group` named by the group's email and calls `groups.set(...)`
  (`canary_staff/services/canary_staff_service.py:1337-1349`), so resolution really is local
  and never calls Google. Minor: `google_group` is proposed at `max_length=255` while
  `Group.name` is 150.

  ## 6. Your own earlier position on requester binding is the opposite of this goal

  From your 1-1 notes with Steph (5 Aug 2026): your stated position was **don't** link the
  person who requested the grant to the person who can perform the impersonation. Secondary
  goal #3 in this doc is "a grant is only usable by the person who requested it." Same notes
  have typed SAGs as an open item with you offering to write the PRD first draft, and
  "Lauta's proposals should be adapted for SAGs."

  Worth resolving before the final pass rather than after: either you have changed your mind
  (the Drury incident in your "Readonly impersonation" note argues for binding), or Ramiro
  inherited the goal without knowing you had argued against it. Risk 1 in the doc ("requester
  binding breaks a real handoff", mitigated by re-requesting) is exactly the concern your note
  was pointing at, so it may just need you to say out loud that the re-request escape hatch is
  enough for you now.

  ## 7. Smaller notes

  - **"Enforced on every request" is not quite true.** `ImpersonateMiddleware.__call__`
    early-returns for `/canary-admin`, `/impersonate`, `/control-portfolio`, `/control-hotel`,
    and `HTTP_X_SKIP_IMPERSONATION: true` before any impersonation handling. The `ends_at`
    check has to sit relative to those returns deliberately, and the doc should say where.
  - **The `is_impersonation_expired` bug the doc identifies is never fixed.** The doc
    correctly notes it only fires when the resolved url name is `unimpersonate`. But no
    milestone touches it, and it isn't in "Out of scope." Adding `ends_at` enforcement fixes
    the window for SAG support users only — regular impersonation of real hotel users still
    has an effectively infinite session. Either scope it in or name it as out.
  - **Pseudocode nit**: `_provision_support_user` loops calling
    `RoleService.grant_default_role_to_user` per role. `grant_default_roles_to_user` takes a
    list and takes the per-user lock once (`permissions/services/role.py:288`) — call it once
    with the list. Also `roles: frozenset[...]` gives non-deterministic iteration order, which
    is a smell for logging/reproducibility even if the grant is order-independent.
  - **Verified correct**: `DefaultPropertyRole.CANARY_SUPPORT` exists and holds exactly
    `CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS` (`permissions/constants/default_role.py:143`),
    which is the sole `CANARY_ONLY`-strength permission
    (`permissions/constants/permission.py:614`). The enterprise gate is applied inside
    `approve()` itself (support_access_grant.py:194), so it covers all three approve paths —
    the doc's description of it as live is right.

  ## Not done

  - Could not read the Slack DM thread (no Slack tooling in this session), so anything Ramiro
    said in the message itself is unreviewed:
    https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1788933604308199
  - Nothing posted anywhere. No Notion comments, no Slack reply. Findings 1, 2, 4 and 5 are
    the ones worth getting to him before the final pass; 6 is the one only you can answer.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1788933604308199
tags:
- morning-gtd
- slack
time_minutes: 40
title: Read Ramiro's 'Different levels of Support Access Grant' eng design before
  his final pass
updated: 2026-09-09T10:12:57.990976
waiting_on: null
waiting_since: null
working_on: false
---

He sent the draft last night and will do a final pass this morning; we discussed reason-vs-type mapping and approver resolution yesterday. Design: https://app.notion.com/p/canarytechnologies/Different-levels-of-Support-Access-Grant-3ce81468615180a49485efb90e609963
https://canarytechnologies.slack.com/archives/D08CJ15NW21/p1788933604308199