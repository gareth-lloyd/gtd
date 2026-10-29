---
area: null
completed_at: 2026-10-29 13:23:49.198269
contexts: []
created: 2026-10-28 15:41:45.688651
defer_until: 2026-10-29 09:00:00
due: null
energy: low
id: 2026-10-28T1541-things-for-my-attention-from
order: null
output: |-
  ## Agent run 2026-10-28T16:05

  Source: Enterprise CS/EPD Weekly Sync (https://app.notion.com/p/32e81468615180a9af7ad6342554c265). Whole page read (~81k chars, back to Mar 2026). Two blocks didn't render: a button and one embedded object.

  **The 10/28 section is still the empty template.** Nothing from today's sync is written down yet. The page was last edited 13:16 UTC, and Granola has no recording of it. Everything below comes from earlier weeks.

  ### Asked of you directly
  1. **10/07 Wyndham portfolio switches.** Andrea Bradshaw is to follow up with you for historical context. The question is whether `cut_parent_ties_script` is missing steps, given it's noted as "identical to deactivate_msa_hotel". Expect Andrea to come to you; you could get ahead of it.
  2. **09/30 IHG GDPR reg-card data retention.** Noted as "Sebastian, Martijn, James, Gareth should know this". We don't purge reg-card data today, and nobody clearly owns it. The France changes are on hold until we know we can purge. It would need a script change plus a rollout/backfill, and it also applies to Wyndham. The open question is who owns it.

  ### Scripting/config items in your area (no named owner, or someone else)
  3. **09/30 IHG HotelKey PMS config through onboarding values.** Ties to ENT-6032, the HotelKey+FreedomPay pilot.
     - The FreedomPay gateway was not created even though the onboarding values were there. Sharon fixed it by hand. Andrea or another person (ef49a0e1) was to add the ticket link.
     - PMS gateway config `is_enabled` is not being set. They want it on for HotelKey now and for Opera later.
     - If the hotel was previously on the arrivals list, the PMS configuration may fail silently.
     - 10/07 follow-up: a large batch of onboarding values was added.
  4. **10/07 Marriott.** They need a script for kiosk configuration country requirements. Build on the per-brand default and allow manual adjustments afterwards. This is driven by a 12-property management group that just signed. The certificate expired Friday 10/10.
  5. **09/30 IHG.**
     - Add Tablet Registration settings to the default permissions set (ticket to follow).
     - Tablet reg card config may also need to go into the scripts.
     - Ask IHG for updates to the default configuration and document their requests.
  6. **10/07 IHG Turkey/France.**
     - The anonymize feature was expected to deploy that week; still to be confirmed.
     - The Turkey/France script changes and QA can start once it's out.
     - QA help was requested for the Turkey reg card.
  7. **09/30 Wyndham script changes.**
     - Sending-domain mass update plus script update. Martin Rodriguez is on it and there are no blockers.
     - WAIC booking-link script also turned the link on for messages, not just voice. Needs fixing before the next batch: Slack thread https://canarytechnologies.slack.com/archives/C0AJ1ENFSSU/p1790703003314659
     - WAIC Digital Auths script changes are coming: two tiers, packaged and separate with auths opted out.

  ### Older, probably stale
  - ~07/01: "Connor to follow up with Gareth" on whether to replace the ICE portal.
  - 05/06: populate HotelKey onboarding values together with Taylor and Connor (the 25-site batch).
  - 04/15: you and another person (1fcd872b) to make sure messages are properly deactivated for Wyndham Connect Plus opt-outs.

  Nothing was posted or changed outside this file.
project: null
source_id: null
tags: []
time_minutes: 5
title: things for my attention from
updated: 2026-10-29 13:23:49.198264
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Enterprise-CS-EPD-Weekly-Sync-32e81468615180a9af7ad6342554c265?source=copy_link