---
area: null
completed_at: 2026-10-08 14:00:23.104342
contexts: []
created: 2026-10-07 20:12:32.657575
defer_until: null
due: null
energy: low
id: 2026-10-07T2012-review-ent-sync-transcript-ihg-nad-mobile
order: null
output: |
  ## Agent run 2026-10-08T12:20
  Reviewed Granola "Enterprise clients sync", 2026-10-07 20:03 (https://notes.granola.ai/d/59de57f7-c736-4d19-a35c-321aa616b73f). You were only half there ("I've just been semi-present"). Speaker labels are unreliable: one voice shows up as "Golden Gate" and another as plain "System audio".

  **What you owe**
  - Nothing firm. During the portfolio-switch discussion, someone (probably Marta, or the "Golden Gate" voice) said "Gareth, I might follow up with you just to get a little historical context" about the deactivate-MSA-hotel and portfolio-removal scripts. You offered to answer on the spot and they said they'd follow up. Expect a ping. They want the parent script to revert all brand- or portfolio-specific config when a hotel leaves, e.g. Wyndham to BW. Marta is sharing the related ticket.

  **IHG mobile app SDK flag (the "nad-mobile" part)**
  - Taylor: properties on IHG's mobile app SDK need different check-in messaging. Changing it by hand works for about 6 pilots but not for 50 to 150 hotels, and Canary has no flag to script against.
  - Caitlyn owns this. Today IHG decides who gets the app, and on Canary's side every property is enabled. She'll ask the team whether the app/non-app signal in the request headers can become a config value.
  - Code check: the signal is per request only. It's the `X-SDK-Platform` header (backend/canary/guest_experience/versioning.py:83; also read in check_out/views/guest/guest_auto_checkout.py:29-54). `CheckInMembershipGift.source` has a MOBILE_SDK choice. There's no per-hotel setting. One option is to infer "SDK-live" per hotel from observed X-SDK-Platform traffic, but a new hotel would get the wrong message until its first app guest showed up, so an explicit per-hotel attribute set by onboarding is probably cleaner. Caitlyn's call. Worth mentioning only if she asks.
  - Single-CTA prioritization: no update and not coming soon. Brian expects poor conversion.

  **Other items (owned by others, FYI)**
  - Malay language: a client needs it as a full hotel language, not just guest journey messages. Bigger project.
  - IHG upsells by brand plus welcome-amenity message changes (Taylor and Shanda), part of the quarterly update.
  - Turkey and France: blocked on the anonymization feature, due to deploy this week. Work starts now, with QA on the Turkey registration card once it ships. Turkey is prioritized for next week. Bora is back and taking country rollouts over from Seb.
  - HotelKey (ENT-6032 pilot): FreedomPay gateway is only set up in the base config step, which ran before the values existed. Taylor will rerun the base step for every HotelKey property. The Canadian property's Salesforce ID was the brand ID; resolved and closed.
  - Marriott certificate expires Friday (2026-10-09) with no reply on the thread yet. Taylor says they're in touch with the right people.
  - Kiosk config scripting is an urgent need: a new management group needs about 12 near-identical kiosks. The kiosk team pushes back ("white glove"). Plan: let the Marriott team own it, as the tipping team did.
  - Omni dashboards are rolling out; Connor wants feedback.

  No external writes made.

  ## Agent run 2026-10-08T12:45 (IHG Slack search for the mobile SDK flag)
  No Slack thread found where the flag question (which hotels are on the IHG app SDK, so the script can set their check-in message) is discussed. It looks like Taylor raised it on the call first. I searched #ihg, #ihg-q3-deployment, #temp-ihg-scripting, #project-ihg-pilot, #ihg-onboarding-checklist and #ihg-pulse, then all of Slack, for SDK, mobile app, check-in message and cohort.

  Nearest relevant threads:
  - #ihg, 2026-10-06, Airel's thread (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1791298381164539): Holiday Inn Express Hershey-Harrisburg has Kipsu "text the front desk" in the IHG app and won't switch until Canary is there. Caitlyn: the app rolls out "to the masses at the end of October", and this hotel could join "the first cohort of app go live". Chanda manages the text-the-front-desk list and can swap Kipsu for Canary. So IHG and Chanda keep hotel-level app lists; Canary doesn't.
  - #ihg, 2026-09-14, Caitlyn: SDK live at Kimpton Shane (Atlanta), the only SDK hotel so far, with expansion from mid-October once IHG takes the new SDK version.
  - #epd-mobile timeline (Caitlyn, 2026-09-15): IHG picked up the new SDK on Sept 22, with QA in their app over Sept 24 to 29.
  - #epd-mobile, 2026-09-30, your post: `has_check_in` and `has_check_in_mobile` vary independently, and you suggested a CheckInVersion-style flag. Eric noted the app checks `hasCheckInMobile != false`, so it defaults to on. That's related: it gates the in-app check-in button, not the message.

  Code: the closest existing per-hotel "SDK" flag is `Hotel.enable_push_notifications` (backend/canary/hotels/models/hotel.py:1421; help text "Enable push notifications for the hotel's mobile SDK guests."). Staff push already reuses it (your 2026-10-05 #epd-staff-ops message), so overloading it again for IHG check-in copy would be a mistake. A dedicated per-hotel attribute is still the clean answer.

  Suggested next step (not done): if you want this on record, a reply in #ihg or a DM to Caitlyn and Taylor pointing out that the cohort list already exists on IHG's and Chanda's side. Whatever flag the team adds could be set from that list in the onboarding script. Nothing sent.
project: null
source_id: null
tags: []
time_minutes: 5
title: review ent CS  sync transcript Granola, last night
updated: 2026-10-08 12:45:00.000000
waiting_on: null
waiting_since: null
working_on: false
---