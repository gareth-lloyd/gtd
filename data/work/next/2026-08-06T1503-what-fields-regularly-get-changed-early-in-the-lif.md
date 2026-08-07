---
area: null
completed_at: null
contexts: []
created: 2026-08-06 15:03:33.888408
defer_until: null
due: null
energy: low
id: 2026-08-06T1503-what-fields-regularly-get-changed-early-in-the-lif
order: 2
output: |
  ## Agent run 2026-08-06T12:23Z — PLAN (awaiting approval, no analysis run yet)

  Feasibility is proven end-to-end: I found the right tables, validated the staff join,
  and ran a working prototype of the core query. Below is what exists, what the traps are,
  the test queries that already returned real data, and the five decisions I need from you.

  ### Data sources (validated, US region)

  | What | Table | Notes |
  |---|---|---|
  | Events | `ANALYTICS_PUBLIC.FACT_EVENTS` | 11.5B rows. `EVENT_NAME`, `PAYLOAD` (TEXT json), `HOTEL_ID`, `ACTOR_UUID`, `IMPERSONATOR_UUID`, `OBJECT_CLASS`, `CREATED_AT` (TIMESTAMP_NTZ). Prunes well on `CREATED_AT` — queries return in seconds. |
  | Hotels | `ANALYTICS_PUBLIC.DIM_HOTEL` | 23,570 rows, has `CREATED_AT`, `IS_DEMO`, `IS_LIVE`, `BRAND_ID`. |
  | Staff | `ANALYTICS.HOTELS_USERPROFILE_MERGED` -> `ANALYTICS.AUTH_USER_MERGED` | join `up.USER_ID = u.ID`, filter `u.IS_STAFF`. **365 staff users**. `Event.actor_uuid` is `UserProfile.uuid`, confirmed at `backend/canary/event/services/event.py:904`. |
  | Hotel field history (fallback) | `CANARY_RAW.SNAPSHOT.HOTELS_HOTEL_SNAPSHOT` | dbt SCD2, back to 2025-01-11, 25.7M versions / 23,580 hotels. Independent of the event log. |

  Do NOT use `EVENTS_RAW.SNAPSHOT.EVENT_EVENT_SNAPSHOT_DEDUPED` (26B rows) — an unpruned
  aggregate over it hit the 120s statement timeout. `FACT_EVENTS` is the same data, modelled.

  ### The settings-change events exist and carry field-level diffs

  `ChangeTracker` (`backend/canary/canary/change_tracker.py`, added 2026-03-04 in commit 409ca872777,
  "[CA-38] Record product activation changes" #37079) emits `<app>.<Model>__product_state_changed`
  and `<app>.<Model>__config_changed` with payload:

      {"field": "hotels_timezone", "source": "enterprise_onboarding",
       "old_value": null, "new_value": "America/New_York"}

  `source` is one of `django_admin | enterprise_onboarding | onboarding | shell | api |
  management_command | other` — so we can separate scripted setup from a human in Django admin
  or Adminland.

  **Hard date floors (measured, not assumed).** This is the biggest constraint on the analysis:

  | Event | First seen |
  |---|---|
  | `hotels.Hotel__product_state_changed` | 2026-03-04 |
  | `authorization/tips/chat/addons/voice/check_in/check_out/payment_links ...__product_state_changed` | 2026-03-09 .. 2026-03-13 |
  | `hotels.Hotel__config_changed` | 2026-05-28 |
  | `authorization.AuthorizationConfiguration__config_changed` | 2026-06-17 |
  | `chat / addons / tips / check_in / check_out / voice ...__config_changed` | 2026-06-18 .. 2026-06-23 |

  So field-level *settings* analysis only covers hotels created since ~2026-06-23 (~250 non-demo
  hotels), while product on/off analysis covers hotels created since ~2026-03-13 (~1,300 non-demo).

  ### Test queries already run (real output)

  **T1 — event coverage / date floors.** `FACT_EVENTS` grouped by `EVENT_NAME` for
  `%__config_changed` / `%__product_state_changed` since 2026-01-01. 17 event names,
  `hotels.Hotel__config_changed` biggest at 38,462. Returned in seconds. -> produced the table above.

  **T2 — core prototype: which fields staff change in a hotel's first 7 days.**
  Cohort = non-demo hotels created 2026-06-20..2026-07-20 (205 hotels with any staff event).
  Top rows (field, source, changes, hotels):

      after_checkin_background_image / supported_languages / id_checking_rules /
        right_hero / logo_with_name / amount_verification_rules / image_primary /
        blocked_card_types / image_secondary / blocked_credit_card_networks /
        top_hero / wallet_logo / image_tertiary   [onboarding]   263 each, 179 hotels
      auth_link_email_body_template / contract_link_email_subject_template /
        contract_link_email_body_template / auth_link_email_subject_template /
        amenity_delivery_fee_message                [django_admin] 196 each, 196 hotels
      state, zipcode                                [onboarding]   180, 179 hotels
      hotels_timezone, room_count, city, address1, country, country_code, phone, logo,
        rollout_hide_property_staff_default_role    [onboarding]   179, 179 hotels
      authorization.AuthorizationConfiguration.id_verification_provider [onboarding] 179, 179
      image_primary                                 [api]          174, 171 hotels
      is_demo                                       [django_admin] 147, 147 hotels
      logo                                          [api]          140, 126 hotels
      hotels.Hotel.has_tipping                      [onboarding]   139, 139 hotels
      tips.Configuration.can_be_tipped              [onboarding]   136, 136 hotels
      tips.Configuration.fee_payer                  [api]          131, 127 hotels
      brand                                         [onboarding]   111, 111 hotels
      sms_phone                                     [django_admin]  43,  40 hotels
      gateway_account_needs_sync                    [django_admin]  48,  33 hotels
      check_in.Configuration.rollout_check_in_v2_level [enterprise_onboarding] 42, 21 hotels

  **T3 — full action taxonomy (all event names, staff actor, first 7 days, same cohort).**
  80+ distinct event names. Ranked:

      hotels.Hotel__config_changed                        8678  (205 hotels)
      HOTEL_STAFF_USER.HotelStaffUser__view_hotel         2083  (200)
      guest_journey.GuestJourneyMessage__sms_enabled       801  (185)
      guest_journey.GuestJourneyMessage__disabled/created/whatsapp_disabled  487 each (185)
      hotels.Hotel__product_state_changed                  432  (205)
      check_in.Configuration__config_changed               380  (30)
      guest_journey.GuestJourneyMessage__email_enabled     380  (57)
      authorization.AuthorizationConfiguration__config_changed 330 (188)
      tips.Configuration__product_state_changed            151  (143)
      addons.Configuration__config_changed                  95  (27)
      property_info.Entity__created / compendium.Item__created  90 / 88  (7)
      permissions.PropertyRoleGrant__created                80  (48)
      HOTEL_STAFF_USER.HotelStaffUser__assigned/created     73 / 52
      addons.Room__created/updated, addons.RoomUpgrade__created  ~36 each (3)
      check_in.RegistrationCard__updated                     9  (4)

  So the associated-objects angle is real and rich: guest journey messages, property info /
  compendium, addons rooms & upgrades, staff user provisioning, permission role grants.

  ### Traps found (all confirmed, all need handling)

  1. **No-op changes are logged.** Payloads like `{"field": "after_checkin_background_image",
     "old_value": null, "new_value": null}` and `{"field": "blocked_card_types",
     "old_value": [], "new_value": null}` are recorded as changes. The uniform "263 changes /
     179 hotels" block in T2 is largely this. Must filter `old_value IS DISTINCT FROM new_value`
     after normalising `null` / `[]` / `""`, or the top of the ranking is an artefact.
  2. **Most volume is scripted, not human.** `source` = `onboarding` / `enterprise_onboarding`
     dominates and is really "hotel creation finishing", not "a change early in the hotel's life".
     `django_admin` and `api` are the human signal. Recommend segmenting, not dropping — "what
     does the onboarding script set" is itself an answer to your question.
  3. **Registration Card events carry empty payloads.** `check_in.RegistrationCard__updated`
     and `__policy_updated` both have `PAYLOAD = '{}'`. We can count *that* reg cards were
     touched, never *what* changed. There is no `CHECK_IN_REGISTRATIONCARD` dbt snapshot either,
     so field-level reg-card analysis is not possible from Snowflake today.
  4. **`IMPERSONATOR_UUID` is never populated** — 0 non-null rows across all of July 2026. If
     staff act through impersonation, those events are attributed to the hotel user and we will
     under-count staff activity. Unknown magnitude; worth a separate check.
  5. **`is_staff` is current state, not as-of-event.** Someone who left Canary and had the flag
     cleared drops out of the cohort retroactively. 365 staff today.
  6. **Demo hotels distort everything.** e.g. 25 Marriott demo hotels bulk-created 2026-08-01
     generate thousands of config events in minutes. `DIM_HOTEL.IS_DEMO` filters them.

  ### Proposed phases

  - **P1 — Action taxonomy.** T3 generalised: what staff do in the first 7 days, by event name /
    object class, plus a time-since-creation histogram (0-1h / 1-24h / 1-3d / 3-7d) to separate
    the creation burst from genuine follow-up.
  - **P2 — Settings deep dive.** T2 with the no-op filter, split by `source`, ranked by
    *hotels affected* not raw count, plus the common old->new value transitions for the top
    fields, and a "changed more than once in the first week" list (churn = ambiguous defaults).
  - **P3 — Associated objects.** Guest journey messages, property info / compendium, addons,
    permission grants, staff user provisioning; reg cards as counts only (trap 3).
  - **P4 — Optional, only if you want pre-June coverage.** Diff `HOTELS_HOTEL_SNAPSHOT` SCD2
    versions for the cohort to recover field changes back to 2025-01-11 and cover fields outside
    `CONFIG_FIELDS`/`PRODUCT_FIELDS`. Slower and it loses actor/source attribution — the snapshot
    knows *what* changed but not *who* changed it. Would answer "what fields change early" but
    not "by Canary staff".

  ### Decisions I need from you

  1. **Cohort window.** Recommend running two: settings-level over 2026-06-23..2026-07-30
     (~250 non-demo hotels, full `config_changed` coverage) and product-state over
     2026-03-13..2026-07-30 (~1,300 non-demo hotels). Or pick one.
  2. **Demo hotels** — exclude (recommended) or report as a separate segment?
  3. **Scripted sources** — segment `onboarding`/`enterprise_onboarding` separately from
     `django_admin`/`api` (recommended), or exclude scripted entirely?
  4. **Staff definition** — `is_staff` as-is (recommended, matches your ask), or cross-check
     against `@canarytechnologies.com` email to catch flag drift?
  5. **Output** — markdown tables in this file, or an Artifact dashboard with the rankings and
     the time-since-creation histogram?

  Also: do you want P4 (the pre-June snapshot diff)? It roughly doubles the work and loses
  the "by Canary staff" dimension, so I'd default to skipping it unless the March/June date
  floor is a dealbreaker.

  No writes were made to any external system. All queries were read-only SELECTs.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: What fields regularly get changed early in the life of a hotel - event analysis?
updated: 2026-08-06 15:23:11.121058
waiting_on: null
waiting_since: null
working_on: false
---

Snowflake
Up to 1 week after creation of hotel, find Events logging changes by Canary staff (User.is_staff) users. 
What actions are being taken?
In particular, what settings get changed?
If the analysis can extend to associated objects e.g. Registration Cards, all the better. 

Plan first, including test queries, then present for my approval.