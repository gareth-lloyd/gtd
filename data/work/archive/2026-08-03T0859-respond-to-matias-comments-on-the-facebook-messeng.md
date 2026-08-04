---
area: null
completed_at: 2026-08-03 14:39:21.017747
contexts:
- deep
created: 2026-08-03 08:59:34.732019
defer_until: null
due: null
energy: medium
id: 2026-08-03T0859-respond-to-matias-comments-on-the-facebook-messeng
order: null
output: "## Agent run 2026-08-03T13:11\n\n### Headline: the premise is inverted —
  Matías left no substantive comments\n\nDoc: \U0001F4AC Facebook Messenger Channel
  Integration\nhttps://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc (status WIP,
  owner Belinda Wang, teams APAC)\n\nThe quoted line \"I've left a few comments where
  we need more specifics\" is **your own**\ncomment from 2026-07-27, not Matías'.
  The Gmail notification subject was \"Matías Marcó del\nPont commented in…\", but
  Notion's email body renders the whole thread starting from the\nfirst comment —
  the GTD capture grabbed that opening text and attributed it to Matías.\n\nMatías
  Marcó del Pont's only comment on the doc, 2026-07-31 19:11 UTC, in full:\n\n    \"I'll
  review on monday if that's okay!\"\n\nIt replies to your 2026-07-31 comment: \"This
  document looks ready to my eyes. Just waiting\nfor final approval from CC pod -
  @Matías Marcó del Pont\".\nThread: https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=6e181468615182ab997583bb8689ec85&pvs=42\n\n**So
  there is nothing from Matías to respond to.** Today (Mon 2026-08-03) is the day
  he said\nhe'd review. The real action is a nudge, not a reply. Related Linear: APAC-53
  \"FB Messenger\nDesign Doc ratification\"\nhttps://linear.app/canary-technologies/issue/75793428-efda-474e-8cd2-01b63478e51d\n\n###
  What DID land since you last looked: 3 new comments from Sudarshan (2026-08-01)\n\nAll
  unresolved. These are for the author (Belinda) to answer, but two touch your review
  points.\n\n1. On **Out of scope** — \"what about receiving multimedia - images,
  etc? does twilio support\n   this out of the box?\"\n   https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3af81468615180c3b125001c4ddd548e&pvs=42#b7481468615182628b56813809ff74ab\n
  \  Codebase check: inbound Twilio media parsing already exists and is channel-agnostic
  form\n   parsing — `NumMedia` / `MediaContentType{i}` / `MediaUrl{i}` at\n   `backend/canary/chat/views/api_twilio_incoming_message_webhook.py:169-184`,
  downloaded into\n   `MessageAttachment` + `DocumentService` (same file, ~:150-163).
  But it lives inside the SMS\n   webhook view, not a shared helper — a new `FBMessengerWebhookView`
  must reuse\n   `get_messaging_context` and the download path rather than reimplement.
  Whether Twilio's\n   Meta beta channel actually populates those fields for Messenger
  inbound is a Twilio-side\n   question I did NOT verify (no sandbox, not in the docs
  I read). The doc's Goals only\n   promise *outbound* image attachments; inbound
  media is unstated. Genuine gap.\n\n2. On **narrow tagged exceptions** — \"what are
  the narrow exceptions? is there a 'utility\n   message' concept similar to whatsapp?\"\n
  \  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3af814686151808c95c1001c1b773df8&pvs=42#9e419f260ed3497ea8f51d8496210f11\n
  \  Not verified by me — this is Meta message-tag semantics (CONFIRMED_EVENT_UPDATE
  /\n   POST_PURCHASE_UPDATE / HUMAN_AGENT), and whether Twilio's beta channel exposes
  tags at all.\n   Worth the doc naming them explicitly since \"proactive outbound\"
  being impossible is a\n   load-bearing scope claim.\n\n3. On **messaging_outbound**
  — \"you'll also need a new model in\n   notifications/models/fb_messenger_notification.py,
  and associated links\"\n   https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3af81468615180528d01001c494fc5f2&pvs=42#3ac814686151803da8f9c1a5f55b69b3\n
  \  **Correct, and the doc has a real gap here.** Confirmed: `backend/canary/notifications/models/`\n
  \  holds `sms_notification.py`, `whatsapp_notification.py`, `amb_notification.py`,\n
  \  `web_chat_notification.py`, `ota_notification.py`, `zingle_notification.py`.
  Line and WeChat\n   follow the same pattern but their models live in `messaging_integrations.models`\n
  \  (`WeChatNotification`), with `Message.wechat_notification` / `Message.line_notification`
  FKs\n   added by chat migrations 0184 and 0199. The doc mentions adding the\n   `fb_messenger_notification`
  *branch* to notification dispatch and `Message.get_channel_status`,\n   but its
  data-model section never lists the new notification model or the `Message` FK.\n
  \  Nuance worth adding to the reply: since FBM is scoped to\n   `messaging_integrations/services/fb_messenger/`,
  the Line/WeChat precedent\n   (`messaging_integrations.models`) is the better home
  than `notifications/models/`.\n\n### Full thread state (10 discussions, 0 resolved)\n\nYours,
  still unanswered by the author:\n- Page-level 7/27 — Twilio Flex known-issues implications
  (reply-quoting, forwarded messages)\n- \"I'd like more information on how pages
  are added\" 7/27 —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3aa81468615180878fff001c4f3cb7f4&pvs=42#e923e8246dc549e99bb5d4f2d108eb63\n
  \ (partially addressed — doc now describes the manual Twilio Console auth + CSM
  entering\n  `fb_page_id`; arguably resolvable)\n- Monitoring proposals / Groundcover
  monitors 7/27 —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3aa81468615180158b8a001c0ae484d0&pvs=42#3a781468615180adb60ed354307ddbb9\n
  \ (addressed — doc now has a 3-bullet Groundcover tracking list; resolvable)\n-
  Adminland vs Canary Admin terminology 7/30 —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3ad81468615180f58a64001c6b96c9ea&pvs=42#6b9991b6f85f4ffdad806b8d4c564a7e\n
  \ (doc still mixes the two — e.g. \"Vue Adminland\" and \"Django admin tools\" in
  the same UX\n  bullet; not yet fixed)\n- Webhook 200/500 semantics 7/30 —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3ad814686151808a9a49001c84518f2e&pvs=42#3ac81468615180f7b4d5c0f1bf6ae02d\n
  \ (doc text unchanged — still says \"always returns HTTP 200\"; your objection stands)\n-
  Sender detach→re-attach trap 7/30 —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3ad81468615180819f14001ce04826fb&pvs=42#3ac81468615180eb8991c293ce95a625\n
  \ (unaddressed; still a `TwilioFBMessengerSenderView` disconnect action in the doc)\n-
  25-Page-limit note 7/27 (informational, resolvable) —\n  https://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3aa81468615180bbbaaa001c24f00a90&pvs=42#35081468615183119c40017e6114895b\n\nNote
  the tension: on 7/31 you wrote \"This document looks ready to my eyes\" while three
  of\nyour own 7/30 threads (Adminland wording, always-200, sender detach) are still
  open and the\ndoc text is unchanged. Worth deciding whether those are blocking or
  trust-the-author.\n\n### Drafted, NOT posted — waiting on your go-ahead\n\n**Draft
  A — reply to Matías on the page-level thread** (destination:\nhttps://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=6e181468615182ab997583bb8689ec85&pvs=42):\n\n
  \   Monday now — no rush, but flagging that @Sudarshan Muralidhar left three new
  comments on\n    Aug 1 (inbound multimedia, Meta message tags, and a missing notification
  model) that are\n    worth reading alongside the doc. Happy to hold my \"looks ready\"
  until CC has weighed in.\n\n**Draft B — reply on Sudarshan's notification-model
  thread** (destination:\nhttps://app.notion.com/p/3a581468615180aaaed2c47b844e3bcc?d=3af81468615180528d01001c494fc5f2&pvs=42#3ac814686151803da8f9c1a5f55b69b3):\n\n
  \   Agreed, and this is missing from the data-model section. One refinement on placement:\n
  \   Line and WeChat keep their notification models in `messaging_integrations.models`\n
  \   (`WeChatNotification`), not `notifications/models/`, with the `Message.line_notification`\n
  \   / `Message.wechat_notification` FKs added in chat migrations 0199 and 0184.
  Since FBM\n    lives in `messaging_integrations/services/fb_messenger/`, following
  that precedent is\n    probably cleaner than `notifications/models/fb_messenger_notification.py`.
  Either way the\n    doc should list both the new model and the `Message` FK explicitly
  — the migration is a\n    separate PR.\n\nSay the word and I'll post either/both;
  I have not written anything to Notion, Linear, or Slack.\n\n### Not verified\n-
  Twilio Meta beta channel behaviour for inbound media and message tags (no sandbox
  access;\n  would need Twilio docs/support or the sender attached to a test Page).\n-
  Whether Matías has reviewed since 19:11 UTC on 7/31 — comment fetch at 13:11 on
  8/3 shows\n  nothing newer from him.\n"
project: null
source_id: https://mail.google.com/mail/u/0/#inbox/19fb996a2e352ccf
tags:
- morning-gtd
- gmail
time_minutes: 30
title: Respond to Matias' comments on the Facebook Messenger Channel Integration design
  doc
updated: 2026-08-03 14:39:21.017677
waiting_on: null
waiting_since: null
working_on: false
---

Notion comment 2026-07-31: "I've left a few comments where we need more specifics." Addressed to me on a design doc thread.
https://mail.google.com/mail/u/0/#inbox/19fb996a2e352ccf