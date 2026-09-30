---
area: null
completed_at: 2026-09-30 13:49:29.417640
contexts:
- react
created: 2026-09-30 04:36:29.886966
defer_until: null
due: null
energy: medium
id: 2026-09-30T0436-follow-up-on-bw-staff-app-push-notifications
order: null
output: |
  ## Agent run 2026-09-30T14:10 (Europe/Athens)

  **TL;DR: this is almost certainly not an SSO bug. Staff-app push is gated on a per-hotel flag (`Hotel.enable_push_notifications`) that is OFF for every Best Western hotel, and every hotel Jason Pitard is a member of. Only 3 US hotels have it on, all Canary test/demo hotels, which is why Connor sees pushes in TestFlight and BW never has. The thread and STAFF-258 are chasing SSO; suggest redirecting Diana before she ships a "quick fix" for the wrong thing.**

  ### Thread status
  - Slack thread: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790702092262039?thread_ts=1790702092.262039&cid=C0AN8AQ49UG
  - Connor (2026-09-29): BW (Jason, Caleb) have NEVER received pushes. Big sticking point for BWH; convention is Oct 26.
  - Caitlyn: Mobile team push-reliability project tracking Oct 16, Diana leading.
  - Diana: "push works but is flaky"; Sofya flagged SSO; Diana said she will add a quick fix for SSO so we can showcase. Opened STAFF-258 (https://linear.app/canary-technologies/issue/STAFF-258/review-flaky-push-notifications-for-sso-users), Triage, assigned to Diana, related to MOB-1276 (Gravity Haus Westport, same symptom, Todo).
  - Ron Stenger (2026-09-30 05:47): Jason + 2 more SSO coworkers, none get pushes; "SSO is a potential factor".
  - Nobody has replied since Ron. No PR yet from Diana for STAFF-258.

  ### What the code actually does (backend/canary)
  - Inbound guest message -> `MessageReceiver._enqueue_staff_chat_push` -> `send_staff_chat_message_push_to_hotel` (push_notifications/tasks/send_staff_push.py). First check: `if not hotel.enable_push_notifications: return`. The per-user task and `PushNotificationService.send_to_staff_user` re-check the same flag. The generic notifications path (`NotificationDispatchService`, notification_dispatch.py:203) also returns PUSH_DEFERRED_DISABLED on that flag.
  - Recipient selection is `PermissionService.get_all_users_with_permissions_for_hotel(MESSAGES_HAS_PRODUCT_ACCESS)`, which does include SSO-mapped PropertyRoleGrants and portfolio-wide grants, intersected with StaffSubscription (device registrations). Nothing SSO-specific short-circuits it.
  - The flag is `Hotel.enable_push_notifications`, default False, help text still says "for the hotel's mobile SDK guests". It is only settable in Django admin, under "Release and rollout flags" (hotels/admin/hotel.py:981). Not in Adminland.
  - Staff app (staff-app-react-native): `PushRegistrationSync` in `src/app/(app)/_layout.tsx` registers the device on every signed-in session regardless of login method; the SSO path only differs at login. No SSO-conditional in the push code.

  ### Prod data (Snowflake CANARY_RAW mirror, US, read-only, 2026-09-30)
  - Hotels with `enable_push_notifications = true` in US: exactly 3: `canary-test-hotel` (id 1), `demo-hotel-canary-staff-app-hotel-9bf3t` (129297974), `customer-test-hotel` (129299690). No BW hotel.
  - Jason Pitard has 3 users: `bwjasonpitard` (id 3747696, Jason.Pitard@bestwestern.com, SSO role "BW Corporate" role 22335 on 919 hotels, 988 CompanyHotelUser rows, last login 2026-09-29 23:25 UTC), `jasondemo` (3742064, Jason.Pitard@bwh.com, hotels best-western-demo 129234652 + jonas-chorum-test-hotel), `jason pitard` (3727261, staging-bw-00821 + hotelkey-test-2). Zero of those hotels have the flag on.
  - Could not find a Caleb user with a @bestwestern.com email in the mirror (search by name/username). Could not verify StaffSubscription rows or PermissionGrant rows for role 22335: neither table is mirrored to Snowflake. Worth a quick shell-plus read on prod if someone wants belt-and-braces.
  - Not checked: whether the "BW Corporate" SSO role actually carries MESSAGES_HAS_PRODUCT_ACCESS. If it does not, that is a second blocker for the SSO users specifically, but the flag blocks everyone first.

  ### Recommended next steps
  1. Reply in the thread (draft below) pointing at the hotel flag. Ask which hotel(s) BW will use for the convention demo (likely `best-western-demo` 129234652, Jason's jasondemo user) and have someone with Django admin flip `enable_push_notifications` on those. That should make pushes work for password and SSO users alike within minutes, no code change.
  2. Ask Diana to reframe STAFF-258: first confirm on a flag-enabled hotel whether SSO users still miss pushes. If they do, then check the "BW Corporate" role's permissions and the StaffSubscription rows for user 3747696.
  3. Product question for Caitlyn/Mike: the flag is a per-hotel admin toggle with guest-SDK help text. If staff-app push is meant to be on for every staff-app customer, it needs a rollout plan (bulk-enable for staff-app hotels, or drop the gate for staff pushes). MOB-1276 (Gravity Haus) is probably the same flag.

  ### Draft Slack reply (NOT sent; needs your OK)
  > I dug into this. I don't think SSO is the cause. Staff-app push is gated on a per-hotel Django-admin flag, `Hotel.enable_push_notifications` (it still has the old "mobile SDK guests" help text). In prod US it's on for exactly 3 hotels: canary-test-hotel, Canary Staff App Hotel, and customer-test-hotel. None of the BW hotels have it, including best-western-demo and the ~900 hotels Jason's SSO user is attached to. So nobody at BW has ever been eligible for a push, SSO or not. That also matches Connor getting them in TestFlight on our test hotels.
  > Suggest: tell us which hotel(s) BW will demo on at the convention, flip the flag there (Django admin > Hotel > "Release and rollout flags"), and re-test. If SSO users still miss pushes on a flag-enabled hotel, then STAFF-258 has something to chase. Also worth deciding whether this should just be on for every staff-app hotel (MOB-1276 / Gravity Haus is likely the same thing).

  ### Nothing written externally
  No Slack, Linear, or Notion writes. No Salesforce access. Temp clone of staff-app-react-native removed.

  ## Agent run 2026-09-30T14:40 (Europe/Athens): re-verification of the flag gate

  User asked to double-check that `enable_push_notifications` truly gates BW staff pushes. It does. Checked:
  - Full path from inbound guest message: `MessageReceiver._enqueue_staff_chat_push` (chat/services/message_receiver.py:184) returns before enqueueing unless `message.thread.hotel.enable_push_notifications` is true. The fan-out task and `PushNotificationService.send_to_staff_user` re-check the same field. Pinned by tests: test_message_receiver.py:745 ("enable_push_notifications defaults False" -> `staff_push_mock.delay.assert_not_called()`) and test_send_staff_push.py:78.
  - Every producer of a staff push in backend/canary goes through one of two entry points, both gated: the chat fan-out above, and `NotificationDispatchService` (notifications/services/notification_dispatch.py:203, returns PUSH_DEFERRED_DISABLED). The private `POST /api/private/v1/messaging/notifications` endpoint (ID-78) routes into that same dispatch service; identity-service only uses it for MFA SMS anyway. No other module imports APNsService/FcmService or `_send_to_devices`. The tips and kiosk "staff notification" hits are SMS/WhatsApp, not push.
  - No feature flag, GrowthBook, or settings override reads that field. It is only written from Django admin ("Release and rollout flags" fieldset) and the demo-hotel service.
  - Snowflake mirror freshness: latest CDC row 2026-09-30 10:28Z, extracted 10:31Z (about 40 min lag at query time). Re-ran the flag query keyed on hotels that have EVER had a true row: only the same 3 hotels (canary-test-hotel since 2026-05-21, demo-hotel-canary-staff-app-hotel-9bf3t since 2026-08-28, customer-test-hotel since 2026-09-16). No BW hotel has ever had the flag on in the mirror's history.

  Still unverified (not mirrored): StaffSubscription rows for Jason's users, and whether the "BW Corporate" role carries MESSAGES_HAS_PRODUCT_ACCESS. Neither changes the conclusion: the flag short-circuits before either is consulted.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790702092262039?thread_ts=1790702092.262039&cid=C0AN8AQ49UG
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Follow up on BW staff app push notifications
updated: 2026-09-30 13:51:18.891484
waiting_on: null
waiting_since: null
working_on: false
---

Connor in #epd-staff-app: Best Western (Jason and Caleb) report push notifications are not working for new messages in the staff app; 16 replies.
https://canarytechnologies.slack.com/archives/C0AN8AQ49UG/p1790702092262039?thread_ts=1790702092.262039&cid=C0AN8AQ49UG