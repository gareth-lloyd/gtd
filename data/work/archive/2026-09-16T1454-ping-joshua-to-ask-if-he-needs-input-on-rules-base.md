---
area: null
completed_at: 2026-09-28 14:41:55.237917
contexts: []
created: 2026-09-16 14:54:38.205014
defer_until: null
due: 2026-09-28
energy: low
id: 2026-09-16T1454-ping-joshua-to-ask-if-he-needs-input-on-rules-base
order: null
output: |
  ## Agent run 2026-09-28T11:15:49Z

  NOTHING SENT. Draft below, ready to paste. Two placeholders need your decision before it goes: [REVIEWER + DAY] and [SDM-4996 DATE].

  ### Read this first: four things in the task notes that no longer hold

  1. Workstream E IS waiting on us, on review. All four brand-profile PRs are open with only Joshua's approval (jwhart91) and an outstanding review request for pod-enterprise. Luiza asked in #epd-enterprise on 9/24 and got zero replies: https://canarytechnologies.slack.com/archives/C047K6WSUJY/p1790280101226119
     - They are a stack: #56838 (base master) -> #56836 -> #57051 -> #57320. Only #56838 targets master, and its "Re-run gate after review" check shows as failed in the status rollup.
     - #56838, #56836 and #57320 also request pod-arrivals-departures, because CODEOWNERS line 285 gives `/backend/canary/enterprise_four_seasons/` to A&D. #56838 and #56836 request pod-platform too. So an Enterprise approval alone will not clear all four.
     - Your own approval cannot clear the gate. pod-enterprise members are abrad, rrgrs, lmenaolivares, andresfigueira, martinrodriguezcanary. gareth-lloyd is not in it (Luiza hit this on 9/17 with #56680).
     - PRs: https://github.com/canary-technologies-corp/canary/pull/56838 , https://github.com/canary-technologies-corp/canary/pull/56836 , https://github.com/canary-technologies-corp/canary/pull/57051 , https://github.com/canary-technologies-corp/canary/pull/57320
  2. Joshua may be starting the SDM-4996 work solo. His 9/26 standup says "I'll build on Luiza's brand profiles to add the form templates for ESA and Four Seasons": https://canarytechnologies.slack.com/archives/CQKD0PB63/p1790370370381739?thread_ts=1790369101.334729&cid=CQKD0PB63 . SDM-4996 itself says "Don't start solo". Its blocker text is also stale: the Configuration Drift Detection project is no longer Paused, it is in Implementation, labelled 26Q4A, target 2026-10-31, lead Tincho (https://linear.app/canary-technologies/project/configuration-drift-detection-364d47914acc).
  3. Explanations reach two places, not one. `explanation=` exists only on tree `define()`. It is read at `services/drift.py:194` (drift log) and `admin.py:240` (tooltip in the drift admin). Consistency rules have no explanation at all: `ConfigurationConsistencyError(keys, message)` and the decorator takes only `keys=`. So every consistency surface lacks a "why", not only E001: `checks.py:29` (E001), `services/conformity.py:683` (finalize), `signals.py:72` and `:123` (admin save and go-live warnings), `services/hotel_config_health.py:162` and `config_health.html:94`. Line numbers are from origin/master. ENT-7103 (https://linear.app/canary-technologies/issue/ENT-7103) shipped the define side only.
  4. The binding doc does not cover payment-gateway capabilities. It names `pms`, `capabilities_present`, `capabilities_absent` and `Authority.PMS_CAPABILITY`, all PMS. The word "gateway" appears only as "PMS Gateway". So the doc hosts the ENT-6097 Part 2 rule (PMS lacks `post_deposit_token`) as written, but "gateway can't do auth-only" needs a gateway dimension the design has not got yet, and possibly its own authority. Also `binding/pms/` is listed as "Later", after releases 1 to 3, and depends on Asher's PMS capabilities design. The draft says both plainly so SDM does not read it as "coming soon".

  Also: Joshua and Luiza are BOTH already in the doc's Reviewers property, so the ask is a nudge, not an invitation. I found no Slack message from you to either of them about the doc (you sent it to Asher, Blake, Andrea, #project-step-configurator and #epd-emea-engineers on 9/24 and 9/25).

  ### Verified as stated in the notes

  - SDM-5039 Done 9/21, SDM-4991 Done 9/21, SDM-4862 Done 9/21 (https://linear.app/canary-technologies/issue/SDM-4862).
  - #56000 merged 2026-09-21, #55498 merged 2026-09-14, #55833 merged 2026-09-21.
  - `deposit_slot_required_for_pms` is on master in `authorization/configuration_rules/consistency_rules.py`.
  - ENT-7488 is still in Triage with no comments (https://linear.app/canary-technologies/issue/ENT-7488).
  - Milestone "Brand profiles for top enterprise configs" is 18.75%. Its target date was 2026-09-03. SDM-4863/4994/4995 In Review, SDM-4996 Backlog (https://linear.app/canary-technologies/issue/SDM-4996).
  - Binding Rules Tree doc status IN REVIEW, last edited 2026-09-25: https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09
  - ENT-7614 PR #57673 is open, approved by Tincho 9/25 (https://github.com/canary-technologies-corp/canary/pull/57673).
  - CODEOWNERS precedent for co-ownership exists: `/frontend/packages/schemaform/` lists pod-arrivals-departures and pod-sdm on one line.

  Not verified: the deposit-slot code reading (auto-post CC flag vs `pms_operations`). I took the notes' conclusion as given and did not re-read that path.

  ### Decisions only you can make

  - [REVIEWER + DAY]: my suggestion is Tincho. He leads the drift project, approved #57673 and wrote ENT-7103. Ask him before naming him. Andrea (abrad) is the alternative.
  - [SDM-4996 DATE]: I would not give a build date. Suggested wording is in the draft: offer a date for a design session instead, and ask what Joshua is about to build.

  ### Draft message (Slack group DM: Joshua Hart UH2GJM97X, Luiza Manhães U09RFN779EW)

  Hi Joshua, cc Luiza. Closing the loop on the rules-engine asks now that SDM-4862 is done. One thing we owe you first.

  *Waiting on us: the brand profile PRs.* #56838, #56836, #57051 and #57320 have Joshua's approval but still need a pod-enterprise review, and Luiza's ask on 9/24 got no reply. Sorry about that. My approval doesn't count for that gate, so [REVIEWER] will review the stack by [DAY]. Three of them also need A&D because `enterprise_four_seasons/` is theirs in CODEOWNERS.

  *1. ENT-7488, capabilities as settings keys.* I'd like to answer this a different way and reach the same outcome. "PMS lacks post_deposit_token, so no Canary deposits" and "gateway can't do auth-only" are both attribute to setting impossibilities. The Binding Rules Tree design gives those a home: `binding/pms/`, `authority=PMS_CAPABILITY`, scoped by `capabilities_absent`, under a root that matches every hotel. Those are the two gaps SDM-4991 recorded: no capability tree, and no tree at all for non-enterprise hotels. So capabilities become a matching dimension on `HotelAttributes`, not derived keys through `generate_setting_types`.
  https://app.notion.com/p/3e58146861518147b489e3fa8e8aef09

  Two caveats. The doc covers PMS capabilities only so far. Gateway capabilities have no stored representation and are not designed yet, and after Nexi the dimension has to come from whatever the runtime trusts, not the `CAPABILITIES` class-set. Second, `binding/pms/` lands after the first three releases and depends on the PMS capabilities design, so your admin-page check from #55833 stays the guard until then.

  *2. The split going forward.* Setting to setting rules stay consistency rules: deposit slot when posting is on, the fraud-flag pair. Attribute to setting rules become binding rules and get a boot check, drift, and later a `pre_save` refusal, on enterprise hotels too. That last step goes past the warn-only contract we agreed, so tell me if it worries you.

  *3. Explanations.* `explanation=` only exists on tree defines, and only the drift log and drift admin show it. Consistency errors carry a message and nothing else, so E001, the admin save warning and the config health page never show a why. It's a small standalone fix. Happy to take it, or it's yours if you'd rather.

  *4. Ownership.* I'd like pod-sdm as CODEOWNERS co-owner of `binding/pms/` with PMS Platform. You hold the incident evidence for those rules.

  *5. SDM-4996, template and named-config packages.* This is the one piece that still needs design from us. [I can't give a build date yet. I can do a design session the week of DATE.] Joshua, I saw you plan to add form templates for ESA and Four Seasons on top of Luiza's profiles. What shape are you thinking of? I'd rather we didn't build two.

  Deposit slot: Luiza's reading was right, nothing to add from me.

  Two asks. Are you happy for ENT-7488 to be answered by the binding tree plus a capabilities dimension? And you're both on the doc's reviewer list. The executive summary is enough, but Luiza, the gateway half is where your read would help most.

  ### Follow-ups this implies, none done

  - Comment on ENT-7488 with the outcome once Joshua and Luiza reply. It is in Triage on your team with no comments.
  - If they agree to item 4, the doc's "Layout and ownership" section and the CODEOWNERS row in Appendix A need pod-sdm added.
  - If gateway capabilities go into the binding tree, the doc needs a gateway dimension and a decision on whether `PMS_CAPABILITY` covers it.
  - SDM-4996 description is stale (Enterprise is unpaused). It is Joshua's ticket, so raise it, don't edit it.
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: message joshua re SDM rules-engine asks and the binding rules tree
updated: 2026-09-28 14:41:55.237911
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