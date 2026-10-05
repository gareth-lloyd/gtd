---
area: null
completed_at: 2026-10-05 10:01:21.462472
contexts:
- consume
created: 2026-10-02 00:00:00
defer_until: null
due: null
energy: low
id: 2026-10-02T0000-review-this-week-s-eng-leads-recording
order: null
output: |
  ## Agent run 2026-10-05 09:48:09

  Eng Leads, Thu 2026-10-01 (52 min, ~30 invited). Run by Andy Monroe; Blake Vanlandingham co-leading. Transcript: /Users/garethlloyd/Downloads/GMT20261001-155929_Recording.transcript.vtt

  ### Things that touch Gareth directly
  - **Canary Energy check-ins (Blake, ~34:50).** After Terry's departure Blake asked every lead to ask ICs "what's your Canary Energy?" (1-10) consistently in 1:1s. Anything below 8 means dig in; flag high performers drifting below 7/8 to your manager (or Blake directly, he will loop the manager in). Doc lives in the 1:1 guidance in Notion. Blake said departures are the moment people "poke their heads up".
  - **Perf reviews (~23:30).** Sudarshan said 1.5 weeks for 9 reviews is too tight and suggested ~3 weeks. Andy: manager-review extensions are available, and early-open extensions are technically possible but unadvertised. Use an extension if needed.
  - **Holiday on-call + December code freeze (~44:20).** Blake confirmed another December code freeze. Z Lee and Alan Lee will drive the holiday on-call schedule ASAP: shifts split into ~3-day blocks across Thanksgiving and Christmas/New Year, each block counts as a full cycle (skip next rotation), and all days around the holidays get holiday on-call comp. Volume last year was very low (one security item). Plan team PTO against this.
  - **Wyndham Stripe COGS (Yasmin, ~13:30).** ~70% of Stripe cost sits in the Wyndham Elavon implementation. Blocked for months on internal alignment, not the customer. Logic lives in check-in and authorizations, not payments, with no cost attribution infra. Yasmin is briefing Connor (director of product, Wyndham owner). Stephen Reddekopp suggested Ani (enterprise CSM for Wyndham) can drive. Andy: re-raise next week if still stuck. Possible place for Gareth to offer enterprise/Wyndham context.
  - **Wallet rebuild (Yasmin, ~19:55).** Apple Pay / Google Pay implementation is legacy and needs a ground-up rebuild (no Google identity or partner registration, app review needed). Driven by digital tipping enterprise customers, with Taylor and Quinn as owners; also needed for F&B pilot and mobile. Backend, web and mobile pieces all in flight at once.

  ### Critical items / high-risk changes
  - Check-in V3 migration (Dana): going well, big ramp starting next week; stays on the list one or two more weeks. Dana to add estimated end date to the note. Ishwar following up separately.
  - RDS migration to main VPC (Aditya): complete as of 10-01. EKS and RDS now share a VPC with IPv6; removes the VPC peering and NAT64 black-hole workaround. Done almost entirely via agents watching Groundcover and Sentry. Blake asked for a show-and-tell on the process, tentatively next week.
  - Loom deprecation (Chris Carter): no new update, waiting on one more SOP before a wider announcement. Ian Clark's bulk download script works (Sudarshan pulled ~80 Looms).
  - Stephen: auto-scaling by call volume (with Aditya) is working; will bump the minimum for the rollout.

  ### People
  - Terry's last day was Fri 2026-10-03 (went to a smaller company, nothing Canary-specific). Left PRDs and designs for upcoming AK blocks. Val will spend ~half of next quarter on AK (self-healing AI loops). With Miguel and Cherry also gone, AK engineers will do more PRD/design work until more designers are hired. SJ is actively looking at retention.
  - Bernard Pietraga's last week (health reasons; open to returning). Handing a security questionnaire / investigation agent (built on Overlord) to Khush and Chris. Security (Z, Greg, Alina) triggers runs and manually reviews drafts with Groundcover links.
  - Proactive retention (Andrea Bradshaw's question): Blake wants to fix how equity value is communicated and get the Eng Retreat on the calendar; otherwise the stance is "fast reaction to signals" rather than new programs.

  ### Other
  - Eng Leads format stays as-is after Blake and Andy's review; DM them with further thoughts rather than group debate.
  - Friday demos: AI voice recovery after failed transfer, KB dupes/conflicts (Huddle); show and tell: RFP marketplace Chrome extension, web chat testing (Kelly), F&B payments (tentative), check-in V3 configurator (tentative), SQL tool.
  - Andy still owes a follow-up on Navid's side-fee email (not 4 weeks yet).
  - IT: new laptop sign-in banner is a reminder it's a Canary device; a handful of departed-employee laptops are unreturned.

  ### Suggested next actions for Gareth (none were assigned in the meeting)
  - Ask Canary Energy in each report's next 1:1 and read the 1:1 guidance doc.
  - Confirm holiday on-call availability with the team before Z and Alan publish the schedule.
  - Decide whether to offer Yasmin Wyndham/Elavon context or an Ani intro.
project: null
source_id: null
tags: []
time_minutes: 30
title: Review this week's Eng Leads recording
updated: 2026-10-05 10:01:21.462448
waiting_on: null
waiting_since: null
working_on: false
---

/Users/garethlloyd/Downloads/GMT20261001-155929_Recording.transcript.vtt