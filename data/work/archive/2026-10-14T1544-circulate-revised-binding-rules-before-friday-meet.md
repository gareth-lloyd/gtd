---
area: null
completed_at: 2026-10-30 13:06:12.081265
contexts: []
created: 2026-10-14 15:44:29.679206
defer_until: null
due: 2026-10-29
energy: low
id: 2026-10-14T1544-circulate-revised-binding-rules-before-friday-meet
order: 1
output: |
  ## Agent run 2026-10-15T15:05
  Meeting: "Brainstorm use-cases for the binding rules engine", Fri 2026-10-16 15:45-16:15 Athens (https://www.google.com/calendar/event?eid=NmFvdmk5aDQ1MTJhZHJ2Y2RsajRjZmF2YXMgZ2xsb3lkQGNhbmFyeXRlY2hub2xvZ2llcy5jb20).
  Attendees: Martijn Dekker (mdekker, U0A3VFD5N1E, EMEA Lead Engineer) accepted; Asher Davidson (adavidson, U0AQVRJPHCL) DECLINED, out of office. So it's a 1:1 with Martijn unless you reschedule. Message still CCs Asher async because the PMS capability questions are his.
  Doc: https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09 (last edited 2026-10-15 11:51 UTC, status IN REVIEW).
  NOT SENT. Destination: group DM Martijn + Asher (or a DM to Martijn only if you drop Asher).

  --- draft ---
  Hi both, ahead of tomorrow's brainstorm I've revised the rules design doc: <https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09|Modeling laws, system capabilities and country conventions>

  What changed:
  • *Country conventions.* Besides the binding authorities (`LAW`, `PMS_CAPABILITY`, `PLATFORM`) there's now `CONVENTION`: a country default that applies only where the brand tree is silent. First example: German hotels default to `de` guest language. Independents finally get country defaults, written at creation by a new onboarding plan.
  • *Rules combine with AND, no tree.* Every matching binding rule must hold. An exception names the rule it replaces with `supersedes`. A brand value that breaks a rule fails boot.
  • *Predicates.* Rules (and brand defines) can say `OneOf`, `AtMost`, `SubsetOf`, `SupersetOf` etc., not just "equals X".

  For tomorrow I'd like to collect use cases beyond the first few (EU ID capture, German retention cap, German languages). Things worth thinking about:
  • Martijn: EMEA laws or country conventions you know of that aren't in the doc (registration, retention in other countries, invoicing, languages for AT/CH)?
  • Asher: I know you're out tomorrow, so async is fine. The "Later" section and the open questions table have the PMS capability questions: impossibility vs default, `capabilities_all` vs `capabilities_present`, dropping D23, and the "Spain requires ID but this PMS can't" case.

  Comments in the doc are welcome before or after.
  --- end draft ---

  Notes:
  - Retention open question in the doc is addressed to "Marta (EMEA-350)", not Martijn. Check that's the right person before tomorrow; if Martijn owns EMEA-350, add the retention question to his bullet.
  - I didn't check what the doc looked like before this revision, so "What changed" is inferred from the 2026-10-13/14 plan memory (conventions, SupersetOf, Binding->Rule rename). Edit if you revised something else.

  ## Agent run 2026-10-15T15:20 (reschedule)
  Done (you picked the slot in session): moved "Brainstorm use-cases for the binding rules engine" to Tue 2026-10-20 16:00-16:45 Athens (https://www.google.com/calendar/event?eid=NmFvdmk5aDQ1MTJhZHJ2Y2RsajRjZmF2YXMgZ2xsb3lkQGNhbmFyeXRlY2hub2xvZ2llcy5jb20) and added Diego Guzman (dguzman), AC Gantan (agantan) and Stephanie Barry (sbarry), as Martijn suggested (https://canarytechnologies.slack.com/archives/D0A2UR1AMD1/p1792066449127639). Invites sent to all. Everyone's response is reset to needsAction.
  Local times: 09:00 New York (Stephanie), 07:00 Belize (Diego), 21:00 Kuala Lumpur (AC), 16:00 Athens. No slot suits all three zones.
  Asher is out 16-27 Oct (back 28 Oct), so he's still on the invite but will miss it. The only slot with all six free was Thu 29 Oct 15:00 Athens.

  NOT SENT. Revised Slack draft. Destination: group DM with Martijn, Diego, AC, Stephanie and Asher.
  --- draft ---
  Hi all, I've moved the rules-based config brainstorm to *Tue 20 Oct* (16:00 Athens / 09:00 NY / 07:00 Belize / 21:00 KL, sorry, there's no slot that's kind to everyone) and added Diego, AC and Stephanie.

  The aim: collect use cases for a new part of rules-based config, rules that apply to every hotel whatever its brand. Laws (GDPR retention caps, EU ID capture), PMS limits, and country defaults (German hotels greet guests in German). Design doc: <https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09|Modeling laws, system capabilities and country conventions>. The executive summary is enough to skim beforehand.

  @Diego @AC: Martijn and I would most like to hear how customer ops use the current tooling today (config drift, onboarding settings, country-specific setup) and where it hurts. A couple of real examples would be gold.
  @Stephanie: the internal-tools angle. How these rules should show up in the configurator and in drift.
  @Asher: you're out, I know. Please leave async thoughts on the PMS capability open questions in the doc when you're back.
  --- end draft ---
  Note: the doc's retention open question is addressed to "Marta (EMEA-350)". That still needs checking.
  ## Agent run 2026-10-19T12:00 (non-technical draft for Tue)
  Meeting check (https://www.google.com/calendar/event?eid=NmFvdmk5aDQ1MTJhZHJ2Y2RsajRjZmF2YXMgZ2xsb3lkQGNhbmFyeXRlY2hub2xvZ2llcy5jb20): Tue 2026-10-20 16:00-16:45 Athens. Martijn accepted, AC accepted, Diego NOT YET RESPONDED, Asher declined (OOO), Stephanie DECLINED ("out of office"). Draft below treats Stephanie as async.
  Doc re-read (last edited 2026-10-16 09:38 UTC): https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09
  NOT SENT. Destination: group DM Martijn, Diego, AC, Stephanie (+ Asher optional).

  --- draft ---
  Hi all, here's a plain-English preview for tomorrow's brainstorm (Tue 20 Oct, 16:00 Athens / 09:00 NY / 07:00 Belize / 21:00 KL).

  *The problem.* Today our settings rules are written per brand. That works for brand preferences, but some rules don't depend on brand at all:
  • *Laws.* e.g. "In Germany, guest data can't be kept more than 455 days", or limits on how ID capture can be set up in the EU.
  • *System limits.* e.g. "If this hotel's PMS can't create memberships, membership push must be off."
  • *Country defaults.* e.g. "A German hotel should greet guests in German unless its brand says otherwise."
  Right now these only exist as copies inside each brand's setup, the copies sometimes disagree (IHG and Wyndham treat Italy differently), and independent hotels get none of them.

  *The idea.* Keep these rules in one place that applies to every hotel, branded or not:
  • Laws and system limits are *must-follow*. Brands can choose anything inside them, but nothing breaks them, and config drift flags any hotel that does.
  • Country defaults are *suggestions*. A new hotel gets them when its brand doesn't say otherwise; a brand can always override.
  • Every rule carries a short reason, so when drift flags a hotel it says which rule and why.

  *What I'd love from you tomorrow:* real examples. Things like:
  • Country-specific setup you do by hand today (languages, ID, registration, invoicing, retention)
  • Settings that are "illegal" or "impossible" for some hotels and keep getting set anyway
  • Where config drift or onboarding settings are painful or noisy
  Rough notes are perfect, even one line each.

  @Stephanie @Asher: I know you're both out. If you get a moment afterwards, comments in the doc are very welcome. Stephanie, I'd especially value your take on how this should look in the configurator and in drift.

  The full design doc is here if you're curious, but it's engineering-heavy and you don't need to read it: <https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09|Modeling laws, system capabilities and country conventions>
  --- end draft ---

  Notes:
  - Stephanie is OOO tomorrow. You may want to reschedule again if her input matters live, or accept async.
  - Diego hasn't responded; worth a nudge in the same message if you want a confirmation.
  - Still open from earlier runs: the doc's retention question is addressed to "Marta (EMEA-350)". Not checked.
  ## Agent run 2026-10-19T14:00 (rescheduled to Thu)
  Done (you approved in session): moved the meeting to Thu 2026-10-22 16:00-16:45 Athens (https://www.google.com/calendar/event?eid=NmFvdmk5aDQ1MTJhZHJ2Y2RsajRjZmF2YXMgZ2xsb3lkQGNhbmFyeXRlY2hub2xvZ2llcy5jb20). Updated invites went out and every response reset to needsAction.
  Free/busy showed you, Martijn, AC, Diego and Stephanie all free. Stephanie was out only on Tue 20 Oct. Asher is out until 28 Oct and will still miss it.
  Local times: 09:00 New York, 07:00 Belize, 21:00 Kuala Lumpur.
  Slack draft from the 2026-10-19T12:00 run, with these changes:
  - Opening line: "...preview for Thursday's brainstorm (Thu 22 Oct, 16:00 Athens / 09:00 NY / 07:00 Belize / 21:00 KL). I've moved it from Tuesday so Stephanie can join."
  - "What I'd love from you tomorrow" -> "What I'd love from you on Thursday".
  - Async line becomes "@Asher: I know you're out. If you get a moment afterwards, comments in the doc are very welcome." Move Stephanie's configurator/drift ask into the examples list: "Stephanie: how this should show up in the configurator and in drift".
  Still NOT SENT.
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 5
title: Write an overview of the rules system. to present in meeting.
updated: 2026-10-30 13:06:12.081241
waiting_on: null
waiting_since: null
working_on: false
---

draft slack message to attendees of meeting tomorrow. Non-technical overview for CS and STephanie.

https://app.notion.com/p/canarytechnologies/Modeling-laws-system-capabilities-and-country-conventions-in-rules-based-configuration-3e58146861518147b489e3fa8e8aef09?source=copy_link#4e6b5e4efec34807a0ff47f89d6630e3