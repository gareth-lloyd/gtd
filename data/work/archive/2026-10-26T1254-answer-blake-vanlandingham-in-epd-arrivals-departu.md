---
area: null
completed_at: 2026-10-27 08:29:48.172117
contexts:
- react
created: 2026-10-26 12:54:53.852382
defer_until: null
due: null
energy: medium
id: 2026-10-26T1254-answer-blake-vanlandingham-in-epd-arrivals-departu
order: null
output: |-
  ## Agent run 2026-10-26T15:10
  Nothing sent. Draft reply below, for you to post.

  ### What Blake is remembering
  The July thread in #tmp-check-in-configuration-location: Blake's requirements post (https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785363226229569), Blake asking for an "INTERNAL_STAFF permission or an is_staff-like control", and your reply "If we go that way I think it should be google group based rather than binary flag". Your proposal (main channel posts of 2026-07-30 16:45 and 2026-07-31 12:23 EEST in #tmp-check-in-configuration-location, https://canarytechnologies.slack.com/archives/C0BKDAG8FMY) was: Canary-only capabilities become ordinary Canary permissions, views never check is_staff or impersonation, training users get them before go-live, and a typed SAG's support user gets them after.

  ### That plan is built (checked on master)
  - `Permission.CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS`, strength CANARY_ONLY (permissions/constants/permission.py:162, :637)
  - `DefaultPropertyRole.CANARY_SUPPORT` holds it (permissions/constants/default_role.py:154). This is probably the "CANARY_STAFF role" Rami mentions.
  - `SupportAccessGrantType` model exists (internal_support/models/support_access_grant_type.py)
  - Guest_experience catalog/flow views gate on it.

  ### Precedent for Lea's preferred option
  PA-904 (#58534), mobile_key/access_control.py: `operator = impersonator or user; operator.is_staff and operator.has_perm("mobile_key.change_mobilekeyconfig")`. That is a Django permission on the staff member, checked under impersonation. StaffUserGatekeeper.staff_permissions works the same way for /manage routes.

  ### The gap
  Post-live, engineers need a SAG to edit config. The open question is whether some staff skip the SAG for CANARY_ONLY permissions. That's a policy call for Blake. The mechanism is already settled.

  ### Draft reply (thread: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1792792765818379?thread_ts=1792772835.919819&cid=C029BPP02H0)
  > Yes, same conversation, back in July: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785363226229569. Where we landed: no `is_staff` or impersonation checks in views. Canary-only capabilities are ordinary permissions (`CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS`, CANARY_ONLY strength) held only by the Canary Support role. You get them by impersonating someone who has that role: the training user before go-live, a SAG support user after. That's all built.
  >
  > So the question here is who gets it without a SAG on live hotels. That's a policy decision, not a new mechanism. On the options:
  > • Hardcoding for superusers / `is_staff`: I'd avoid it. It's the binary flag we said no to, and once it exists it gets reused for other things. Blake, I said "google group, not binary flag" in July and still think so; "staff" covers sales and others too.
  > • Lea's preferred option, a Django perm granted by the EPD Google group and OR'd with the hotel perm: fine by me, and there's already precedent (mobile key settings, PA-904, checks the impersonator's Django perm). Two conditions: one shared helper rather than per-view checks, and scope it to CANARY_ONLY perms so it doesn't become blanket write access on live hotels. Blake's call whether configurator is safe to have outside SAG.
  > • For this hotel right now: a UAT hotel should have a training user. Fixing that is the quickest unblock.
  >
  > Rami, agreed it won't scale as is. The Google group sync only adds perms (your thread https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1790784822781399), so if groups become the "Canary staff" identifier, that sync needs to switch to set (not just add) first.

  Background: impersonation access model doc https://app.notion.com/p/2e78146861518041beacfd081d4ea930

  ## Agent run 2026-10-26T15:40 (revised draft: defend new permissions, the problem is how engineers get them)
  Replaces the earlier draft. Checked on master: SAG types carry a per-type `auto_approve` flag (internal_support/constants/support_access_grant_type.py). The request path honours it (internal_support/services/support_access_grant.py:215), and the approved event records `auto_approved`. CHECK_IN_CONFIGURATION grants PROPERTY_MANAGER + CANARY_SUPPORT, with `auto_approve=False`.

  ### Draft reply
  > Yes, this is the July conversation: https://canarytechnologies.slack.com/archives/C0BKDAG8FMY/p1785363226229569. I'd keep the new permission (`CHECK_IN_HAS_ADVANCED_CONFIGURATION_ACCESS`) as the gate, and not add `is_staff` or a Django-perm override in these views:
  > • Adminland is a hotel-facing surface, and everything there is gated on hotel permissions. If one section checks "is this Canary staff" instead, that section has its own rule. The frontend can't tell from `Permission.ts` what will show, and every new staff-only feature adds another special case.
  > • The permission is also how we hand features to hotels later. When a section is ready for hotel admins, we add the permission to their role. That's config, not a code change. An `is_staff` check would have to be found and removed.
  > • Impersonation stays honest: you see what the user you're impersonating sees. The new permission sits on the Canary Support role, which no hotel user can hold or grant themselves.
  >
  > So the real problem isn't "how do we detect staff". It's how an engineer gets the permission, given they normally impersonate the Property Manager, who will never have it. Today that's a check-in-configuration SAG. It already provisions a support user with Property Manager + Canary Support, but it needs a second person to approve and a Linear ticket, and that delay is what's hurting.
  >
  > The SAG system already supports a per-type `auto_approve`. I'd make the check-in-configuration type auto-approve when the requester holds a Django permission granted through the EPD Google group (and loosen the Linear-ticket requirement for that type). Engineers get one-click, time-boxed, audited access. Views stay purely permission-gated, and Canary staff membership is decided by group, not by a yes/no flag.
  >
  > Separately, this UAT hotel should have a training user, which would have unblocked Dana today. And Rami's point stands: if Google groups decide access, the group sync must replace permissions, not only add them (https://canarytechnologies.slack.com/archives/C08RJU9Q7FV/p1790784822781399).

  ### Open questions for you before posting
  - Should the auto-approve be EPD-group-gated, or open to every requester of that type? Group-gated is safer, and the draft assumes it.
  - Should the Linear ticket stay mandatory for the auto-approved type? The draft says loosen it.
project: null
source_id: https://canarytechnologies.slack.com/archives/C029BPP02H0/p1792792765818379?thread_ts=1792772835.919819&cid=C029BPP02H0
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Blake VanLandingham in #epd-arrivals-departures: identify Canary Staff
  users with the permission framework'
updated: 2026-10-27 08:29:48.172094
waiting_on: null
waiting_since: null
working_on: true
---

Blake recalls a decision to use the permission framework rather than a new flag to identify Canary Staff users (impersonation access). Stephanie and Ramiro are aligned. Open 2 days, no reply from me.
https://canarytechnologies.slack.com/archives/C029BPP02H0/p1792792765818379?thread_ts=1792772835.919819&cid=C029BPP02H0