---
area: null
completed_at: 2026-11-10 16:26:39.272080
contexts:
- deep
created: 2026-11-10 11:04:30.932217
defer_until: null
due: null
energy: high
id: 2026-11-10T1104-progress-ent-8222-review-eng-design-gjm-drift-dete
order: null
output: |-
  ## Agent run 2026-11-10T12:11

  Reviewed iteration 1 of the GJM Drift Detection design (https://app.notion.com/p/41381468615181089aa2d0e08023625a) against master, your ENT-7726 stack and plan, and Tincho's reader POC. Nothing was posted anywhere. A draft review comment is at the bottom.

  **Verdict:** the direction is right and matches your own proposal (https://app.notion.com/p/3f9814686151813da661eb802029d0eb). Iteration 1 is not "almost no big effort" as written: two claims are wrong against the code, and the per-message records need a mechanism the doc defers to iteration 2.

  ### Decisions only you can make

  1. **SupersetOf lives in the conventions PR.** The doc's dependency table lists #61724 (https://github.com/canary-technologies-corp/canary/pull/61724) as "SupersetOf predicate". That PR is the whole conventions engine, PR 4 of your stack. Either pull `SupersetOf` forward into #59059 or #61725, or iteration 1 waits for conventions.
  2. **Aggregate key or per-message keys in `StoredHotelAttributes.drifts`.** Your proposal put per-message records out of scope ("only the config key that has drifted would be recorded"), and your plan says drift does not change what it persists. The doc persists one synthetic `.missing` key per message. See finding 2.
  3. **Who builds the column-less reader setting.** Your ENT-7726 comment on 2026-11-05 told Tincho to extend your draft reader (https://linear.app/canary-technologies/issue/ENT-7726). The doc records this as "ENT-7726 settled: ours" but gives no design. Your plan's PR 6 section already has one (`ReaderSetting`, `declare_reader_setting`, declared items, the audit of callers that assume `hotel.`). Tincho has not seen it unless you share it.
  4. **Your stack is the critical path.** #59047, #59059, #61725 and #61724 are all still draft, and nobody from pod-enterprise has reviewed #59047 or #59059. Iteration 1 cannot start wiring until those land.

  You also have three unanswered review comments from Tincho on #61725, dated 2026-11-04. They are the questions this design depends on: https://github.com/canary-technologies-corp/canary/pull/61725#discussion_r4471587063 (registry rejects a key with no column), plus two on `conformity.py` (does `get_actual_hotel_setting` degrade for an unknown key; `HotelValidationResult` returns the raw value, not the reader's).

  ### Findings on iteration 1

  1. **"First sweep baselines silently" is wrong for this cohort.** `drift.py:180` treats a hotel as a baseline only when `drifts_calculated_at is None`. Every live Wyndham hotel has already been swept, so the first night the rule ships, every missing message posts to `#enterprise-drift-detection` as new drift: about 50 hotels with the title fallback, about 200 without. The rollout needs an explicit step: warn the channel, or seed the keys into `drifts` before the first alerting run.
  2. **Per-message keys do not get the pipeline "for free".** The sweep log loop (`drift.py:195-197`) and the acknowledgement service (`drift_acknowledgement.py:16-25`) both call `get_setting_value_for_hotel_attributes` and `get_actual_hotel_setting` with each drifted key. A synthetic `hotel.guest_journey.message.mid_stay_message.missing` key is not a setting key, so each consumer needs a resolver for it. That resolver is the `DriftContributor` the doc defers to iteration 2. Simpler iteration 1: persist the one aggregate key and expand to per-message lines only when rendering the Slack alert and the Manage page. The cost is one acknowledgement per hotel, not per message.
  3. **Acks do not consult readers.** Your `value_readers.py` on #61725 says a reader is used by the conformity comparison only, never by `get_actual_hotel_setting`. The ack snapshot and the drift log both use `get_actual_hotel_setting`, so for a column-less key they have nothing to read. This must change in either design.
  4. **The ack snapshot of a set is not stable.** `_actual_value_str` stores `str(value)`. The POC reader returns a `set` of `StrEnum`, whose print order changes between processes (string hash randomisation), so an ack would spuriously stop matching. The reader should return a sorted tuple, or the ack should serialise sets in sorted order.
  5. **`cleanup=False` does not exist.** The doc says drift reads pass `cleanup=False` and write nothing. On master `GroupUseCaseService.get_guest_journey_messages_by_use_cases` (`onboarding/services/group_use_case_service.py:90`) has no such parameter and deletes stale association rows as it reads. The POC (#63299, https://github.com/canary-technologies-corp/canary/pull/63299) calls it as is, so the reader writes today. Adding the parameter is a change to an onboarding service and belongs in the rollout list.
  6. **Title fallback.** About 150 hotels have the message but lack the association row, so the reader falls back to matching by title. Titles are hotel-editable and translated, so the fallback silently fails for a hotel that renamed the message. A one-off backfill of the missing association rows fixes the data and keeps the reader a single query. Worth asking why a backfill was not chosen.
  7. **Echo Suites is not excluded by the node.** `WYNDHAM_NORTH_AMERICA_LIVE` (`enterprise_wyndham/configs/wyndham.py:41`) matches on MSA and country only. A `FINAL` rule there flags every US/CA Echo Suites hotel unless a heavier Echo Suites node defines its own set. The doc calls the node "a close approximation" and does not say how the exclusion is made.
  8. **The seven use-cases are never listed.** Wyndham selection today also varies by a site-ID exclusion list (the day-of check-in reminder) and by segmentation v1 against v2 (which welcome messages exist). The spike screenshot shows "Welcome Message (Non-Members)" as required, which looks segmentation-dependent. The required set must hold only what every hotel on the node gets. I did not verify the seven against `WyndhamGuestJourneyMessagesProvider`; ask Tincho to list them with that check.
  9. **Key naming.** The setting key is `guest_journey.message_use_cases` and the drift keys start `hotel.guest_journey.message.`. Your plan flags the prefix as open, and seven callers assume `hotel.`. Pick one.
  10. **Smaller points.** `NoneOf` is in the iteration 1 rollout (step 3) but presence does not need it. A present but disabled message reads as conforming, although "turns checkout off" is the doc's own opening example; the reader could return enabled use-cases only. The spike branch behind "121 backend tests" is not linked; #63299 is a 72-line reader.

  ### Iteration 2, briefly

  Agree with the doc that prevalence of edited copy must be measured before committing. On the seam, I would put the contributor registry in the drift layer, not on `ConformityService`. The doc's line that ENT-7726 "settled the related reader question our way" overstates your comment, which only said to extend the reader.

  ### Not checked

  - The prod numbers (4,582 hotels, 95%, about 50 missing) are Tincho's; I did not re-run them.
  - The spike's Manage UI and its tests; no branch is linked.
  - The Notion design doc has no comments yet. Status is "REVIEW ME!".

  ### Draft review comment (not posted)

  For the Notion doc or ENT-8222 (https://linear.app/canary-technologies/issue/ENT-8222/review-eng-design-gjm-drift-detection-gareth):

  > Thanks Tincho. Iteration 1 is the right first step and I agree with the split. A few things to settle before building:
  >
  > 1. First run: a hotel is only baselined when `drifts_calculated_at` is null, and the Wyndham cohort has already been swept. So the first night posts every missing message as new drift. We need a channel warning or a seeding step in the rollout.
  > 2. Per-message `.missing` keys: the sweep log and the ack service look up expected and actual values by setting key, so synthetic keys need the resolver you have in iteration 2. For iteration 1, could we persist the single `guest_journey.message_use_cases` key and expand per message only in the Slack line and on Manage?
  > 3. Acks read through `get_actual_hotel_setting`, which does not consult readers. That needs changing for a column-less key. The reader should also return a sorted tuple, since `str()` of a set is not stable between processes and would break ack matching.
  > 4. `get_guest_journey_messages_by_use_cases` has no `cleanup` parameter today and deletes stale associations as it reads. Please add that change to the rollout.
  > 5. Title fallback: would a one-off backfill of the ~150 missing association rows be simpler than matching titles, which hotels can edit?
  > 6. Scope: `WYNDHAM_NORTH_AMERICA_LIVE` does not exclude Echo Suites. How is that exclusion made? Can you also list the seven use-cases and confirm none depends on the site-ID exclusion list or on segmentation v1/v2?
  > 7. Dependencies: `SupersetOf` is in #61724, which is the conventions engine. I will look at moving it earlier in the stack. `NoneOf` can drop out of iteration 1.
  >
  > I owe you answers on your three #61725 comments and will reply there. I will share my notes on the reader-setting design so you can build on them.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-8222/review-eng-design-gjm-drift-detection-gareth
tags:
- morning-gtd
- linear
time_minutes: 60
title: 'Progress ENT-8222: Review eng design: GJM Drift Detection'
updated: 2026-11-10 16:26:39.272058
waiting_on: null
waiting_since: null
working_on: false
---

Tincho assigned me the review sub-issue and @mentioned me on ENT-8066: design is split into two iterations, focus on iteration 1 first. Doc: https://app.notion.com/p/41381468615181089aa2d0e08023625a
https://linear.app/canary-technologies/issue/ENT-8222/review-eng-design-gjm-drift-detection-gareth
Mention: https://linear.app/canary-technologies/issue/ENT-8066/eng-design#comment-be4c8f45