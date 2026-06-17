---
area: engineering
contexts:
- deep
created: 2026-06-16 16:24:56.442407
defer_until: null
due: 2026-06-17
energy: medium
id: 2026-06-16T1624-re-review-gaston-s-big-pr
order: 7
output: |
  ## Agent run 2026-06-16T13:27:35Z

  **PR:** VOX-2622 "Decouple voice config from onboarding + adminland voice setup"
  by Gaston (gdelarrechea) — https://github.com/canary-technologies-corp/canary/pull/47421
  Linear: https://linear.app/canary-technologies/issue/VOX-2622
  State: OPEN, reviewDecision=APPROVED (mason from voice side, abrad), but mergeable=CONFLICTING.
  +3171 / -1269, 44 files.

  ### Intent of THIS re-review (figured out first, as asked)
  This is your own PR review thread. On 2026-06-11 you left two substantive
  comments on `voice/services/voice_setup.py`. Gaston pushed fixes on 06-12,
  marked both resolved, and on 06-16 left ONE new unresolved comment directed at
  you (cc @gareth-lloyd) on `onboarding/admin/onboarding_value.py:47`. So the
  re-review = (a) verify his two fixes actually do what he claims, (b) answer his
  open question. Both done below.

  ### Your comment #1 — can_activate enforced client-side only → FIXED (exceeded the ask)
  I asked for a guard at the top of `activate_voice_for_hotel` raising 422 when a
  config already exists. He did better: re-checks `status.can_activate` up top AND
  inside the txn does `Hotel.objects.select_for_update().get(pk=...)` then re-checks
  `Configuration.objects.filter(hotel=hotel).exists()` before any external call.
  That closes the double-submit RACE (not just the sequential case) by serializing
  on the hotel row — the loser blocks, re-reads the winner's config, and 422s
  without buying a duplicate Twilio number / LiveKit trunk. Verdict: fully resolved.

  ### Your comment #2 — external calls inside txn → orphaned resources → ADDRESSED (scoped + logged, reorder deferred)
  He added structured audit logging on activation (`_log_voice_activated`) and
  clarified access control was missing from the PR: setup is gated to non-live
  hotels / temporary SupportAccessGrant users (`get_voice_setup_status` →
  `can_activate=False` + `_SUPPORT_ONLY_REASON` otherwise), so operator-triggered
  retries are currently rare. He explicitly deferred reordering the irreversible
  Twilio purchase behind the failure-prone LiveKit/geocode steps, citing PR size,
  and flagged it as a real concern once self-onboarding ships. Reasonable to accept
  now. NOTE for later: the orphaned-trunk failure mode is NOT fixed, only made
  rarer + traceable — worth a VOX follow-up ticket before self-serve onboarding
  opens this path to live/hotel-side users.

  ### His open question (onboarding_value.py:47) — "open to removing clean_to_number since it would fail later on voice config creation"
  ANSWER: keep it. It is NOT redundant.
  - `clean_to_number` calls `format_strict_e164(value)` per formset row, attaching
    a per-FIELD error to the offending `to_number` input and normalizing the stored
    number (e.g. "+1 (202) 555-1234" → "+12025551234").
  - The "fail later" path does NOT catch a bad number at write time. I verified the
    centralized `validate_data` → `validate_with_registered_schema` runs
    `ForwardNumberSpecSchema`, whose `to_number = fields.String()` only checks
    string-ness, NOT E.164. The E.164 invariant (`validate_forwarding_specs` →
    `validate_e164_phone`) only runs at `VoiceAIConfig.build()`, i.e. at
    activation / onboarding-script-run time — far from the operator who typed it.
  - So removing it trades an immediate, per-field form error for a delayed,
    decoupled failure at script-run/activation. That's strictly worse operator UX
    and a footgun (bad number sits stored in an OnboardingValue until much later).
  - It already uses the shared `format_strict_e164` primitive, so there's no rule
    duplication — it just applies the canonical check at the form boundary, which
    is consistent with the PR's "centralize the rule" goal.
  - Removing it would also delete 4 real tests in
    `onboarding/tests/admin/test_forwarding_config_formset.py`
    (rejects no-country-code / too-short / too-many-digits; normalizes formatting).
  Minor optional polish (non-blocking): could call
  `voice_input_validation.validate_e164_phone` instead of `format_strict_e164`
  directly to centralize on one named voice helper — but importing the canary util
  from onboarding admin is arguably cleaner than reaching into the voice package,
  so current code is fine as-is.

  ### Two unresolved nits from others (already non-blocking, FYI)
  - Mason / abrad: `get_voice_setup_status` resolves the variant; `activate_voice_for_hotel`
    re-resolves it via `resolve_voice_config_cls`. Could return the variant from
    status to avoid the second lookup. Cosmetic.

  ### Merge-readiness flags (not review content, but you'll want these)
  - mergeable=CONFLICTING — has conflicts with master; needs a rebase before merge.
  - CI: `make check-dependency-changes` FAILING and `review-bot` FAILING; most other
    checks (Django tests skipping, typecheck, security, migrations) pass/skip.
    Worth confirming the dependency-changes failure is real before merge.

  ### Bottom line
  Both of my prior comments are satisfactorily handled (#1 fully, #2 scoped+deferred
  with justification). Recommended reply to Gaston: KEEP `clean_to_number`. No new
  blocking concerns from me. Remaining gates are merge-conflict + the two failing CI
  checks, not code review.

  --- DID NOT post anything to GitHub. Draft reply for his line-47 question (post only
  if you approve):
  > Let's keep it. The schema validation (`ForwardNumberSpecSchema.to_number =
  > fields.String()`) doesn't check E.164 — the only E.164 enforcement is at
  > `VoiceAIConfig.build()` (activation/script-run time). So without `clean_to_number`
  > a bad number is accepted into the OnboardingValue and only blows up much later,
  > away from the operator. The field-level clean gives an immediate per-row error and
  > normalizes the number, and it already uses the shared `format_strict_e164`
  > primitive so there's no duplicated rule. Happy as-is.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 15
title: Re-review GAston's big PR
updated: 2026-06-17 15:23:42.082423
waiting_on: null
waiting_since: null
working_on: false
---

Figure out intent first. 
https://github.com/canary-technologies-corp/canary/pull/47421