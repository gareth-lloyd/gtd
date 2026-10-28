---
area: null
completed_at: 2026-10-27 14:51:30.045062
contexts:
- react
created: 2026-10-27 05:36:42.460187
defer_until: null
due: 2026-10-27
energy: medium
id: 2026-10-27T0536-respond-on-tool-924-give-pov-on-syncing-gm-owner-d
order: null
output: |-
  ## Agent run 2026-10-27 08:33:05.938660

  Read TOOL-924 (https://linear.app/canary-technologies/issue/TOOL-924/sync-gm-and-owner-designations-between-canary-and-salesforce), Stephanie's ask (https://linear.app/canary-technologies/issue/TOOL-924/sync-gm-and-owner-designations-between-canary-and-salesforce#comment-30aca8f8), and the existing sync code. Nothing posted. Draft comment below; post it yourself or tell me to.

  ### Code facts that shape the answer
  - The designation is per hotel: `CompanyHotelUser.is_general_manager` / `is_owner` (backend/canary/hotels/models/company_hotel_user.py:38). Salesforce `Persona` is per person, so it can't hold a per-hotel fact.
  - `SalesforceContactService` (backend/canary/salesforce/services/salesforce_contact.py) only inserts. It only picks up users with no `SalesforceContact` row yet. A contact that already exists by email gets its timestamp bumped and nothing else, and nothing re-syncs on later changes. So "write when the designation changes" is a new change-driven path, not an extension of the current job.
  - It skips users with more than 10 hotels (`DO_NOT_SYNC_USERS_WITH_MORE_THAN_N_HOTELS`), and owner/management-company users are often exactly those. It also excludes the BW/Wyndham corporate roles.
  - It already creates AccountContactRelation rows (contact to hotel account) with a `Role`. That is the natural home for a per-hotel GM/Owner role, i.e. option D's shape, with no new object.
  - Possible bug I spotted, not verified: in `sync_contacts`, the secondary-relations branch does `extend(... for contact in contacts)` inside the per-contact loop. That queues relations for every contact on that account, including ones whose primary account it already is, so it may create duplicate or erroring relations. Worth a look before building on it.

  ### Draft Linear comment

  > Thanks for writing this up. My take:
  >
  > **1. Source of truth:** agree it should be Canary for who the GM/Owner is at a hotel, with Salesforce staying the truth for the ownership company. One caveat: Canary is only fresher than Salesforce where a feed maintains it (TOOL-922/923). For other hotels it's set once at onboarding and will go stale the same way, so we shouldn't promise freshness we don't have.
  >
  > **2. Direction:** A (Canary → Salesforce only), written onto the per-hotel link. I'd rather not do two-way. In Canary these flags will drive behaviour (TOOL-925 alerts, the event log), and I don't want CRM edits changing product behaviour. If Sales spots a difference, they should fix it in Canary. A Salesforce report on "contacts marked GM in SF but not by Canary" is enough of a review list; we don't need to build a queue (C).
  >
  > **3. How it's written:** the designation is per hotel in Canary, and Persona is per person, so I'd put it on the AccountContactRelation we already create between the contact and the hotel account (a GM / Owner role value on that link). That's D's shape, but one-way. It probably only needs picklist values rather than a new field, which Marketing DB should confirm. I'd skip writing Persona, and skip linking owners to the ownership-group account. Inferring that a person belongs to a company is a Salesforce judgement call, and putting the Owner role on the hotel link makes the 59%-with-no-ownership-group question go away.
  >
  > **4. Removal:** undo what Canary wrote, i.e. take the role off the link. Stale GMs are the problem we're solving, so a sync that only ever adds would recreate it. Removing a designation shouldn't deactivate the contact or the link itself, because the person may still work there.
  >
  > **Prereqs in the existing sync:** today it only inserts. It never updates an existing contact and only runs once per user. It also skips users with more than 10 hotels, who are often the owner/management-company contacts. So this needs a change-driven write path, not a tweak to the current job, and the more-than-10 cap needs revisiting for owners.

  ### Open points for you before posting
  - Do you want to say "skip Persona" that firmly? Sales may lean on Persona in their reports/list views, so Marketing DB may want it set too. A compromise is to set Persona=GM only when empty (their proposal) and never clear it.
  - Whether to mention the possible `sync_contacts` relations bug in the comment or check it first.

  ## Agent run 2026-10-27T14:30:00

  > is_owner, is_general_manager - where do these get set in canary? Are they edited internally or by end users? This will shape whether canary can be "source of truth"

  Answer: **end users set them.** Hotel admins tick them in the hotel-facing staff settings. There is no internal-only path and no automated feed yet. Code only, no prod data checked.

  ### Where they're written
  - Fields added 2026-10-05 in TOOL-761 (f4856e1feed, #58872). The UI shipped 2026-10-13 (db6d6282da7, #58963). That makes them about 3 weeks old, so almost every hotel will still be at the default of false.
  - The only writer is `HotelStaffUserService.set_property_designations` (backend/canary/hotel_staff/services/hotel_staff_user.py:620). It's called from the staff create and update APIs (hotel_staff/views/hotel_staff_users.py, hotel_staff/views/hotel_staff_user.py).
  - Those endpoints are gated by `Permission.PLATFORM_HAS_USER_MANAGEMENT_SETTING_ACCESS`, which is the hotel's own user-management permission, not a Canary-staff one.
  - The UI is GM and Owner checkboxes per property row in the hotel staff Add/Edit modal (frontend/adminland/src/hotelStaff/HotelStaffPropertyRolesTable.vue:385-411, used by AddEditHotelStaffUserModal and InviteExistingUserModal). The staff list also shows GM/Owner badges (HotelStaffTable.vue:431). I found no feature flag or staff-only gate. Canary CS can only set them by acting inside that same UI.
  - They're not in Django admin. No PMS, Salesforce or SSO feed writes them (TOOL-922/923 aren't built). A manual user merge ORs them together (sso/services/manual_user_merge.py:406).
  - Internal nudge: the onboarding go-live view shows `has_general_manager_or_owner` (onboarding/views/common.py:1026, TOOL-711) to warn when a hotel has neither. Onboarding/CS is pushed to get them set, but the hotel's own admins can change them at any time.
  - No audit trail: changes only emit `logger.info("set_property_designations")`, with no EventService event. There's no record of who changed a designation or what it was before.

  ### What this means for "source of truth"
  - **Good:** the people who know (hotel admins) maintain it in a product they use. That's a better owner than Sales updating Salesforce, and it's a reason Canary could be the truth.
  - **Caveats to put in the comment:**
    1. The data is new and sparse. Until onboarding backfills it (or 922/923 land), Canary says "no GM" for most hotels. Syncing *removal* from Canary would wipe Salesforce GM data that's correct today. Any first sync must be add-only, or must skip hotels where Canary has no designation yet.
    2. Nothing forces it to stay current. A GM who leaves usually just gets deactivated, and the flag isn't revisited. The sync should treat a deactivated or removed CHU as "designation ended", not only an unticked box.
    3. Any hotel admin can set it, and there's no audit. If it drives Salesforce (and TOOL-925 alerts), it should get an event log first, so we can answer "who said this person is the GM".
  - Net: Canary can be the source of truth for *who is GM/Owner at this hotel*, but only as hotel-asserted data that's patchy at first. One-way Canary→Salesforce still holds, but it should be add-only until coverage is real, and it needs audit logging as a prerequisite.

  ### Suggested addition to the draft comment
  > On source of truth: these flags are set by the hotel's own admins in staff settings (shipped mid-October in TOOL-761). Hotel admins are the right people to own the data, but it's brand new, so almost every hotel is unset today. I'd make the first version of the sync add-only, so we don't wipe correct Salesforce GMs with Canary blanks. We'd add removal once onboarding is filling it in reliably. We should also add audit logging on designation changes before Salesforce depends on them, since today there's no record of who set them.

  Not done: no prod count of how many hotels have a GM/Owner set. A read-only `canary prod-db query` would get it if you want the number for the comment.
project: 2026-04-16T1210-unblock-team
source_id: https://linear.app/canary-technologies/issue/TOOL-924/sync-gm-and-owner-designations-between-canary-and-salesforce#comment-30aca8f8
tags:
- morning-gtd
- linear
time_minutes: 20
title: 'Respond on TOOL-924: give POV on syncing GM/Owner designations with Salesforce'
updated: 2026-10-27 14:51:30.045055
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie Barry: "@glloyd would love your POV on this". Ticket is Blocked, priority 3.
https://linear.app/canary-technologies/issue/TOOL-924/sync-gm-and-owner-designations-between-canary-and-salesforce