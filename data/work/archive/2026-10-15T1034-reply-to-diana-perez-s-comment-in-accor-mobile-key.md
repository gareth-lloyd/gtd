---
area: null
completed_at: 2026-10-16 14:39:01.490625
contexts:
- react
created: 2026-10-15 10:34:12.767836
defer_until: null
due: 2026-10-15
energy: low
id: 2026-10-15T1034-reply-to-diana-perez-s-comment-in-accor-mobile-key
order: null
output: |
  ## Agent run 2026-10-15T10:58:07: merge
  Folded in `2026-10-14T1915-look-at-accor-doc-in-my-inbox-what-is-it` ("look at accor doc in my gmail inbox. what is it?"). It is now in data/work/trash/ and can be recovered from there.
  - Kept this item's title. The other title was a "find out what it is" question, and the research below answers it.
  - The other item had no body. Its notes were all in `output:` (two agent runs from 2026-10-14). They are copied verbatim below so nothing is lost.
  - Added to the body: the deck comment-thread link, the ask (route the question, don't answer it), and the Oct 27 CRM call deadline. All three come from that output.
  - Dropped as duplicate: the Gmail thread link, which is the same in both items.
  - Fields: the other item had no contexts or tags. Its time_minutes (5) was not used because this item already had 10.

  ### Folded-in output from 2026-10-14T1915-look-at-accor-doc-in-my-inbox-what-is-it
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

  ## Agent run 2026-10-16T11:28:40
  > Follow-up asked: "Give me a straightforward explanation of what this doc is"

  It's a Google Slides deck called "2026.10 | Accor Mobile Keys Workshop": https://docs.google.com/presentation/d/1DDwwM89FDgDSkBgNtlfs-OVbXJPQgPme7iJRjtQgQ18/edit
  Canary made it for a workshop with Accor on Oct 14. The workshop was about Canary providing digital room keys
  (NFC keys in the phone wallet, issued through the Accor ALL app) at Accor hotels, starting with a 5-hotel pilot.

  What's in it:
  - Who Canary is.
  - How guests would get their key: when it is sent, by which channel, different wording per loyalty tier, and a QR-code fallback.
  - What hotel staff would see in the Canary dashboard.
  - The pilot timeline (5 hotels; follow-up calls Oct 26 for app/SDK and check-in, Oct 27 for CRM).
  - An appendix on the technical setup: the ALL app SDK, Apple Wallet roles, and the two lock-vendor paths (ASSA/Vostio and Dormakaba/LEGIC).
  - A "Graveyard" section of slides cut from the presentation but kept for reference.

  Why you got an email: it wasn't the deck being shared with you. It was a comment notification.
  On one of the Graveyard slides ("Questions for Accor"), Jean-Charles Lacoste asked whether Accor's own CRM could send some guest messages
  (e.g. SMS) while Canary sends others (e.g. WhatsApp). Diana Perez replied that it's a question for the comms team and tagged you to point it
  to the right people. You don't need to read the deck; you only need to answer that one thread. A draft reply is in the earlier run above.
  No external writes made.


  ## Agent run 2026-10-16T11:45:00
  > Follow-up asked: "summarize the comment thread i'm tagged in, give context from doc"

  Thread text comes from the Oct 14 notification email (https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879025017160912033).
  The Drive API returned 54 comment threads on the deck but NOT this one (AAACGqid614). It may have been deleted with its slide, or the API may just be omitting it. Open the link to check it still exists before replying:
  https://docs.google.com/presentation/d/1DDwwM89FDgDSkBgNtlfs-OVbXJPQgPme7iJRjtQgQ18/edit?disco=AAACGqid614
  No later reply emails arrived.

  Thread, in order (on the "Questions for Accor" slide):
  1. Rich Warner (Oct 8) asked Mehul and JC what other questions to put on the slide.
  2. JC: Diana is drafting an SDK question. Also, if Accor does the CRM part, do they want Canary to do SMS and WhatsApp, and can channels even be split between Accor and Canary?
  3. Rich: suggested dropping the slide and covering these topics as the deck goes.
  4. JC asked Diana to fold a CRM question in with the SDK one: if Accor handles CRM, does Canary still run SMS/WhatsApp, or can channels be split (Accor one, Canary the other)? Is that technically supported?
  5. Diana (Oct 14): it's a question for the comms team, tagged Gareth to route it.
  Mehul was tagged twice and never answered in the thread.

  Context from the deck (current version):
  - "Questions for Accor" slide now has two questions: own messaging at brand/corporate level or per brand? Which channel and timing at each stage (booking, 2 days before, day of arrival, check-in)?
  - "Guest communication options" slide: Canary recommends sending Accor's messages itself for the pilot (no CRM work for Accor, faster go-live, SMS/WhatsApp/email). The alternative is Accor's CRM generating check-in links via Canary's API, with logic based on key status. Bryan Michalis commented "we should be pushing to send messages... emails are the only open question" (open comment).
  - "Provider routing: who sends the key?" (WIP): how Accor's CRM knows whether Canary or another provider (e.g. Duve) handles a booking. Options: a PMS flag, a per-property CRM setting, or Canary sharing key status by API.
  - "Three ways guests get their Digital Key": the recommended message timeline, any channel at each step. Accor can change timing, channel or message.
  - Timeline slide: CRM technical call Tue Oct 27.
  - Other relevant comments: Bryan wants a note that WeChat/LINE etc. are regional and cost extra; Rich says the channel slide shows flexibility, not a prescription; JC says Accor can let hotels control comms 100% if they want.

  Bottom line: the question is "who sends which messages, Accor's CRM or Canary, and can it be split by channel". The deck already leans toward Canary sending everything for the pilot, so the split matters for after the pilot and the Oct 27 CRM call.
  No external writes made.


  ## Agent run 2026-10-16T11:55:00
  > Gareth pasted the live thread text.
  Confirmed: the thread still exists and matches the email word for word. No replies since Diana's (Oct 14, 2:33 PM). Mehul still hasn't answered.
project: 2026-09-08-mobile
source_id: https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879025017160912033
tags:
- morning-gtd
- gmail
time_minutes: 10
title: Reply to Diana Perez's comment in Accor Mobile Keys Workshop doc
updated: 2026-10-16 14:39:01.490619
waiting_on: null
waiting_since: null
working_on: false
---

Diana @-mentioned me in a comment on '2026.10 | Accor Mobile Keys Workshop' (Questions for Accor).
https://mail.google.com/mail/?authuser=glloyd@canarytechnologies.com#all/thread-f:1879025017160912033

Comment thread on the slide deck: https://docs.google.com/presentation/d/1DDwwM89FDgDSkBgNtlfs-OVbXJPQgPme7iJRjtQgQ18/edit?disco=AAACGqid614

- The ask: route Jean-Charles Lacoste's CRM / SMS-vs-WhatsApp channel-split question to the right owner. They want routing, not an answer.
- Answer needed before the Accor CRM technical call on Tue Oct 27.
- Earlier research and a draft reply (not posted) are in `output:` (folded in from "look at accor doc in my gmail inbox. what is it?").