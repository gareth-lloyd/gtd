---
area: null
completed_at: null
contexts: []
created: 2026-10-14 19:15:50.828978
defer_until: null
due: null
energy: low
id: 2026-10-14T1915-look-at-accor-doc-in-my-inbox-what-is-it
order: null
output: |
  ## Agent run 2026-10-14T19:25
  **What it is:** a Google Docs comment notification (not an attachment). Diana Perez tagged you on a comment thread in the slide deck
  "2026.10 | Accor Mobile Keys Workshop" (https://docs.google.com/presentation/d/1DDwwM89FDgDSkBgNtlfs-OVbXJPQgPme7iJRjtQgQ18/edit?disco=AAACGqid614).
  Email (unread, starred): https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879025017160912033

  **The deck:** Canary's pitch and working-session deck for the Accor Digital Key (NFC wallet key) workshop held today, Oct 14.
  It covers the Canary overview, key distribution flows (when/where/what, loyalty-tier messaging, QR fallback), the staff dashboard,
  the pilot timeline (5 properties, first pilot hotel call Oct 15/16), and appendix architecture (ALL app SDK, Apple Wallet CM/CP roles,
  ASSA/Vostio vs Dormakaba/LEGIC paths).

  **The ask to you:** the thread is on the "Questions for Accor" slide, which now sits in the Graveyard section (Rich Warner proposed cutting it).
  - Jean-Charles Lacoste asked: if Accor wants to handle the CRM side, do they expect Canary to send SMS and WhatsApp?
    Or can the channels be split, with Accor handling one and Canary the other? Is that technically supported?
  - Diana: "this is a question for the team handling communications, maybe @glloyd can help us channel this to the right team."
  - So they want you to **route the CRM and messaging-channel-split question to the right owner** (guest messaging / comms team). They are not asking you to answer it.

  **Context in the deck:**
  - Graveyard slide "Guest communication options": Canary recommends sending Accor's messages itself for the pilot. The alternative is Accor's CRM generating check-in links via Canary's API, with logic based on key status.
  - Graveyard slide "Provider routing" (WIP) poses the open question of how Accor's CRM knows which key provider (Canary vs e.g. Duve) to use.
    Options: a PMS flag, a per-property CRM setting, or Canary exposing key status by API.
  - There is a **CRM technical call on Tue Oct 27**. The App/SDK and online check-in calls are Mon Oct 26. The answer is needed before then.

  **Suggested next action (yours):** reply on the comment thread naming the owner of guest messaging/CRM integration
  (I did not guess who that is). Or reply that it belongs on the Oct 27 CRM call agenda. Nothing was posted. No external writes were made.

  ## Agent run 2026-10-14T19:50: Slack/Notion research + draft comment
  **Opinion:** the channel split isn't a pilot question. In today's workshop Slack thread, Vibhor and JC agreed the pilot uses Canary's comms
  (https://canarytechnologies.slack.com/archives/C0BU61U4Q1E/p1791985635401259).
  A split is technically possible in a narrow sense, but it's a poor default. It belongs to a post-pilot CRM track that builds on PA-986, which Physical Access has already scoped.

  Evidence:
  - Accor's CRM is mostly email. SMS and WhatsApp are barely used (SMS is being tested for OCI invites). Accor also runs Duve
    (https://canarytechnologies.slack.com/archives/C0AHEMNMWMN/p1791374180392559).
  - PA-986 "Expose Key Status to Accor's CRM" (Physical Access, Done) is the main finding: https://app.notion.com/p/3f281468615181289065d86f152ef7af
    - It scopes two options: a pull Key Status Link API (8-12 days) or push webhooks (11.5-18 days). Canary has no customer webhook system today.
    - Both options include a per-hotel "delivery-owner" flag that turns off Canary's DOWNLOAD_MOBILE_KEY message and check-in key notifications, so guests don't get duplicates.
    - Its open questions for Accor include "should Canary stop sending its own key messages?", which is effectively JC's question.
  - Channel config:
    - Guest journey messages can be toggled per channel. IHG, for example, runs some messages email-only, some SMS-only, and has WhatsApp off
      (https://canarytechnologies.slack.com/archives/C0B1MN8F869/p1787603683099099).
    - Default outbound channels are set per hotel: https://app.notion.com/p/28181468615180728933e713b71d5242
    - Catch: the automatic "mobile key created" message is hard-coded and outside journey-message config
      (https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1787233076316649).
    - The PA-986 delivery-owner flag is all-or-nothing per hotel, not per channel.
    - So "Canary sends WhatsApp, Accor sends SMS" means turning Canary's SMS off at hotel level. That loses Canary's SMS fallback and would need checking for the key message.
  - Precedent:
    - Best Western embedded Canary check-in links in its own emails, then switched to Canary-sent emails and saw "a big jump" in effectiveness
      (https://canarytechnologies.slack.com/archives/C0BU61U4Q1E/p1791990643063699).
    - IHG's version hit the multi-region problem with the legacy API (https://canarytechnologies.slack.com/archives/C0BET8YEKB4/p1787584570877399).
    - The Opal Upsells Link API already has a per-hotel switch for Canary vs brand sends: https://app.notion.com/p/3a78146861518049965cfc578b38a7bd
  - Owners:
    - Messaging pod: PM Rachel Kim (Jake Wilhelm is also listed as Messaging PM in Slack), eng lead Matías Marcó del Pont, #epd-messaging / #epd-communications-core
      (https://app.notion.com/p/16a81468615180d9872bd2d683839528).
    - Physical Access: PM Mehul Parekh (already on the thread), #epd-physical-access (https://app.notion.com/p/28281468615180c9927cd9960a30adfb).
    - The eng lead for Physical Access is unclear: Notion says Jordan Sterling, Slack profiles say Dana Levine, and Slack also puts Jordan on the public API in #eng-identity. Check before tagging.
  - Gaps: nothing found on how Accor's CRM picks Canary vs Duve per booking (the "provider routing" slide). PA-986 asks Accor whether its CRM holds the CRS or PMS confirmation id.

  **Draft reply** (NOT posted; reply on https://docs.google.com/presentation/d/1DDwwM89FDgDSkBgNtlfs-OVbXJPQgPme7iJRjtQgQ18/edit?disco=AAACGqid614 ; swap names for @mentions):

  > Thanks Diana. Routing below, plus my take so we go into the Oct 27 CRM call with a position.
  >
  > Short version: for the pilot, Canary sends on every channel (which I understand is already the plan). A channel split should be a post-pilot CRM decision, not a default.
  >
  > - Is a split technically possible? Partly. Journey messages can be switched on or off per channel, but the "mobile key ready" message sits outside that config. The switch for "Accor's CRM sends the key link instead of Canary" (scoped in PA-986) is all-or-nothing per hotel, not per channel. So "Canary does WhatsApp, Accor does SMS" means turning Canary's SMS off at those hotels and losing our SMS fallback. It's doable, but needs confirming, and it's fiddly.
  > - Best Western is the precedent: they embedded our links in their own emails, then moved to Canary-sent emails and conversion went up noticeably. That's a good argument for keeping the key message with us.
  > - If Accor's CRM does want to send, Physical Access has already scoped it in PA-986: a key-status link API or webhooks, plus a per-hotel flag to stop Canary sending duplicates. The open questions there (which CRM platform, CRS vs PMS confirmation id, does Canary stop sending) are the Oct 27 agenda.
  >
  > Owners: Mehul Parekh (Physical Access) for the key and CRM integration side, and Rachel Kim (Messaging) for the SMS/WhatsApp channel behaviour. I'd invite Rachel or someone from Messaging to the Oct 27 call.
project: null
source_id: null
tags: []
time_minutes: 5
title: look at accor doc in my gmail inbox. what is it?
updated: 2026-10-14 19:50:00
waiting_on: null
waiting_since: null
working_on: false
---