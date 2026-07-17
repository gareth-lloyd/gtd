---
area: null
contexts: []
created: 2026-07-16 14:35:46.248130
defer_until: null
due: 2026-07-17
energy: low
id: 2026-07-16T1435-give-peter-feedback-on-prs
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Give Peter feedback on PRs
updated: 2026-07-17 12:09:25.963246
waiting_on: null
waiting_since: null
working_on: false
---

Serious issues from the review of Peter's GJ auto-translate stack (EMEA-394→397). Verdicts: [#49749](https://github.com/canary-technologies-corp/canary/pull/49749) request-changes · [#50084](https://github.com/canary-technologies-corp/canary/pull/50084) request-changes · [#50405](https://github.com/canary-technologies-corp/canary/pull/50405) request-changes · [#50412](https://github.com/canary-technologies-corp/canary/pull/50412) approve-with-nits.

## Stack hygiene (fix before anything merges)

1. **Fix commits are on the wrong branches.** The guardrail case-sensitivity fix for #49749 lives on the #50084 branch; the excluded-words prompt fix (`1ca9501`, which Macroscope marked "resolved") lives only on the #50405/#50412 branches. Merging any PR alone ships bugs its own review thread believes are fixed. Cherry-pick each fix down to its owning PR, then rebase the stack.
2. **CI red on #50084/#50405**: `opinionated_state.py` out of sync, pyright errors (one on #50405's own line), unformatted test files. #50412's frontend lint auto-commit failed to push.
3. **Hand-seeded feature flag will be clobbered.** `guest-journey-auto-translate` was hand-added to `generated_features.py`, but the nightly GrowthBook sync regenerates that file. If the flag isn't created in the dashboard before the first nightly sync after merge, the sync PR drops the constant and fails typecheck, blocking org-wide flag-sync automation. Create the dashboard flag *before* merging #50405.
4. #50405/#50412 bases are 2 commits stale — #50412's apparent backend changes are comment-only; a rebase makes it purely frontend.

## #49749 — guardrails (both verified by executing the branch code)

- **Dropped merge-tag parameters pass** (`translation_guardrails.py:99`): `{{ form_url_button:Check in now }}` → `{{ form_url_button }}` passes, then renders the hard-coded English "Go to form" inside a translated email. Peter dismissed Macroscope's adjacent comment saying placeholder tags never had parameters — factually wrong (`form_url_button`, `payment_receipt` take them; his own test uses one). Needs re-litigating with the render-default evidence.
- **CJK/Thai opt-out keywords match by bare containment** (`:129-153`): a candidate saying only 免费停车 ("free parking") satisfies the STOP check because 停 is inside 停车; same for Thai ออก. A translation that drops the opt-out instruction entirely can pass — for exactly the target languages this feature is for.

## #50084 — LLM service

- **No identity/completeness check** (`template_translation.py:96-98`): a model returning the English source unchanged, or a gutted "Hola {{ guest_first_name }}" for a 500-char source, passes every structural guardrail and gets stored. Fix: `candidate != source` + length-ratio bound. (Macroscope raised the length half; unaddressed.)
- `channel` is a bare `str` — passing `"SMS"` silently gets email semantics and disables the opt-out guardrail. Use `Literal["email","sms"]`.

## #50405 — endpoint

- **Blocker**: `translated_field_validation.py:44` passes `list[str]` where `list[LANGUAGE_CODE]` required — typecheck fails on its own line.
- **No `target_language` allowlist** (`views/guest_journey_translate_field.py:64`): any string is accepted and interpolated into the LLM prompt as the language name via the `SUPPORTED_LANGUAGES.get(target, target)` fallback — injection surface + garbage-cost calls. Validating membership in `SUPPORTED_LANGUAGES` also fixes the blocker.
- No `source_text` length cap on a paid-LLM endpoint (comparable `booking_link_parse.py` caps at 2048 chars).

## #50412 — frontend (non-blocking but worth raising)

- X-ing out of a **partial** failure permanently disarms the banner for those edits — the failed language silently stays stale with no retry path until the source is re-edited. Code comments say deliberate; deserves an explicit decision + test.
- Network/thrown errors swallowed into a generic string with no Sentry capture — systematic failures would be invisible to engineering.

Full review with minors/nits is in the Claude session from 2026-07-16 (canary repo).