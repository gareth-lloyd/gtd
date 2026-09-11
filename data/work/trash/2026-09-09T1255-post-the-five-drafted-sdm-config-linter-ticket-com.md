---
area: null
completed_at: null
contexts:
- react
created: 2026-09-09 12:55:30.979046
defer_until: null
due: null
energy: medium
id: 2026-09-09T1255-post-the-five-drafted-sdm-config-linter-ticket-com
order: null
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 25
title: Post the five drafted SDM config-linter ticket comments and settle the SDM-5039
  priority question
updated: 2026-09-10 15:37:59.283913
waiting_on: null
waiting_since: null
working_on: false
---

Five comments drafted 2026-09-09 but NOT posted — all need a final read before sending. They post as me.

Context: ENT-7201 was moved to the SDM team and is now **SDM-5039**
(https://linear.app/canary-technologies/issue/SDM-5039/consistency-rules-validate-declared-keys-statically-and-decide-any-non).
The move reverted priority High -> Medium and status Todo -> SDM Triage.

---

## 1. SDM-5039 — the important one

Three things I found after writing this up, worth having on the ticket before anyone starts:

**Scope 3's exemption list is incomplete.** ENT-7113 documents a second, larger class: the FINAL rule mandating `is_tokenizing_with_hotel_payment_gateway = True` + non-null `payment_gateway_config_id` false-flags 154 live Wyndham hotels, overwhelmingly international and all Opera Cloud, which tokenize via the PMS-native tokenizer or raw Stripe.js. That path is first-class — see the `check_in_tokenizes_via_stripe_gateway` docstring in `check_in/services/check_in_payment.py`, which names both flows. The consistency rule as written only fires when the tokenize flag is True so it probably won't hit those 154, but scope 3 should name the class rather than only the legacy FreedomPay/Shift4 one.

**Scope 2 and ENT-7113 are the same problem from opposite sides.** ENT-7113 changes what the tree *declares* for those keys; scope 2 changes how consistency rules *read* declarations. Different teams, no link between the tickets. Whoever picks either one should read the other first.

**Sequencing:** ENT-7103 (#55727, in review) touches `conformity.pyi`, `setting_type_generator.py` and `conformity.py` — the same generated-stub machinery scope 1 depends on. Land that first or expect a regeneration conflict.

Also flagging: this dropped to Medium when it moved to the SDM team. I'd filed it High on the basis that it gates the linter's correctness — happy either way, but wanted to make sure the change was intentional rather than a side effect of the move.

---

## 2. SDM-4993

Worth noting how load-bearing this is for SDM-5039. `HotelConfigHealthService.check()` runs `_check_consistency` against a real hotel's settings, so it is the only one of the three layers where a null-presence rule actually means anything — the tree/`finalize()` and Django-system-check layers both evaluate tree-declared settings, where `ANY_NON_NULL` is a non-None sentinel and every presence rule passes regardless.

That makes this PR the practical answer to SDM-5039's scope 2: presence rules are valid here and nowhere else. If we go with layer-tagging rather than making rules sentinel-aware, this is the layer they'd be tagged to.

---

## 3. SDM-4990

The constraint here — "every key must exist in `conformity.pyi`" — is exactly what SDM-5039 scope 1 is trying to make automatic. Right now it's author discipline, and we already know what happens when it slips: `payment_gateway_required_for_tokenization` sat dead from ENT-4739 until #55352 because nothing checked, and its tests passed because they were built from the same wrong keys.

Two notes for this batch:
- Until scope 1 lands, a typo'd key here is a silent no-op with green tests. Worth eyeballing the keys against the stub by hand before merge.
- ENT-7103, the explanation-field blocker listed in the constraints, is now in review as #55727.

---

## 4. SDM-4991

ENT-7113 is worth reading before writing this rule — it's not just the same capability-dimension ask, it's a worked example of the failure mode. Two FINAL rules that encode the US mainstream setup, with counts: 154 international hotels flagged on tokenization, plus the auto-post family flagging arrival-only hotels where posting is a no-op.

The relevant lesson for "gateway can't do auth-only": expressing it over `hotel.pms` + gateway settings is right, but the gateway relation itself isn't in the flat keyspace (`AutoOneToOneField` on `hotels/models/payment_gateway.py`, not one of the `CONFIGURABLE_MODELS`), which is the same expressibility wall SDM-5039 scope 3 hits. If you end up needing legacy-gateway or capability presence as a derived scalar setting, that's a shared need across both tickets and probably worth doing once, on our side.

---

## 5. SDM-4989

Thanks for picking up the repoint — that rule had been dead since ENT-4739 and I'd only clocked it last month.

One gap in #55352: the port didn't bring across the exemption from `CheckInConfiguration.clean()`, which skips the check when `hotel.payment_gateway.gateway` is set. Legacy FreedomPay/Shift4 hotels tokenize without a `payment_gateway_config_id`, so they'll trip the rule once it's actually firing. Tracked as scope 3 on SDM-5039 rather than something to fix in this PR — flagging so it doesn't get lost when this merges.

Separately, ENT-7113 documents a second exemption class on the same two keys (PMS-native tokenization, 154 international hotels). Probably doesn't affect this rule since it only fires when the tokenize flag is True, but worth a look.

---

## Also outstanding (not SDM, don't post with the above)

- **Andrea Bradshaw** asked the priority question on ENT-7201 on 13 Aug and pushed back on capacity. The answer changed materially — it no longer costs Enterprise capacity. She'll see an unexplained Triage->Todo/High->team-move on a ticket she challenged. Worth a short reply closing that loop.
- **Link ENT-7113 <-> SDM-5039** as related. Nobody has connected them.

Skipped deliberately: SDM-4992. Its dormant-checker overlap is thematic (different registry, `FEATURE_FLAG_CHECKERS`) — a comment there would be noise.

Full drafts also at: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/c0864814-daf4-447d-8c01-5698fa6332fb/scratchpad/comments.md (session-scoped, will not survive)