---
area: null
completed_at: null
contexts:
- react
created: 2026-11-10 11:04:30.569066
defer_until: null
due: null
energy: medium
id: 2026-11-10T1104-answer-belinda-in-epd-apac-engineers-q4b2-idea-on
order: null
output: |-
  ## Agent run 2026-11-10T14:24:29

  NOTHING SENT. Draft reply below; needs your "yes, send it" (or paste it yourself).

  ### What Belinda asked
  Thread: https://canarytechnologies.slack.com/archives/C0BJKKPLJAY/p1794297369753859?thread_ts=1793692804.937989&cid=C0BJKKPLJAY
  Her idea (09:49 EET today): "Maybe integrate with Rorror3 forms of thailand - IHG discussion", then a bare @-mention of you. No question text, so she wants your read on the IHG side.
  "Rorror3" = R.R.3 (ร.ร.3), the Thai Hotel Act guest registration card.
  I could NOT find the specific "IHG discussion" she means (no Slack, Granola or Notion hit). The draft asks her.

  ### Background found
  - Thai rules (Notion "Thailand: required fields", https://app.notion.com/p/3f281468615181649736f1f8d709185b): every guest goes on an R.R.3 card; R.R.4 register goes to the DOPA registrar weekly; every non-Thai guest is reported to Immigration (TM.30) within 24h. Page states "TM.30 and R.R.4 filing: Canary does not file them. The hotel's PMS or staff do."
  - Kempinski Siam precedent: tracker task marked Done 22 Jul, "no Canary TM30 integration is needed; the hotel handles the reporting via its existing Opera/export processes"; also notes there is "no official public API" for TM.30 (https://app.notion.com/p/3a4814686151819886f3d705963b7b6b). I did not verify the no-API claim independently.
  - Capture side is already built for Kempinski: the Nationality Fields step collects occupation, place of departure, next destination, date of entry (AD-10300, https://linear.app/canary-technologies/issue/AD-10300/siam-kempinski-bangkok-configurable-guest-details-step-by-nationality). Opera mapping for BKK1 (Jerome, 27 Oct): Occupation -> profile "Position", Place of Departure -> UDFC25, Next Destination -> UDFC26, Date of Entry -> UFDF5 (https://canarytechnologies.slack.com/archives/C0AV5BQM1JQ/p1793106152551429?thread_ts=1791824742.643799&cid=C0AV5BQM1JQ). These UDFs are per-property, not a standard.
  - IHG side: Thailand is on Taylor's top-10 country list by IHG property concentration (https://canarytechnologies.slack.com/archives/C0BSBH7BELE/p1788381889923049?thread_ts=1788302467.604549&cid=C0BSBH7BELE) and on the country readiness priority list (https://canarytechnologies.slack.com/archives/C0BSBH7BELE/p1790253462651079). 4 Thai IHG properties signed as of IHG Pulse 9 Nov (https://canarytechnologies.slack.com/archives/C0BSYBWSM6C/p1794256490879279). Vibhor flagged on 25 Sep that Thailand needs more discovery: occupation must go in the report to authorities and we need to know which UDF/profile field holds it (https://canarytechnologies.slack.com/archives/C0BJPFZKQ9W/p1790353195604809). Country setup guide: https://app.notion.com/p/3ea81468615181a382add4022b88ca68
  - Your 19 Oct APAC standup: Belinda's complaint that "nationality fields" is misnamed (these are fields required by the hotel's country, not the guest's nationality), and nationality must be able to come before ID scan.

  ### Draft reply (to post in the thread)
  > I think there's something here, but I'd split it into three sizes:
  > 1. *Capture + PMS writeback* (small): collect the R.R.3 extras (occupation, arriving from, next destination, date of entry) and write them to Opera. We already built the capture for Siam Kempinski (AD-10300). For IHG the missing piece is the mapping: Kempinski used property-specific UDFs, so we'd need IHG to tell us a standard field per item, or it stays manual per hotel. Vibhor flagged the same occupation-field question for IHG Thailand back in Sept.
  > 2. *Produce the R.R.3 card / R.R.4 register* (medium): generate the card and a weekly register export in the official layout from what we collect, so the hotel isn't re-keying. Feels like the best value for the effort.
  > 3. *File with the authorities for them* (TM.30 to Immigration, R.R.4 to DOPA) (large, uncertain): when we looked at this for Kempinski, the note was that there's no official public API, and the hotel handles it via Opera/export. I'd treat this as a discovery spike, not a build.
  > On the IHG angle: only 4 Thai IHG properties signed so far, but Thailand is in the top 10 countries by IHG footprint, so it matters for the rollout. Which IHG conversation did this come from, and were they asking us to do the filing itself or just the data capture? That decides whether it's #1/#2 or #3.

  ### Caveats
  - "4 signed" is from the pulse post; I did not check how many are live.
  - Sizes (small/medium/large) are my estimate, not scoped.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0BJKKPLJAY/p1794297369753859?thread_ts=1793692804.937989&cid=C0BJKKPLJAY
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Belinda in #epd-apac-engineers: Q4B2 idea on Thailand forms integration
  (IHG discussion)'
updated: 2026-11-12 12:45:07.472927
waiting_on: null
waiting_since: null
working_on: false
---

Belinda tagged me in the 'Q4B2 ideas hat' thread right after 'Maybe integrate with Rorror3 forms of thailand - IHG discussion'. She wants my input on the IHG angle. Open 0 days, no reply from me.
https://canarytechnologies.slack.com/archives/C0BJKKPLJAY/p1794297369753859?thread_ts=1793692804.937989&cid=C0BJKKPLJAY