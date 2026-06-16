---
area: null
contexts:
- react
created: 2026-06-16 11:31:36.186451
defer_until: null
due: null
energy: low
id: 2026-06-16T1131-answer-andrea-on-ent-6511-historical-context-for-i
order: null
output: |
  ## Agent run 2026-06-16T13:32

  Researched the history of `PLATFORM_CAN_BYPASS_IP_VALIDATION` to draft a reply
  to Andrea on ENT-6511. NOTHING POSTED to Linear — draft below for you to send.

  ### Bottom line
  I don't have firsthand memory of the default-grant decision — it predates my
  direct involvement (authored by Montserrat Pladevall, original IP-list feature
  by Navid Khan). But git + my own notes reconstruct a clear story, and I agree
  with Lautaro that the default-role bypass is surprising. Safe immediate fix for
  The Goring is a custom role without the bypass; changing the default role is a
  broader behavior change that needs a comms/migration plan.

  ### What the git history actually shows
  - `edbd340b` (PR #9759, 2023-09-07, Montserrat Pladevall) *created* the
    permission. It did two things at once: added it to the default Manager-type
    roles in `default_role.py` AND added it to `LEGACY_PERMISSION_MAPPING` in
    `permission.py`.
  - The original IP allowlist feature came just before: "IP Validation: Adds
    list" (#9236, Navid Khan, 2023-08-07). Then `f99999f9` (COR-435 / #9821,
    Montserrat, 2023-09-13) wired the *new permissions framework* into the IP
    check (`is_request_ip_address_allowed_by_hotel`, `hotels/decorators.py`).
  - PR #9759's description explicitly updates the **SSO Documentation** — so IP
    allowlisting was conceived as an enterprise / SSO platform-access control,
    not a per-property security toggle.

  ### My read on *why* it was default-on
  The tell is that the permission was dropped into `LEGACY_PERMISSION_MAPPING` at
  the same moment. That mapping is what existing roles inherited when the new
  permission framework rolled out. Granting "can bypass IP validation" to the
  default/legacy roles was a **non-breaking-rollout choice**: turning the feature
  on shouldn't suddenly lock out the large population of existing users who never
  asked for IP restriction. So the default biased toward fail-open.

  ### Color from my own notes (Bear) — note the timeline nuance
  My daily logs + on-call notes from **May 2024** show IP filtering as a
  **Wyndham** enterprise/SSO platform-access feature, and there was a real
  incident — **ENT-3874** "wyndham-corporate-user-unable-to-access-property … due
  to IP", logged as *"Waiting for decision on allowing override."* i.e. Wyndham
  *corporate* users were getting locked out by IP validation and we had to decide
  whether to allow an override. That reinforced the same fail-open bias — keep
  legitimate platform/corporate users from being filtered out.
  CAVEAT: that incident is ~May 2024, while the permission itself landed Sep 2023,
  so ENT-3874 is a later reinforcement of the pattern, not the original reason.
  The authoritative paper trail for the *default-grant* decision (who approved,
  intended scope) would be PR #9759's review thread + COR-435.

  ### How the mechanism bites here (confirms Lautaro's diagnosis)
  `is_ip_address_allowed_by_hotel()` (canary/utilities/
  is_request_ip_address_allowed_by_hotel.py): returns True if the request IP is
  in the allowlist, OTHERWISE returns True anyway if the user holds
  `PLATFORM_CAN_BYPASS_IP_VALIDATION`. Because the default Property Manager role
  carries that permission, the allowlist is a no-op for default-role users —
  exactly Richard Hart's situation.

  ### Recommendation (agreeing with Lautaro)
  - Immediate: yes, move The Goring's users off the default role to a custom
    role that lacks the bypass (or strip the permission from their role) so the
    allowlist is enforced. That unblocks the customer safely.
  - Longer-term: removing bypass from the default role is the "correct" behavior
    but it's a widely-held grant (default + legacy + Marriott/4S/Aimbridge/Pyramid
    onboarding providers all set it). Changing it could lock out users at
    properties that have an allowlist configured but rely on the default role.
    Worth a deliberate migration: identify hotels with allowlists configured,
    audit who'd be affected, and split the default role / make bypass opt-in with
    comms. Not a quiet one-line removal.

  ### Draft reply for Andrea (Linear comment — NOT sent)
  > I don't have firsthand history on the default-grant decision — it predates my
  > involvement (added by Montserrat in #9759, Sep 2023; original IP-list feature
  > by Navid in #9236). But the git story is fairly clear:
  >
  > #9759 added `PLATFORM_CAN_BYPASS_IP_VALIDATION` to the default Manager roles
  > AND to `LEGACY_PERMISSION_MAPPING` in the same PR, and its description updates
  > the SSO docs. IP allowlisting was built as an enterprise/SSO platform-access
  > control, and the bypass was granted to default/legacy roles so that enabling
  > it wouldn't lock out the existing user base — a non-breaking-rollout default,
  > biased fail-open. That same bias shows up later in ENT-3874 (Wyndham corporate
  > users locked out by IP → "waiting on decision to allow override").
  >
  > So I agree it's surprising that our most-common role bypasses validation.
  > For The Goring now, the clean fix is a custom role without the bypass (or strip
  > it from their role) — don't globally remove it from the default role yet,
  > because it's widely granted (default + legacy + several brand onboarding
  > providers) and removing it could lock out other properties that rely on it.
  > If we want to fix the default properly, let's do it as a tracked change:
  > audit hotels with allowlists configured, see who'd be affected, then split the
  > role / make bypass opt-in with comms.

  Refs: commit edbd340b (#9759), #9236, COR-435/#9821, ENT-3874, ENT-6511.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6511/ip-allowlist-not-restricting-access-hotel-network-mismatch-richard
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Answer Andrea on ENT-6511: historical context for IP-allowlist default permission'
updated: 2026-06-16 13:42:32.834493
waiting_on: null
waiting_since: null
working_on: false
---

Andrea asked if you have historical knowledge of why that permission was added by default. Lautaro found it was added ~3 years ago (commit edbd340b). Add any color you have. https://linear.app/canary-technologies/issue/ENT-6511/ip-allowlist-not-restricting-access-hotel-network-mismatch-richard