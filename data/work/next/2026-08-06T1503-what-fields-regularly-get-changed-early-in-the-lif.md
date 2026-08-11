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

  ## Agent run 2026-08-07T12:51Z — FIRST PASS RESULTS

  Parameters you set: cohort = since ChangeTracker; exclude demo hotels (current `IS_DEMO`);
  segment scripted; **exclude onboarding-script changes, human only**.

  ### Cohort and denominators

  1,213 non-demo hotels created 2026-03-04 .. 2026-07-30 (Mar 225, Apr 267, May 313, Jun 176,
  Jul 232). Each hotel's window is its own `CREATED_AT` + 7 days.

  Because the event types went live at different dates, each metric has its own denominator:

  | Metric family | Live from | Eligible hotels |
  |---|---|---|
  | `__product_state_changed` (product on/off) | 2026-03-13 | 1,134 |
  | `hotels.Hotel__config_changed` | 2026-05-28 | 456 |
  | per-product `__config_changed` (tips, chat, auth, check_in ...) | 2026-06-23 | 295 |

  ### Scripted vs human split (this is the headline)

  Staff-actor settings events in the first 7 days, by `payload.source`:

  | source | events | hotels | staff actors |
  |---|---|---|---|
  | onboarding | 9,872 | 914 | 25 |
  | enterprise_onboarding | 6,948 | 323 | 24 |
  | **django_admin** | **2,465** | **464** | **46** |
  | **api** (Adminland UI) | **818** | **253** | **29** |
  | shell | 4 | 1 | 1 |
  | management_command | 1 | 1 | 1 |

  **83% of early-life settings churn is the onboarding tooling, not a person.** Everything below
  is the remaining 17% (django_admin + api + shell + management_command), with no-op events
  filtered out (`old_value` normalised against `new_value`, treating `null`/`[]`/`""`/`{}` as equal).

  Note: `IS_SERVICE_USER` is false for every one of these actors — the onboarding tool runs under
  real staff identities, so `payload.source` is the *only* way to separate scripted from human.
  That matters below.

  ### What humans actually change, first 7 days

  Ranked by share of eligible hotels. `hrs` = median hours after hotel creation.

  | Field | Model | Hotels | % of eligible | hrs | Dominant transition |
  |---|---|---|---|---|---|
  | `fee_payer` | tips.Configuration | 175 | 59% | 0 | staff -> guest (175 hotels; reverse only 3) |
  | `image_primary` | Hotel | 235 | 52% | 0 | — |
  | `is_demo` | Hotel | 205 | 45% | 0 | true -> false (204) |
  | `logo` | Hotel | 172 | 38% | 0 | — |
  | `phone` | Hotel | 124 | 27% | 0 | — |
  | `can_be_tipped` | tips.Configuration | 59 | 20% | 0 | true -> false (53); false -> true (9) |
  | `has_ai` | chat.Configuration | 54 | 18% | 0 | false -> true (53) |
  | `sms_phone` | Hotel | 69 | 15% | **51** | — |
  | `authorization_tier` | AuthorizationConfiguration | 38 | 13% | 0 | no_restrictions -> auth_only (38) |
  | `gateway_account_needs_sync` | Hotel | 47 | 10% | **66.5** | false -> true (47) |
  | `has_check_in_messages` | Hotel | 46 | 4% | 0 | false -> true (45) |
  | `has_check_in` | Hotel | 35 | 3% | 0 | false -> true (34) |
  | `has_voice` | Hotel | 32 | 3% | 0 | false -> true (32) |
  | `has_authorizations` | Hotel | 25 | 2% | 0 | false -> true (19); true -> false (6) |
  | `has_tipping` | Hotel | 24 | 2% | 1 | true -> false (17); false -> true (9) |
  | `blocked_card_types` | Hotel | 13 | 3% | **81** | [] -> ["prepaid"] (12) |
  | `has_pms_sync` | Hotel | 10 | 2% | **82** | false -> true (10) |

  114 distinct fields in total; full ranking is reproducible from the query below.

  ### Two distinct behaviours, visible in the timing

  | Window | Changes | Hotels |
  |---|---|---|
  | under 1h | 1,180 (61%) | 348 |
  | 1h - 24h | 300 | 70 |
  | 1d - 3d | 158 | 57 |
  | 3d - 7d | 292 | 91 |

  **(a) Setup finishing (median 0h)** — branding (`image_primary`, `logo`), `is_demo` flip,
  `phone`, product toggles, tips `fee_payer`. This is a human completing creation, arguably
  part of provisioning rather than "change".

  **(b) A genuine second visit, 2-5 days later.** These are the fields nobody can know at
  creation time, and they cluster hard:
  - *Telephony / messaging*: `sms_phone` 51h, `has_fallback_to_sms` 93h, `allow_send_whatsapp`
    93h, `whatsapp_phone_number` 95.5h, `twilio_whatsapp_sender_status` 96h
  - *PMS integration*: `has_pms_sync` 82h, `pms` 85h, `pms_payment_slot_identifier_auths` 102.5h,
    check_in `integration_auto_post_to_pms*` (7 fields) 111h, `is_tokenizing_with_hotel_payment_gateway` 115.5h
  - *Payments / gateway*: `gateway_account_needs_sync` 66.5h, `blocked_card_types` 81h,
    `has_advanced_payments` 91h
  - *SSO*: `sso_hotel_id` 84.5h, `sso_organization` 24h

  ### Associated objects (staff actor, first 7 days, full 1,213 cohort)

  Non-settings events carry no `source`, so these counts **include onboarding-tool activity** —
  they cannot be filtered to human-only. Read as "what gets touched", not "what a human clicked".

  | Area | Signal | Hotels |
  |---|---|---|
  | Hotel viewed by staff | `HotelStaffUser__view_hotel` 12,799 events | 1,116 (92%) |
  | **Guest Journey messages** | `sms_enabled` 4,925 / `created` 2,871 / `disabled` 3,407 | 656 (54%) |
  | GJ template editing | `sms_template__edited` 598 / `email_template__edited` 491 | 254 / 214 |
  | Permission grants | `PropertyRoleGrant__created` 625; `Role__created` 60 | 332 / 48 |
  | Staff user provisioning | `HotelStaffUser__assigned` 578 / `__created` 335 | 308 / 207 |
  | Property info / compendium | `Entity__updated` 379, `Entity__created` 302, `Item__created` 286 | only 23-28 hotels |
  | Addons | `Room__updated` 83, `Room__created` 65, `RoomUpgrade__created` 65, `MenuItem__added` 158 | only 4-7 hotels |
  | **Registration Cards** | `RegistrationCard__updated` 49 events | 32 (2.6%) |
  | First real usage | `Reservation__created` 106 / `CheckIn__created` 98 / `Authorization__created` 81 | 70 / 61 / 57 |

  Guest Journey message configuration is the single biggest non-settings workload — bigger than
  everything else combined, and touching over half the cohort. Property info / compendium and
  addons are the opposite shape: very few hotels, but hundreds of events each when they happen.

  Registration Cards: confirmed at 32 hotels but the payloads are `{}`, so there is still no
  field-level detail available. This remains the one part of your ask Snowflake cannot answer.

  ### Caveats on this pass

  1. `hotels.Hotel__config_changed` only covers hotels created since 2026-05-28 (456 of 1,213),
     and per-product configs since 2026-06-23 (295). Product toggles cover 1,134. Percentages
     above use the correct per-family denominator, but the config rows rest on a smaller base.
  2. Non-settings events cannot be split human vs scripted (no `source` on the payload).
  3. `IMPERSONATOR_UUID` is null everywhere — impersonated staff work is invisible and would be
     attributed to the hotel user.
  4. `is_staff` is read at current state, not as-of-event.
  5. "Exclude demo" uses current `IS_DEMO`. Since `is_demo: true -> false` is itself the 3rd most
     common human change (204 hotels), a large part of this cohort *was* demo during the window
     being measured. Worth being explicit about — the filter is "is a real hotel today", as you
     specified, not "was never a demo".

  ### Reproducing

  All queries are `sf_query` (region `us`), read-only. The core shape is:
  staff = `HOTELS_USERPROFILE_MERGED` join `AUTH_USER_MERGED` on `USER_ID = ID` where `IS_STAFF`;
  cohort = `DIM_HOTEL` where `CREATED_AT` in range and not `IS_DEMO`;
  events = `ANALYTICS_PUBLIC.FACT_EVENTS` joined on `HOTEL_ID` with
  `CREATED_AT` between `hotel_created_at` and +7 days, plus a literal `CREATED_AT >= '2026-03-04'`
  predicate so Snowflake prunes micro-partitions (without it the query does not return);
  human filter = `TRY_PARSE_JSON(PAYLOAD):source NOT IN ('onboarding','enterprise_onboarding')`;
  no-op filter = normalise `TO_JSON(old_value)`/`TO_JSON(new_value)` with
  `NULLIF(...,'null')`/`'[]'`/`'""'`/`'{}'` then `IS DISTINCT FROM`.

  ### Suggested next cuts (not run)

  - Split the ranking by brand / enterprise vs SMB — the `enterprise_onboarding` source touches
    323 hotels and likely has a different human-fix profile.
  - Correlate the "second visit" fields against time-to-go-live (`GO_LIVE_DATE_AUTHS`) to test
    whether telephony/PMS fixes are on the critical path.
  - Check whether the 61%-under-1h human edits are the same staff member who ran the onboarding
    tool (i.e. a tooling gap) or a different person (i.e. a handoff gap).

  ## Agent run 2026-08-07T12:59Z — CORRECTION to the impersonation caveat

  Followed up on "are we systematically failing to set impersonator UUID on events?". Answer:
  the column is dead, but **the caveat I drew from it was wrong and the first-pass numbers are
  unaffected**. Correcting caveat #4 in both sections above.

  ### `Event.impersonator_uuid` has never been written

  Added in `backend/canary/event/migrations/0008_auto_20230726_1840.py` (July 2023) and never
  wired up. Both write paths build the row without it:

  - `backend/canary/event/services/event.py:157` — `create_from_dispatched_event`
  - `backend/canary/event/services/event.py:215` — the bulk-create path

  A grep across all of `backend/` finds no assignment of `impersonator_uuid` on an `Event`
  anywhere. The only writes to a field of that name are in
  `backend/canary/api_gateway/views/private/validate.py:155`, an unrelated auth-validate
  response payload. So 0% populated is not partial instrumentation or a regression — the column
  has never been used since the day it was added.

  ### Impersonated staff activity is NOT missing from the analysis

  Impersonation is captured by two other mechanisms:

  1. **`actor_uuid` holds the impersonator, not the impersonated user.**
     `EventService._impersonation_event_actor_from_eventable_model`
     (`backend/canary/event/services/event.py:463`) returns
     `EventActor(actor_uuid=impersonator.userprofile.uuid, impersonated_actor=EventActor(...))`.
     `ChangeTracker._post_save` (`backend/canary/canary/change_tracker.py`) reinforces this:
     `impersonator = get_current_impersonator(); user = impersonator or get_current_user()`.
  2. **The impersonated user is written as an `EventRelatedObject`** with
     `relation='impersonated_actor'` (`backend/canary/event/services/event.py:312-328`).

  So when Canary staff impersonate a hotel user and change a setting, the event is attributed to
  the staff member. The first-pass figures already include that work — they do not under-count it.

  **The real limitation is different:** we cannot *distinguish* impersonated from direct staff
  actions in Snowflake, because `event_eventrelatedobject` is not replicated at all. Checked
  `CANARY_RAW`, `ANALYTICS` and `EVENTS_RAW` — no such table in any of them. That is a
  replication gap, not an instrumentation gap.

  ### Incidental bug found in the same code: the no-op change events

  `ChangeTracker._post_save` compares **raw** field values:

      if old_val == new_val:
          continue

  but writes the **`_json_safe(...)` projection** into the payload. Value pairs that differ
  raw-side yet collapse to the same JSON still emit an event — `FieldFile(name='')` vs
  `FieldFile(name=None)` both serialise to `null`; `[]` vs `None` both come out empty. That is
  the origin of the `{"old_value": null, "new_value": null}` records I had to filter, and why the
  unfiltered ranking was topped by an artefact (the uniform "263 changes / 179 hotels" block).

  Fix would be to compare the json-safe values rather than the raw ones in `_post_save`.
  Small, self-contained change.

  ### Two candidate tickets (not raised — your call)

  1. `Event.impersonator_uuid` is dead weight: either populate it from the resolved
     `impersonated_actor` or drop the column. Currently it misleads anyone reading the table.
  2. `ChangeTracker` emits no-op change events; compare post-`_json_safe` values.
     Also worth replicating `event_eventrelatedobject` to Snowflake if impersonation
     attribution matters for future analysis.
project: 2026-08-05-strategy
source_id: null
tags: []
time_minutes: 5
title: What fields regularly get changed early in the life of a hotel - event analysis?
updated: 2026-08-07 15:59:04.689761
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