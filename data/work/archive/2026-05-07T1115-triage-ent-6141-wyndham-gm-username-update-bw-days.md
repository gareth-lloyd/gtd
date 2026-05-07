---
area: null
contexts:
- react
created: 2026-05-07 11:15:35.017206
defer_until: null
due: null
energy: medium
id: 2026-05-07T1115-triage-ent-6141-wyndham-gm-username-update-bw-days
order: null
output: '## Agent run 2026-05-07T13:35Z


  **Triage summary**


  Classic Wyndham SSO "stale username" case, not a bug. The `username` field is set
  at first SSO login and is not updated on subsequent logins, even when first/last
  name change. The display name updates correctly because the SSO sync writes `first_name`/`last_name`
  on every login.


  **Account state (per Canary Agent triage comment)**

  - Hotel: Days Inn by Wyndham Nanaimo (admin id 972, site id `04797`)

  - User: id 3473551, username `RobGreen`, display name "Leo Saad"

  - SSO IdP: Wyndham (Okta), email `manager@daysinnnanaimo.com`

  - SSO attrs: first_name=Leo, last_name=Saad, hotels=[04797], roles=[top_level]

  - Roles on hotel 972: Hotel admin, Wyndham manager, Can view credit card

  - SLA: medium-risk already; breaches 2026-05-10


  **What''s happening**

  Rob Green was the prior GM. Wyndham reused the property''s SSO mailbox (`manager@daysinnnanaimo.com`)
  for the new GM, so Okta surfaces the same SSO subject. Canary''s SSO sync updates
  name fields but keeps the original `username` ("RobGreen") because that''s the immutable
  login identifier. Leo can log in and edited the display name (which is what the
  staff list shows), but the username UI is read-only — hence the screenshot showing
  "Rob Green" still.


  Sub-asks bundled in the ticket:

  1. Update username from `RobGreen` → something correct for Leo Saad.

  2. "Not in the staff members list" — the Canary Agent comment shows he IS a property
  user with the right roles, so this is the same record showing as RobGreen. Likely
  resolves itself once (1) is addressed.

  3. Help adding more staff users — doc/macro task, not engineering.


  **Recommended path (for whoever picks this up)**


  Safest option is to rename the existing user record rather than create a new one
  (preserves audit trail, sessions, role assignments):

  - Pick a new username that fits the Wyndham-SSO convention used elsewhere (e.g.
  derived from email or site id). Confirm convention with the Wyndham/Enterprise pod
  before changing — wrong format may break SSO lookup on next login.

  - Rename via Django admin (`/canary-admin/auth/user/3473551/change/`) — but verify
  the SSO sync keys on Okta subject/email rather than `username` first; otherwise
  next login will create a fresh `RobGreen` user.

  - Alternative: do nothing to the username (it''s an internal login string, not guest-facing).
  The customer''s complaint may dissolve once they understand the staff list shows
  display name, not username.


  **Open questions to ask the requester / pod before acting**

  - Does Leo actually need the username changed, or just the displayed name in the
  staff list (which is already correct)?

  - Is `RobGreen` showing up anywhere guest-facing or audit-facing where it would
  matter?


  **Handles**

  - Issue: https://linear.app/canary-technologies/issue/ENT-6141

  - User admin: https://www.canarytechnologies.com/canary-admin/auth/user/3473551/change/

  - Hotel admin: https://www.canarytechnologies.com/canary-admin/hotels/hotel/972/change/

  - Zendesk: https://canarysupport.zendesk.com/tickets/177159

  - Reserved branch: `glloyd/ent-6141-update-username-in-canary`


  **Did NOT do**

  - No staging/prod data touched (CLAUDE.md rule).

  - Did not post to Linear.

  - Did not investigate the SSO sync code path — flagged as a prerequisite for whoever
  fixes this.


  **Next action recommendation:** Ping the Wyndham/Enterprise pod for the username
  convention and SSO-sync key details, then either (a) rename `RobGreen` → Wyndham-convention
  username for Leo Saad in Django admin, or (b) reply to the requester clarifying
  that the display name is what matters and the internal username is harmless.

  '
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6141/update-username-in-canary
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6141: Wyndham GM username update (BW Days Inn Nanaimo)'
updated: 2026-05-07 13:49:56.912515
waiting_on: null
waiting_since: null
working_on: false
---

ENT triage, in Triage status. Username didn't update properly — shows 'Rob Green' instead of 'Leo Saad'. Created 2026-05-07.
https://linear.app/canary-technologies/issue/ENT-6141/update-username-in-canary