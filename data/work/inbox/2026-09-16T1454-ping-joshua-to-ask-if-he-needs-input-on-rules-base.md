---
area: null
completed_at: null
contexts: []
created: 2026-09-16 14:54:38.205014
defer_until: 2026-09-28 09:00:00
due: null
energy: low
id: 2026-09-16T1454-ping-joshua-to-ask-if-he-needs-input-on-rules-base
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: 5
title: message joshua re SDM rules-engine asks and the binding rules tree
updated: 2026-09-25 15:10:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

Message to Joshua (cc Luiza). State as of 2026-09-25: SDM-5039, SDM-4991 and umbrella SDM-4862 are Done; PR #56000 merged 9/21 with my approval. Deposit-slot question is closed: Luiza's code reading holds (auto-post CC flag only gates the card push in `pms_operations`; slot is read on the payment path), replacement rule `deposit_slot_required_for_pms` is on master (#55498). Nothing to refute.

What to communicate:

1. **ENT-7488 (capabilities as settings keys): different shape, same outcome.** Their "gateway can't do auth-only" and ENT-6097 Part 2 rules ("PMS lacks `post_deposit_token` → no Canary deposits") are attribute → setting impossibilities. The Binding Rules Tree design (https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09, in review) hosts exactly these under `binding/pms/` with `authority=PMS_CAPABILITY`, scoped by `capabilities_absent`, and its root matches every hotel — the two things SDM-4862 said were missing ("no capability tree", "non-enterprise hotels have no tree"). So the answer to ENT-7488 is a matching *dimension* on `HotelAttributes` (PMS capabilities already a local M2M; gateway capabilities need a stored representation), not derived settings keys through `generate_setting_types`. Caveat they already hit: `NexiConfig.CAPABILITIES` was wrong for years, so the dimension must come from the source the runtime trusts, not the class-set.
2. **The split going forward.** Setting → setting rules (deposit slot when posting on, fraud-flag pair) stay consistency rules. Attribute → setting rules (capability absent → value) become binding rules and get boot check, drift and eventually `pre_save` refusal, including on enterprise hotels.
3. **Explanations.** `explanation=` reaches drift only; E001 consistency errors never see it (`checks.py`, `services/consistency.py`). Small standalone fix; offer to take it or let them.
4. **Ownership / review turnaround.** Propose SDM as co-owner (CODEOWNERS) of `binding/pms/` with PMS Platform — they hold the incident evidence — and name a reviewer on my side for SDM PRs touching the engine.
5. **Workstream E.** Milestone is 18.75%, not stalled: SDM-4863/4994/4995 all In Review (PRs #57320, #57051, #56838, #56836). Only SDM-4996 (template/named-config packages) waits on us. Give a date or say we can't yet.

Ask: are they happy for ENT-7488 to be answered by the binding tree + a capabilities dimension, and does Luiza want to review the doc?
