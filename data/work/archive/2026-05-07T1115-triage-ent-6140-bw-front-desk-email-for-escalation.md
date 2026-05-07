---
area: null
contexts:
- react
created: 2026-05-07 11:15:35.018346
defer_until: null
due: null
energy: medium
id: 2026-05-07T1115-triage-ent-6140-bw-front-desk-email-for-escalation
order: null
output: "## Agent run 2026-05-07T11:30Z\n\n### Ticket recap\n- ENT-6140 (Triage, Medium,
  Enterprise team, no assignee, no comments).\n- Reporter: Tracy Drakeley (CSM). Customer:
  BW property 03162 (\"Snowflake Inn\").\n- Ask 1 (tactical): add `bw.snowflakeinn@gmail.com`
  directly into unanswered-messages\n  escalation recipients without making it a Canary
  user.\n- Ask 2 (strategic): treat as a feature request — \"common ask\" for hotels
  who don't\n  want individual MemberWeb emails getting escalation texts.\n\n### Why
  the tactical ask is not currently possible\n- `chat.MessageEscalation.staff` is
  `ManyToManyField(User)` — recipients are strict\n  User FKs (`backend/canary/chat/models/message_escalation.py:31`).\n-
  Frontend (`frontend/adminland/src/chat/escalations/ChatMessageEscalationsCard.vue`)\n
  \ sources recipients from `getUsers()`; no UI affordance for raw emails/numbers.\n-
  No \"non-user notification recipient\" concept exists in the model today.\n\n###
  Recurrence signal — this is real and there's adjacent work in flight\n- **ENT-6111**
  (High, \"Remove Above Property users from Unanswered Messages\",\n  Connor Swords
  → Andrés Figueira, Todo, created 2 days before this ticket).\n  Same UI/file. Notes
  BW corporate is blocking BWH adoption of this feature\n  because corporate users
  appear in the recipient list. Spec is to filter the\n  user list via `useHotelStaffUsersWithPermissionsQuery`
  with\n  `include_above_property_users=false`.\n- **ENT-5362** (related to ENT-6111)
  was the same kind of fix in another modal.\n- **ONC-17137** (Cancelled, Oct 2025):
  Tracy asked us to bulk-rewrite front-desk\n  users' personal emails to a single
  hotel front-desk email — same underlying\n  customer pain. Cancelled with no public
  comments visible.\n- No existing ticket specifically for \"non-user escalation recipients\"
  — that\n  would be net-new.\n\n### Recommendation (does not require my code change)\n1.
  **Unblock BW-03162 immediately via CSM workaround.** Tell Tracy that today's\n   supported
  pattern is: create a dummy User on hotel 03162 with email\n   `bw.snowflakeinn@gmail.com`,
  add to the escalation, and restrict the user\n   (no SSO / no login) so it functions
  purely as a notification target. This\n   does not need engineering. Worth confirming
  with Connor / Messaging that\n   they're OK endorsing this workaround officially
  (it's what most CSMs already\n   do).\n2. **File a Messaging-team feature request**
  to support arbitrary email/SMS\n   recipients on `MessageEscalation` without requiring
  a User. This is the\n   correct long-term fix — `MessageEscalation` model + migration
  change plus\n   recipient selector UI. Owner is Messaging (matiasmdp / kli area),
  not\n   Enterprise eng. Cross-link ENT-6140, ENT-6111, ENT-5362, ONC-17137 as\n
  \  supporting customer signal.\n3. **Don't take this as Enterprise eng work** —
  Enterprise's adjacent ticket\n   (ENT-6111) is purely a UI-filter fix and is already
  with Andrés. ENT-6140\n   should either close as \"use workaround\" once Tracy confirms,
  or convert to\n   an MSG-team feature request.\n\n### Open questions for the user\n-
  Want me to draft a comment for Tracy on ENT-6140 outlining the workaround?\n  (Will
  not post without explicit approval.)\n- Want me to draft an MSG-team feature-request
  ticket linking the recurrence\n  signal? (Will not create without explicit approval.)\n\n###
  Status I'd suggest (not actioned)\n- Move ticket out of Triage, label \"Feature
  request\", reassign to Messaging\n  team — or leave with Enterprise pending Tracy's
  reply about the workaround.\n- I have NOT made any Linear changes.\n"
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-6140/adding-front-desk-email-to-escalation-text
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Triage ENT-6140: BW front desk email for escalation text'
updated: 2026-05-07 13:46:01.347737
waiting_on: null
waiting_since: null
working_on: false
---

ENT triage. BW-03162 wants front-desk email added without making it a user. Common ask, possibly feature request.
https://linear.app/canary-technologies/issue/ENT-6140/adding-front-desk-email-to-escalation-text