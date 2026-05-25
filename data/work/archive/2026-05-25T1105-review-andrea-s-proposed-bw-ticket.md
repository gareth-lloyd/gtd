---
area: null
contexts: []
created: 2026-05-25 11:05:21.861001
defer_until: null
due: null
energy: low
id: 2026-05-25T1105-review-andrea-s-proposed-bw-ticket
order: null
output: |
  ## Agent run 2026-05-25T11:45Z

  Reviewed ENT-6304 against the actual code paths it cites. Andrea's spec is solid overall — references are accurate, the
  approach mirrors the existing compendium populator, and the key risk (BW↔Canary code mapping) is called out
  prominently. A few gaps / things worth pushing back on before she starts cutting code:

  ### Real issues

  1. **Missing Plan + Config dataclass.** The spec only lists a `Provider`, but the BW_MSA pipeline at
     `onboarding/models/property_configuration_processes.py:1538` registers entries as `plan=X, config_provider=Y`.
     Without a `PopulateRoomImagesPlan` class and a config dataclass under `configuration_providers/configs/`, there's
     nothing to wire in. The onboarding `CLAUDE.md` is explicit: providers are paired with Plans + Configs. Spec should
     add:
       - `onboarding/plans/populate_room_images_plan.py` (+ register in `services/plan.py:KNOWN_PLANS`)
       - `onboarding/configuration_providers/configs/populate_room_images.py`
       - Test file under `tests/plans/`

  2. **`_set_images_on_entity` is the wrong template to mirror.** That helper goes through `entity.albums.first()` →
     `Album.image_group`. `Room` has `image_group` directly (no Album indirection), so the mirroring instruction is
     misleading. The reusable bits are just `ImageGroupService.create()` + `ImageGroupService.add_image(file=bytes)` —
     spec should say "reuse the inner fetch+add loop", not "mirror `_set_images_on_entity`".

  3. **`RoomType.room` is nullable.** `room_type.py:24` — `null=True, blank=True, on_delete=SET_NULL`. The spec doesn't
     mention what happens for orphaned RoomTypes (Room=NULL). Should skip silently with a log line, not blow up.

  4. **Many-to-one RoomType→Room means "skip if image_group has images" is order-dependent.** Multiple `RoomType.value`s
     can point to the same `Room` (different PMS codes for the same physical room). If two different BW
     `roomCategoryCodes` both match RoomTypes on the same Room, only the first one in iteration order wins. Probably
     fine for v1, but should be acknowledged in the spec so reviewers know it's deliberate.

  5. **Partial-failure idempotency.** "Skip if image_group has any image" is correct for protecting manual uploads, but
     it also means: if image #3 of 6 fails mid-populate, the next run sees a non-empty group and skips entirely → the
     room is permanently stuck with a partial set unless someone manually clears it. Worth deciding now:
       - Track populator's own writes (e.g. a flag on `ImageGroup` or an `OnboardingValue`), or
       - Accept partial as good enough and add a manual re-run admin action, or
       - Treat any populator failure as fatal so we retry the whole hotel.

  6. **Only wiring into `BEST_WESTERN_MSA`.** `PopulateCompendiumPlan` appears at three pipeline sites in
     `property_configuration_processes.py` (lines 1259, 1538, 1834). Spec only mentions BW_MSA. Worth checking whether
     the other two BW onboarding flows also need room images (likely yes if they were getting the compendium).

  ### Smaller nits

  - **Verification is under-scoped.** "2–3 BW hotels" is a reasonable spot-check, but `RoomType.value` is set by PMS
    sync, and BW supports several PMSes — codes may diverge by PMS, not just by hotel. Suggest sampling at least one
    hotel per BW-supported PMS, not just multiple hotels on the same PMS.
  - **Perf / blast radius unmentioned.** Each matched Room → N sequential `requests.get()` calls. A 200-room hotel with
    4 photos each = 800 inline HTTP fetches inside the onboarding plan transaction. Compendium does the same and
    presumably is fine; just worth confirming this hasn't been a pain point.
  - **`Hotel.has_addons` short-circuit.** The addons app's `CLAUDE.md` requires query helpers to return falsy when
    `has_addons` is False. Likely irrelevant for an onboarding populator (the hotel is mid-setup), but worth a one-line
    acknowledgement so a reviewer doesn't get hung up on it.

  ### What's good

  - All BW client method names check out (`fetch_images_by_category`, `images_by_room_category_code`, `fetch_image`).
  - File paths and line refs are accurate.
  - Skip-if-already-has-images guard for protecting manual uploads is the right instinct.
  - Out-of-scope list (post-onboarding refresh, backfill, configurable mapping) is well-drawn.
  - The mapping-assumption callout is prominent and correctly identifies the highest-risk part of the design.

  ### Recommendation

  Spec is ~80% there. Andrea should add the Plan + Config classes to the spec, clarify the `_set_images_on_entity`
  reference, decide the partial-failure policy, and either confirm or extend the pipeline-registration scope. Once
  those are addressed, this is ready to implement.
project: null
source_id: null
tags: []
time_minutes: 5
title: review andrea's proposed bw ticket
updated: 2026-05-25 11:51:12.739426
waiting_on: null
waiting_since: null
working_on: false
---

https://linear.app/canary-technologies/issue/ENT-6304/populate-room-images-during-bw-onboarding