---
area: null
completed_at: 2026-10-01 15:31:22.242927
contexts:
- react
created: 2026-10-01 10:23:58.459754
defer_until: null
due: 2026-10-01
energy: low
id: 2026-10-01T1023-reply-to-leandro-alvarez-re-keeping-base-registrat
order: null
output: |-
  ## Agent run 2026-10-01T14:58:00+03:00

  Nothing was sent. Draft reply below for you to edit and post in the group DM
  (https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1790795346924589).

  ### Draft reply

  That works for me, and it's the shape I'd want anyway: the script keeps writing the base regcard, then calls your services (`migrate_hotel_to_v3`, then `move_hotel_to_catalog`) instead of building catalog fields and forms itself.

  Two things to settle before we do it for IHG:
  • Re-runs. Today the regcard plan errors out and rolls back if the hotel is already on V3, because overwriting the card would re-seed the live flow. Once a hotel is on the catalog, how does a later regcard change reach it (e.g. the IHG country additions Andrea is doing)? If the answer is "it doesn't", that's the point where we'd need the default catalog fields and forms.
  • Refusals. The move to catalog can refuse (card doesn't compose back, portfolio-managed card, V3 blockers). I'd have the script leave the hotel on the regcard and report it rather than fail the whole onboarding. Does that match how you'd want it handled?

  Timing is still whenever Connor confirms V3 covers all flows. @Andrea with this shape it's back to roughly "set the version plus two service calls", does that sound small enough to pick up when the signal lands?

  ### What the draft is based on

  - Thread context: Andrea confirmed the IHG scripts don't set a version (new hotels get the V2 default) and exit with a rollback if V3 is detected. Lea proposed two pieces: make the IHG property V3, then switch it to the catalog via Rafa's regcard-to-catalog conversion. Andrea's worry was that creating blocks and steps in the script would need more work and support.
  - Yesterday's call "Step configurator and rules-based" (https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c): the regcard-then-convert workaround was described there too, with the long-term intent to retire the registration card model. Granola summary only, I did not read the transcript.
  - The V3 guard is `AddRegistrationCardPlan.execute` in `backend/canary/onboarding/plans/registration_card_plans.py:69`, raising `ERROR_HOTEL_ON_CHECK_IN_V3`. Its comment says the V3 sync signals would re-seed the live guest flow from the overwritten card.
  - Rafa's conversion is `GuestFieldsSourceService.move_to_catalog` in `backend/canary/guest_experience/services/guest_fields_source.py`, wrapped for V3 hotels by `move_hotel_to_catalog` in `backend/canary/guest_experience/services/v3_migration.py:125`, and exposed as the `move_hotels_onto_catalog` management command. PRs #56116 (https://github.com/canary-technologies-corp/canary/pull/56116) and #56118 (https://github.com/canary-technologies-corp/canary/pull/56118), merged 2026-09-24 and 2026-09-29.
  - It refuses non-V3 hotels, portfolio-managed cards, hotels with no schemaform step, and cards whose catalog rows don't compose back to the live form. `migrate_hotel_to_v3` raises `V3MigrationBlocked` on some card-upload, surcharge and Canary-managed-payment configs unless forced.
  - This lines up with what you told Lea on 2026-07-01 in the same DM: scripts should call a pod-owned service rather than hand-roll config on the pod's models.

  ### Not verified

  - What happens on a catalog hotel when its registration card is later edited. I read that `uses_field_catalog=True` makes the form compose from the catalog, so I assumed card edits stop reaching guests, and phrased it as a question to Lea.
  - Whether any IHG hotels have portfolio-managed registration cards (would be refused by the move). Not checked against production data.
  - The second bullet's recommendation (leave on regcard and report, rather than roll back) is my suggestion, not something anyone agreed. Cut it if you'd rather Lea propose the behaviour.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1790795346924589
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Reply to Leandro Alvarez re: keeping base registration cards in the onboarding
  script'
updated: 2026-10-01 15:31:22.242916
waiting_on: null
waiting_since: null
working_on: false
---

Group DM with Andrea. He suggests not building default catalog fields/forms into the script now: keep working with base registration cards and let Rafa's regcard-to-catalog script do the rest.
https://canarytechnologies.slack.com/archives/C0B4QD01GP8/p1790795346924589