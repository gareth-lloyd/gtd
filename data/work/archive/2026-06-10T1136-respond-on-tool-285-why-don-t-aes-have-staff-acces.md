---
area: null
contexts:
- react
created: 2026-06-10 11:36:37.006318
defer_until: null
due: null
energy: low
id: 2026-06-10T1136-respond-on-tool-285-why-don-t-aes-have-staff-acces
order: null
output: |-
  ## Agent run 2026-06-10T14:54

  Investigated why AEs lack staff access and drafted a reply for TOOL-285 (not posted —
  awaiting approval).

  ### Findings

  - The properties page endpoints (`onboarding/views/properties.py`) are gated by
    `IsStaffWithPermissionValidator`: they require BOTH `is_staff=True` AND the Django
    permission `onboarding.view_salesforcehotelaccount`. AEs have neither, so the API
    401s and the SPA renders blank — exactly what Candice and Fandy (APAC AEs) hit in
    the Slack thread.
  - Why AEs aren't staff: historical, by design. `is_staff` has always meant "internal
    user who gets Django admin + internal tooling". Sales/AEs only ever needed demo-hotel
    access, granted via the Demo portfolio (Portfolio Super Admin) without staff — there
    is a long-standing comment in `canary_staff_service.py` noting that not all employees
    have is_staff. Gareth's own PR #27187 (June 2025, "Limit demo access to AEs") created
    the ACCOUNT_EXECUTIVES group with an explicitly empty permission set + Demo portfolio
    access, preserving that design.
  - Ongoing reason to be careful: `is_staff` is load-bearing beyond Django admin —
    it bypasses `hotels.company_admin` in `CompanyManagementPermission`
    (canary/mixins.py:19), grants "control hotel" (any-hotel dashboard access) on login
    redirect (hotels/views/views.py:790), is the operator class for
    StaffGatekeeper/IsStaffValidator internal tools, and forces Google-SSO-only login.
    So adding aes@ to GROUPS_WITH_STAFF_ACCESS grants much more than the properties page.
  - Code comment at canary_staff_service.py:1132: "do not update ANY team permissions
    without notifying Blake first" — which is why Blake was tagged.

  ### Two viable options

  1. Follow the AI_ANNOTATORS precedent: add ACCOUNT_EXECUTIVES to
     GROUPS_WITH_STAFF_ACCESS + grant view-only `onboarding.salesforcehotelaccount`.
     Simple, but knowingly expands AE access to all hotels via the staff bypasses above.
  2. (Preferred) Decouple the properties page from staff: relax `_PropertyAuth` to
     permission-only (keep MFA_REQUIRED) and grant AEs just
     `onboarding.view_salesforcehotelaccount` via their group's model_grants. Permissions
     are assigned independently of staff status, so this works. Smallest blast radius;
     the page's "open in Django Admin" links would still 403 for AEs.

  ### Draft Linear reply (NOT posted — needs approval)

  > Mostly historical, but there's a real ongoing reason to be deliberate.
  >
  > **History:** `is_staff` has always meant "internal user who gets Django admin +
  > internal tooling". Sales/AEs never needed it — they get demo-hotel access via the
  > Demo portfolio, which doesn't require staff. When I limited demo access to `aes@`
  > last June (#27187) that design was preserved: AEs have an explicitly empty Django
  > permission set. The properties page is the first internal tool aimed at them.
  >
  > **Why it's not a one-line change:** `is_staff` is load-bearing beyond Django admin —
  > it bypasses `hotels.company_admin` checks, gives "control hotel" (any-hotel
  > dashboard) access on login, and is the operator class for all internal-tools
  > gatekeepers. Also, staff alone wouldn't fix this ticket: the properties endpoints
  > require `is_staff` AND `onboarding.view_salesforcehotelaccount`, and AEs have no
  > model grants. Candice's blank page is the API 401ing on the staff check.
  >
  > **Can we give them access? Yes — two options:**
  > 1. Add ACCOUNT_EXECUTIVES to GROUPS_WITH_STAFF_ACCESS + a view-only
  >    `salesforcehotelaccount` grant (the AI_ANNOTATORS pattern). Simple, but knowingly
  >    expands AE access to all hotels via the staff bypasses.
  > 2. Decouple the properties page from staff: relax `_PropertyAuth` to
  >    permission-only (keeping MFA) and grant AEs just
  >    `onboarding.view_salesforcehotelaccount`. Smallest blast radius — AEs get the
  >    properties page with no admin/any-hotel side effects (the "open in Django Admin"
  >    links on the page would still be blocked for them).
  >
  > I'd lean (2). Per the note in `canary_staff_service.py`, team-permission changes
  > need Blake's sign-off first — Blake, thoughts?
project: null
source_id: https://linear.app/canary-technologies/issue/TOOL-285/ae-unable-to-access-the-properties-page
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Respond on TOOL-285: why don''t AEs have staff access?'
updated: 2026-06-10 15:17:39.694422
waiting_on: null
waiting_since: null
working_on: false
---

sbarry @mentioned you and blake: "Why do AEs not have staff access (GROUPS_WITH_STAFF_ACCESS)? Historical or ongoing reason? Can we give them access?"
https://linear.app/canary-technologies/issue/TOOL-285/ae-unable-to-access-the-properties-page