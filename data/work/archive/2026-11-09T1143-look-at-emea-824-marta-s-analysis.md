---
area: null
completed_at: 2026-11-10 12:46:34.166210
contexts: []
created: 2026-11-09 11:43:34.025995
defer_until: null
due: null
energy: low
id: 2026-11-09T1143-look-at-emea-824-marta-s-analysis
order: null
output: |
  ## Agent run 2026-11-09T11:44:41

  **EMEA-824** https://linear.app/canary-technologies/issue/EMEA-824 (Crystal Hotel Belgrade, EU hotel 4539, assignee Marta, In Progress, High). Marta's analysis is two comments on 6 Nov: a WIP 9-point findings list and a 4-point summary. Martijn replied 8 Nov: declutter the KB using his Notion "Knowledge Base Optimization Claude Skill" (https://app.notion.com/p/canarytechnologies/Knowledge-Base-Optimization-Claude-Skill-412814686151800ca35cd2736f27c6ee), and decide next steps at the Monday (10 Nov) daily.

  ### What Marta found (3 weeks of logs, 14 Oct to 6 Nov, 136 staff-sent messages, 19 Add-to-AI saves)
  - Headline: the AI is NOT ignoring the KB. A wrong fact caused a rewrite only once. The hotel's complaint is really KB pollution plus drafts that are correct but unhelpful.
  - KB is cluttered: contradictory entries (Wi-Fi SSID "HOTEL CRYSTAL" vs "CRYSTAL HOTEL"), single-guest/single-day entries, duplicates, blog/marketing pages from the website scan, and a half-filled PDF template that contradicts itself. Parking info spread over many overlapping entries so answers are inconsistent.
  - "Add to AI" missing: not a bug. 72% of staff messages had nothing storable, 18% were already in the KB, only 9% were new lasting facts and at least 7 of those were accepted. Logs do not record whether a suggestion was shown, so the remaining 5 are unknowable.
  - Real bug 1: "Add to AI" creates duplicate entries (10 of 19 saves, 8 identical in 3 seconds). Hotel is in "facts only" mode with a 20-result search cap and no dedupe, so duplicates crowd out real facts. Same thing James saw on OLIVER (bed size saved 3x in one minute).
  - Real bug 2: on send, the system swapped a KB check-in link for a click-tracking short link; the curator then suggested that tracking link as a KB entry and staff accepted it, overwriting the original. The original was itself a 404 for one expired reservation.
  - Curator prompt gap: it defines a lasting hotel fact but never tells the model to skip one-off situations, and nothing validates a suggestion before it is shown. 33 of 136 runs rephrased a one-off as a general fact.
  - Product issue A: AI offers paid early check-in / late check-out with no availability data; staff retract.
  - Product issue B (most common rewrite reason): AI drafts "I'll pass your request to the team" and staff, who are the team, rewrite to "we'll prepare it". Martijn's suggestion: in draft mode say "already taking care of it", in auto-reply mode escalate.
  - Product issue C: AI promises things it cannot back up (invoice-by-email example with no usable address and ambiguous invoice).
  - Tone rewrites: many, not a bug.

  ### My read
  - Solid, evidence-based, and it reframes the ticket correctly. The "AI doesn't learn" framing from the CSM is a mismatch with what the product does; James made the same point on EMEA-819 (https://linear.app/canary-technologies/issue/EMEA-819).
  - Ask #3 (same root cause as EMEA-819) is effectively yes but nobody has said so on the ticket: both are KB pollution + duplicate saves + expectation that drafts learn from edits. Worth stating explicitly so the two are handled together.
  - Ask #4 (named owner and date for switching off draft mode) is still open. Nothing in the analysis gives the CSM a timeline.
  - Engineering work hiding in here that should become MSG tickets rather than staying buried in an EMEA ticket:
    1. Dedupe on curator save and/or in facts-only search results (cheap, affects every hotel).
    2. Stop the curator from learning the click-tracking short link; it should see the pre-substitution text.
    3. Curator prompt: exclude one-off situations and single-guest offers; consider a validation pass.
    4. Log whether a suggestion was shown, so "Add to AI is missing" is answerable next time.
    5. Mode-aware "pass along" phrasing (Martijn's idea) is a product decision for Jerome/Jason.
  - Nothing I need to do unless I want to push for the MSG tickets or weigh in on the Monday daily.
project: null
source_id: null
tags: []
time_minutes: 5
title: look at emea-824 marta's analysis
updated: 2026-11-10 12:46:34.166203
waiting_on: null
waiting_since: null
working_on: false
---