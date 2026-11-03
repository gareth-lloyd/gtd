---
area: null
completed_at: 2026-10-30 15:13:15.906615
contexts:
- react
created: 2026-10-30 11:35:30.775784
defer_until: null
due: null
energy: medium
id: 2026-10-30T1135-reply-to-stephanie-re-resolution-agent-and-self-se
order: null
output: |-
  ## Agent run 2026-10-30T12:49:51Z

  Draft reply below. NOT sent. Destination: Stephanie DM, https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793312190746169

  ---
  Caught up on both, and I'm sorry I dropped just as you asked how this all fits together. Here's my answer.

  _Shared foundation:_ Both docs need the same thing first: hotels with correct settings, and settings a hotel can change from the product. That's another reason for one pod, because the first stretch of work pays off twice. The rules work is that foundation, but it's early. The first binding rules (EU ID collection, German retention cap) and the country conventions engine are still draft PRs, and Asher picks up PMS capabilities on top.

  _Biggest gap:_ Rules only warn today, and only on Django admin saves and the demo-to-live flip. Settings Assist doesn't check them, so it could save a combination we know is wrong. Once hotels set themselves up, legal and PMS rules need to block on every write path. I'd add that to "What has to be true first". I'd also gate by setting area rather than treat that list as one big prerequisite, because fixing every live hotel is open-ended. How-to answers and read-only diagnosis can ship before it.

  _Resolution agent:_
  • Settings Assist covers one of Support's top four causes: setting changes (19%). How-to (19%) and working-as-designed (13%) need the product facts source. Login (15%) can't be solved from inside Canary, so it needs an entry point before login.
  • Support marks 32% as needing an agent's judgment and 13% as needing a product fix, which leaves about 55%. If the target is 50% there's almost no slack, and 22% of requests are preventable upstream (go-live setup, proactive notices), so that part depends on onboarding.
  • Acting as the user is what makes Assist safe, but hotel users can't see logs or PMS state, so diagnosis needs a new trust boundary. I'd reuse Workup's engine rather than build a second diagnoser, but it isn't ready to face hotels directly: right action peaked around 57%, and the example in Laura's vision took 17 minutes and $5.72.
  • Support's Scenario B has Fin acting in Canary admin, which is the same front door as level 1. We should decide which one owns it.

  _Onboarding:_
  • The north star only counts a hotel if every step for every product can be self-served. Voice alone (three vendors, about 1.5 months) rules out any hotel that buys it, so the number could sit near zero while real progress happens. I'd lead with per-product activations. "Newly signed hotels" also leaves out cross-sell, which is about half of opportunities.
  • The add-product path needs early attention. In SDM-3520 it turned on ID verification with no provider, and guests hit a server error. That's a good case for one activation path.
  • Stage 4 defaults should build on the conventions engine, which writes country defaults at hotel creation, so we don't end up with two sources.

  _Evidence you can use:_ My settings field guide (not merged) covers 773 settings across 11 models. It records 828 dependencies between settings, and only 37 are enforced. It could feed product facts and diagnosis, and there's a review of 12 concrete cross-setting problems I can share.

  _Next:_ Yes please to bridging to Implementation. Can you add me to #project-agentic-resolutions and to the chat Sudarshan asked for next week? I'm also planning to shadow a CSA and will share what I learn.
  ---

  Check before sending:
  - The 50% resolution target comes from your own description to James. Neither doc states it (Stephanie's Oct 26 DM gives 50% for onboarding only), hence "if the target is 50%".
  - The 55% ceiling is my arithmetic: 744 self-serve + 497 preventable of 2,259 real requests, from https://pages.cnry.cloud/support-product-education/. The page text lists preventable sub-items flat; 744+497+298+720 = 2,259 is why I read them as sub-items.
  - The 57% comes from a garbled passage in your Laura 1-1 plus the Granola summary, which also notes a recent dip. Laura has the current number.
  - The 17 min and $5.72 are one example ticket (PMS-11192), from https://pages.cnry.cloud/workup-vision/.
  - Voice 1.5 months and the cross-sell split are directional figures from Stephanie's working notes, which say they aren't a measured baseline. Cross-sell is DJ's estimate.
  - "Settings Assist doesn't check rules" rests on no rules references in backend/canary/settings_agent and rules_based_configuration/signals.py being warn-only on admin saves and go-live. I did not trace each of the ~75 providers' native APIs, which have their own validation.
  - The 773, 828, 37 and SDM-3520 figures come from settings_field_guide/LANDSCAPE.md at commit 9501bfc4f19 (unpushed). 828 is mined from generated entries and covers the prototype scope only. I did not open SDM-3520 in Linear.
  - PR status checked today: #59047, #59059, #61725 and #61724 are all open drafts. Your memory note called #59047 and #59059 review-ready.
  - Decide whether you're happy to offer the field guide and landscape review; the draft commits you to sharing the review.
  - I couldn't find notes from after you left. Your recording has no call audio after that point, and I found no shared notes. Stephanie and Martijn were still talking, so the draft doesn't reflect anything said after you dropped.

  Sources:
  - Resolution flow: https://pages.cnry.cloud/resolution-flow/
  - Self-Service Onboarding: https://app.notion.com/p/98031c7f731a4cfcacfce21fd6fd804f
  - Working notes: https://app.notion.com/p/61c2fd33118c418cbd5bc050f8e6abf1
  - Support automation: https://pages.cnry.cloud/support-automation-takeaways/
  - Call note: https://notes.granola.ai/d/c726b958-6aac-4f7b-9e4f-de7ac95b4232
  - #project-agentic-resolutions: https://canarytechnologies.slack.com/archives/C0CCPSL66FN
  - Sudarshan's request to meet: posted in that channel on 2026-10-28

  ## Agent run 2026-10-30T12:52:08Z

  Revised after you pasted the rest of the call transcript. This draft replaces the one above. NOT sent. Destination: Stephanie DM, https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793312190746169

  ---
  Caught up on the rest of the call from the transcript. Thoughts on that and both docs:

  _Check-in V3 countries:_ Yes, I think this should end up in the rules system, and it's a good test case. Timing matters: Sam's country definitions (TOOL-872) merged this week with no countries filled in yet, and they include retention and purge settings. My draft PRs define EU ID collection and the German retention cap, so we're about to have two sources for the same values. I'd split it:
  • Legal requirements (retention, ID capture) go in binding rules.
  • Non-binding country defaults go in conventions.
  • Form fields stay with onboarding.
  I don't want this to block V3, so I'll talk to Sam about making Germany the first shared country. One catch: conventions are written at hotel creation, so existing hotels moving to V3 wouldn't get them that way.

  _Guardrails:_ Agree that Settings Assist shouldn't make changes that go against the rules, but today it can. Rules only warn, only on Django admin saves and the demo-to-live flip, and Assist doesn't check them. Once hotels set themselves up, legal and PMS rules need to block on every write path, so I'd add that to "What has to be true first". I'd also gate by setting area rather than treat that list as one big prerequisite, because fixing every live hotel is open-ended. How-to answers and read-only diagnosis can ship before it.

  _Existing hotels:_ Asher's idea looks like a good first slice for the Fix agent: Workup finds where a hotel breaks a rule, and the agent corrects it. Those cases are known wrong and easy to verify. Martijn's point about showing hotels why ("your retention is X because you're in the Netherlands") is also worth designing in, since the agent can explain it the same way.

  _Resolution agent:_
  • Settings Assist covers one of Support's top four causes: setting changes (19%). How-to (19%) and working-as-designed (13%) need the product facts source. Login (15%) can't be solved from inside Canary, so it needs an entry point before login.
  • Support marks 32% as needing an agent's judgment and 13% as needing a product fix, which leaves about 55%. If the target is 50% there's almost no slack, and 22% of requests are preventable upstream (go-live setup, proactive notices), so that part depends on onboarding.
  • Acting as the user is what makes Assist safe, but hotel users can't see logs or PMS state, so diagnosis needs a new trust boundary. I'd reuse Workup's engine rather than build a second diagnoser, but it isn't ready to face hotels directly: right action peaked around 57%, and the example in Laura's vision took 17 minutes and $5.72.
  • Support's Scenario B has Fin acting in Canary admin, which is the same front door as level 1. We should decide which one owns it.

  _Onboarding:_
  • The north star only counts a hotel if every step for every product can be self-served. Voice alone (three vendors, about 1.5 months) rules out any hotel that buys it, so the number could sit near zero while real progress happens. I'd lead with per-product activations. "Newly signed hotels" also leaves out cross-sell, which is about half of opportunities.
  • The add-product path needs early attention. In SDM-3520 it turned on ID verification with no provider, and guests hit a server error. That's a good case for one activation path.

  _Evidence you can use:_ My settings field guide (not merged) covers 773 settings across 11 models. It records 828 dependencies between settings, and only 37 are enforced. There's a review of 12 concrete cross-setting problems I can share. One bears directly on V3: moving a hotel drops five guest form settings without warning, including full birth name and mother's maiden name, which LATAM and Spanish hotels can require.

  _Next:_ Yes please to joining the Implementation conversations, starting with Kelsey. Can you add me to #project-agentic-resolutions and to the chat Sudarshan asked for next week? I'm also planning to shadow a CSA and will share what I learn.
  ---

  What changed from the first draft:
  - Added Stephanie's direct question from the call (should V3 country logic move into the rules system) as the lead.
  - The guardrails section now agrees with her, because she made that point on the call.
  - Added Asher's Workup-plus-agent idea, Martijn's visible-defaults point and Kelsey.
  - Dropped the "Shared foundation" section, the apology and the conventions bullet under Onboarding, all now covered by the V3 section.

  Check before sending:
  - New commitment: the draft says you'll talk to Sam about Germany as the first shared country. The Germany pick and the three-way split are my recommendation.
  - TOOL-872 is #61019 (commit 670914c911b, merged 2026-10-27). COUNTRY_REGISTRATION_CARD_PROVIDERS is empty on master at afd8338fce6. CountryDefinition.check_in_settings is commented as covering additional-guest, retention and purge settings. #61725 adds rules/law/id_collection.py and rules/law/retention.py. I did not compare the values or the exact keys.
  - The conventions catch reflects your 2026-10-27 decision that conventions are written at hotel creation. That write is not built yet (next PR after #61724). I did not check whether Sam's provider also runs when an existing hotel migrates to V3.
  - Asher's fix loop works for binding rules only, because #61724 keeps conventions out of conformity and drift.
  - The V3 finding is finding 5 in LANDSCAPE.md at 9501bfc4f19; I did not re-verify it at HEAD. AD-8414 (open) covers only the relation dropdown.
  - All "check before sending" items in the previous run still apply, except the one about having no notes from after you left, which this transcript resolves.
  - The pasted transcript is computer generated; names like "Sedarian" were read as Sudarshan.
project: null
source_id: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793312190746169
tags:
- morning-gtd
- slack
time_minutes: 20
title: 'Reply to Stephanie re: Resolution Agent and Self-Service Onboarding'
updated: 2026-10-30 15:13:15.906609
waiting_on: null
waiting_since: null
working_on: false
---

Stephanie shared the latest on both and asked for thoughts. I dropped from their call yesterday and said I'd catch up from the notes.
https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1793312190746169