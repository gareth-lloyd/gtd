---
area: null
completed_at: 2026-09-30 13:23:39.944923
contexts:
- react
created: 2026-09-30 04:36:29.966799
defer_until: null
due: null
energy: medium
id: 2026-09-30T0436-follow-up-on-wyndham-ohip-payment-method-rejection
order: null
output: |
  ## Agent run 2026-09-30T13:30:00

  **Verdict: nothing for you to do right now. Andrés owns this end to end and Marta has taken the Wyndham escalation.**

  ### What the Slack post is
  Andrés' #wyndham post (https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790698030424569) is step 1 of the plan in ENT-7627 (https://linear.app/canary-technologies/issue/ENT-7627): ask Wyndham corporate to turn on Chip and PIN (ChipPinYN=Y) on VI/MC/AX/DS at pilot hotel 11675, watch Groundcover, then roll to the other hotels. Marta Ziaei replied 2 minutes later: "I'll reach out to the Wyndham corporate team about this and keep you posted." ENT-7627 and its parent ENT-7033 were moved to Blocked (waiting on Wyndham) on 2026-09-29.

  ### State of the work since your July hand-off (all Andrés, 2026-09-24 onward)
  - ENT-5610 (https://linear.app/canary-technologies/issue/ENT-5610) is Done. Andrés ran a fleet-wide LOV audit of all 1,737 Wyndham OHIP hotels and posted a clear write-up on ENT-5610 (2026-09-24): two buckets, (1) wrong code in our payment_methods map, (2) chip flags off in Opera (338 hotels, whole chain codes e.g. WHRLT3, WHRMP66, WHRFEM1). Andrea Bradshaw asked for child tickets; he created three.
  - ENT-7625 Done (https://linear.app/canary-technologies/issue/ENT-7625): 13 hotels remapped by hand in gateway admin. Includes the 55903 VI->VA and 54703 VA->VI mismatches you found in July, plus 61089, 55979, 51889, 57120, 57404, 48658, 21563, 55666, 010400, 56478, 56525.
  - ENT-7626 Done (https://linear.app/canary-technologies/issue/ENT-7626): fleet-wide JCB JC->JB remap at ~1,347 hotels (your "default JCB: JC may be wrong estate-wide" hunch confirmed). Shipped via PR #57748 (audit command --commit mode, https://github.com/canary-technologies-corp/canary/pull/57748) and PR #57745 (onboarding default JB, merged 2026-09-24, https://github.com/canary-technologies-corp/canary/pull/57745).
  - ENT-7627 Blocked: the Wyndham escalation. CSV of 9 "every card fails" hotels (25-29 Sep, 175 failed pushes): 11675, 50471 (EU), 54064, 54076, 60287, 51295, 50659, 07838, 54067. The Slack CSV lists 8 because 07838 is "entry missing" (Visa mapped to VA which Opera lacks) and is a Canary-side fix, not a Wyndham ask.
  - ENT-7034 (GEN01242 cardType bucket, https://linear.app/canary-technologies/issue/ENT-7034) is still in Triage, unassigned. ENT-7627 scopes it out as "OPI-off configs failing with JSON Mapping Error (45997, 54703, 54730, 59230), a Canary config issue". Nobody owns it yet.

  ### New finding worth knowing (changes the mental model from July)
  ENT-7627 says ChipPinYN=N only rejects *tokenized* card pushes. Full card-number pushes pass with the same flag. Canary's payment setup at the hotel decides token vs card number. About 300 hotels have chip off but send card numbers and do not fail today. So the "chip off = broken" rule from the June/July LOV passes is too strong. Andrés also states the cause is "not confirmed": nobody has ever flipped Chip and PIN at a failing hotel, which is exactly why 11675 is a pilot before the bulk ask.

  ### Risk to watch
  Marta made the same offer on ENT-5610 on 2026-03-27 ("only need Site IDs") and it produced nothing for six months. This time she has Site IDs, hotel names, the setting name, the per-card list and a single pilot hotel, so the ask is concrete. Suggest a waiting-for on "Marta -> Wyndham corporate: Chip and PIN at 11675" with a check-in around 2026-10-07. Success signal per ENT-7627: no ODE09998 at 11675 for 7 days (Groundcover recipe in ENT-7033 comments / your memory note).

  ### Optional thread reply (NOT sent; drafted only)
  If you want to add anything, the only useful contribution is the ownership pointer and 07838 caveat:
  > Thanks both. Tracking ticket is ENT-7627 (pilot 11675, then the other 7). Note 07838 in the CSV is a Canary-side mapping fix, not a Wyndham ask, so 8 hotels for Wyndham. Marta, if Wyndham corporate needs the exact Opera setting: Payment Methods > VI/MC/AX/DS > "Chip and PIN" = Y (and AuthAtCheckinYN=Y).
  Andrés' post already says most of this, so skipping is fine.

  ### Not verified this run
  Prod gateway/Teleport MCP sessions were expired, so I did not re-run the LOV check or Groundcover counts. Numbers above come from Andrés' tickets and CSV.
project: null
source_id: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790698030424569?thread_ts=1790698030.424569&cid=C04STT7UPRQ
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: Follow up on Wyndham OHIP payment method rejections (Andrés)
updated: 2026-09-30 13:23:39.944909
waiting_on: null
waiting_since: null
working_on: false
---

Andrés in #wyndham: asks for help with Wyndham OHIP hotels where Opera rejects the guest's card at check-in with 'Payment Method is not valid'. Cases caused by our own configuration are already fixed. Related: ENT-5610.
https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1790698030424569?thread_ts=1790698030.424569&cid=C04STT7UPRQ