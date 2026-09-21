---
area: null
completed_at: 2026-09-21 14:14:28.528399
contexts: []
created: 2026-09-14 16:11:17
defer_until: null
due: 2026-09-21
energy: low
id: 2026-09-14T1611-follow-ups-from-blake-directs-2026-09-14
order: null
output: |
  ## Signature question: context (researched 2026-09-21)
  **Bottom line:** Blake was right to push back. Immediate purge applies to ID images only. No source says signatures must be purged immediately, and the record points toward keeping them for the statutory register period.

  ### What supports immediate purge (ID images only)
  - Tanja, the lawyer who reviewed the ROPA, advises every hotel be set to purge ID images immediately after OCR. Said in the "GDPR country retention" Granola meeting, Sep 3: "what should be happening now is immediate purge on OCR."
  - The retention matrix has `ID_IMAGE_DAYS = 0` and marks ID copies as prohibited in France and Czech Republic. Its Method tab says the country retention figure does not cover ID photos or scans, which have their own column. https://docs.google.com/spreadsheets/d/1oItyp7d5keDcJjis1onPo0GmcjGbUEj3173Hqpr7A1A/edit
  - The matrix has no signature column at all.

  ### What the record says about signatures
  - Jul 14 "GDPR storage" meeting notes: ID images mostly do not need long-term retention, but "what likely needs retention: signature + the policies being signed (for legal context)". https://app.notion.com/p/39d8146861518063a7a8caf9247db64d
  - WIP PRD "GDPR storage of Reg cards + ID + signature" (V2, Aug 3): signature is a logbook field to keep where the law requires the register, e.g. Germany international 12 months. V1 proposed tagging signature as non-wipeable reg-card data. Open, unowned, last edited Aug 4. https://app.notion.com/p/39d81468615180fca1cfc7ff6ddd9fc3
  - Matrix, France row: "signed fiche kept 6 months from its creation on arrival". A signed register record is a retention duty, not a purge duty.
  - Jul 15 weekly sync follow-up listed James as owner of "continue reg card/signature retention" work.
  - Granola search across the GDPR meetings and EMEA standups, Aug to Sep: no discussion of signatures as sensitive data or of any signature purge rule.

  ### What the code does today
  - The sweep scrubs the signature entry inside the reg-card JSON, so it disappears from the reg card after the country retention period.
  - The signature image itself (`CheckIn.signature`, sensitive-media S3 bucket) is not tagged for obfuscation and survives the sweep. The legacy ID-image purge does not touch it either.
  - Sebastian asked on Sep 4 whether the signature had been reviewed. Marta replied it is "a bug/not handled yet. I will add it to our list." No Linear ticket found for it. https://canarytechnologies.slack.com/archives/C0B3EUYPRL4/p1788521088317839

  ### Suggested follow-ups
  - Tell Blake the correction: IDs immediate on legal advice; signatures follow the country retention period with the rest of the reg card.
  - Ask Marta whether the signature image gap is ticketed.
  - Ask Sebastian and James who owns the reg-card and signature retention PRD, and whether Tanja has been asked about signatures specifically. No record shows she has.
project: 2026-04-16T1210-unblock-team
source_id: 2026-09-01T1451-plan-discussion-for-blake-directs-gdpr-retention-p
tags:
- gdpr
- mobile
- blake
time_minutes: 5
title: Follow-ups from Blake directs 2026-09-14
updated: 2026-09-21 14:14:28.528393
waiting_on: null
waiting_since: null
working_on: false
---

- Cannot irreversibly wipe without warning.
    - Warning options:
        - notification
        - mimicking the obfuscation in the dashboard without it being real yet


## GDPR retention

- **Feed back to the GDPR group today:** Blake is firm that we cannot irreversibly wipe hotel data without warning. It has to be one of:
  1. Advance notification to every affected hotel, framed as "we're tightening our compliance posture to match governance in your area, here are the impacted changes", or
  2. Mimic the deletion in the dashboard before it is real (a warning/preview state).
  This overrides the Sep 3 "silent rollout, ToS and ROPA cover it" position. Blake will push SJ on the same point. Tell Sebastian, Martijn, James and Marta.
- **Find an owner for account notification.** Blake asked whether I'm running notification of accounts; I said no. He wants it done. Likely CS/CSM plus Sebastian; needs a name.
- **Get the legal context for immediate purge of signatures and IDs.** Blake pushed back that signature and ID are very different and "immediate" is a big step. I said I'm still getting the legal reasoning from Sebastian, Martijn and James. Chase it and bring it back to Blake.
- **Send Blake the retention matrix.** He said he'll review it so he's familiar with the per-country periods. Sheet: https://docs.google.com/spreadsheets/d/1oItyp7d5keDcJjis1onPo0GmcjGbUEj3173Hqpr7A1A/edit
- **Confirm the UI gate is staffed.** I told Blake and Ian the UI is a blocker on turning obfuscation on. EMEA-636 is Todo and unassigned. https://linear.app/canary-technologies/issue/EMEA-636/gdpr-hotel-dashboard-ui-check-in
- **Sequence confirmed:** low-volume customers with sign-off first, learn the sensitivity, then widen. Timescale I gave Blake: early October.
- **Follow-up:** did any of "warning options" change the scope or date? Blake said "let's do it" to the larger scope; check with the team what it costs.

## Mobile takeover

- **Talk to Diana about the code-review gap** as Jason stops reviewing mobile PRs. Expect some velocity dip, not the same as losing an IC.
- **Talk to Diana about managing Romy's performance.** Diana becomes his manager. Blake: Romy is not meeting the bar, in a holding pattern for now, last to be looked at hard given OpenKey staffing. If we transition, Diana needs a lot of support. Use it to build her performance-management model.
- **Caitlin:** conversation already scheduled. SJ is not in favour of her; Connor is, for the day-to-day coordination and App Store work. Blake is aware of all sides and doesn't rate her as super effective either. No action beyond the conversation and keeping an eye on it.
- **Staff App ownership:** get it written down that Mike is PM for Staff App. Mobile core owns Lattice/foundations. Blake wants consistency between guest and staff apps on fanout, offline support and eager updates, treated as platform concerns on iOS and Android.
- **Watch Mike's style.** Blake heard rumblings he's ruffled feathers on the PM side by coming in over-confident. Not serious yet. Monitor and feed back via Blake or directly.
- **Set up conversations with the mobile team members** once the announcement is out (Blake sending ~10:00 Eastern today).
- **Ping Andy and Blake on Slack** for the previous review packet.

## Admin

- **Performance reviews:** Blake will run 2 to 4 context conversations per direct. He is cancelling October and November 1:1s, and this week's 1:1 (tomorrow) is cancelled so he can reuse the slot.
- **EMEA/APAC PR review item:** Blake marked it done. Peter is doing well; go-direct-to-owners approach is working.

## Not mine, for awareness

- Ian owns the OHIP/Wyndham Oracle billing decision with Blake pushing SJ for a position in the next hour.
- PMS backfills: hiring stance unchanged, cautious until Wyndham voice, IHG Q4 and EMEA activations materialise. If someone else leaves the PMS pod, Blake would backfill.