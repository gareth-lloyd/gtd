---
area: null
completed_at: null
contexts:
- react
created: 2026-08-10 11:40:43.245843
defer_until: null
due: 2026-08-12
energy: low
id: 2026-08-10T1140-reply-to-stephanie-barry-re-ai-voice-configuration
order: 2
output: |
  ## Agent run 2026-08-14T07:20 (EEST)

  Read the doc, checked the blocker's live status, and pulled the EMEA-specific
  material you'd be replying with. **Nothing was posted** — draft below for you to
  edit and send.

  ### Where things stand
  You already acked on 7 Aug ("Thank you! Will review early next week"), so the
  outstanding action is the substantive EMEA feedback, not an acknowledgement.

  Doc: [(WIP) Automating AI Voice Configuration — Research](https://app.notion.com/p/canarytechnologies/Automating-AI-Voice-Configuration-Research-3ae81468615181758c2fd11954a21356)
  (Stephanie, dated 31 Jul). Her thesis: config is already scripted via
  `CONFIGURE_VOICE`; the bottleneck is a human kicking it off from a ticket; the
  prize is triggering it from Salesforce; the gate is CC-2893.

  ### Four things worth telling her (all verified)

  **1. CC-2893 has moved since she wrote the doc.** Her TL;DR says "Not started".
  It went Planning → **Ready** on 12 Aug, assigned to **Rick Schieck**, and it's in
  a cycle. Still 1 point and still **no priority set**, so her concern holds — but
  the ask is now "get it prioritised", not "get it started".
  [CC-2893](https://linear.app/canary-technologies/issue/CC-2893/enable-twilio-interim-setup-while-voice-is-using-a-main-subaccount)

  **2. "Default language is deterministic from country" is only true inside a
  20-language allowlist — and EMEA is where it breaks.** `LiveKitSupportedLanguage`
  (`backend/canary/voice/models/supported_language.py:48`) is a closed enum bounded
  by two vendor constraints: Deepgram "multi" must detect it *and* Cartesia must
  have a TTS voice. Current set: en, es, fr, de, pt, hi, ja, ru, nl, tr, it, ar, da,
  fi, sv, no, pl, ms, zh, zh-HK.

  Not there: Czech, Hungarian, Greek, Romanian, Hebrew, Ukrainian, Bulgarian,
  Croatian. Those are live EMEA accounts, not hypotheticals — **Kempinski Prague**
  (pilot property #3) and **Danubius/Ensana** (Hungary, signed, Sept pilot). If the
  SF-triggered flow derives language from country with no guard, it will silently
  mis-configure exactly the accounts EMEA is trying to land. The automation needs an
  explicit "country → unsupported language → fall back to English *and* raise a
  ticket" branch. Worth saying plainly that adding a language is a code change plus
  a vendor voice-ID selection (James's walkthrough of the Statler-Portugal Mandarin
  setup: [#epd-voice, 12 May](https://canarytechnologies.slack.com/archives/C07R45PP9AS/p1778598123674029)),
  so it can't be absorbed inside an onboarding script.

  **3. Her "deterministic pieces" list is missing the EU AI Act disclosure string —
  which is regulatory, not preference.** Nathan Higgins asked EMEA CS on 5 Aug to
  hand-edit every web chat and AI Voice opening message to say "AI assistant"
  ([#emea-cs](https://canarytechnologies.slack.com/archives/C099ES3HX8A/p1785920509185389)).
  Nathan also says Jonathan + the AI Voice team are already building it as an
  automated config item, "available in the next 2-3 weeks"
  ([reply](https://canarytechnologies.slack.com/archives/C099ES3HX8A/p1785962179519139)) —
  so there's a track to join up with rather than duplicate.

  The wrinkle that makes it *not* a boolean: Aksel found the Spanish rendering said
  "automated" rather than "artificial intelligence" and had to fix the wording by
  hand. So it's a reviewed string per locale, not a region flag — same shape as her
  multilingual-by-region item, and it belongs next to it.

  **4. There's a live Twilio Slack Connect channel for her open question on bundle
  end users.** #ext-canary-tech-twilio — Jonathan Kennell already used it in June to
  ask about a regulatory bundle for an AU demo number. Answer that came back: the
  bundle is mandatory **even for demo/non-production numbers**
  ([thread](https://canarytechnologies.slack.com/archives/C079SQR30Q4/p1781637941526729)).
  That's a useful data point in its own right for EMEA pilots, and the fastest route
  to her "can Canary be the registered end user, or must it be per-hotel?" question.

  ### Optional fifth point — supports her open question #5 (pre-flight checklist)
  Caller ID is a config flag that isn't in her runbook and can't come from Salesforce.
  Jonathan Kennell, 12 Aug: if a hotel's PBX doesn't preserve ANI, "supplies caller
  phone number" **must** be unchecked, or we flag the PBX for spam and block all
  their calls
  ([#product-questions](https://canarytechnologies.slack.com/archives/C01V4NYTQRH/p1786540453461179)).
  It's PBX-dependent, so it's genuinely manual — and it's the same failure class as
  CC-2893: a silent, config-ordering break that takes out live calls. Good ammunition
  for the per-property pre-flight checklist she's already wondering about.

  ### Your own framing (from Bear — your call whether to say it)
  Your notes from the James Saram conversation are blunt: Voice is **not GTM-ready
  for EU**, "feels like beta testing in EMEA", with feedback coming back from unhappy
  customers (Bear: "James saram"). If you want to set the frame, the honest version
  is: automating configuration is the right target, but in EMEA the binding constraint
  today is product readiness, not config throughput — automation makes a
  not-yet-ready product reach more properties faster. Your Stephanie 1-1 notes also
  list an **EU/UK GDPR ID-purge default** as a small single-decision build — that's
  another deterministic-by-region item for her list #2 (Bear: "Stephanie Barry 1-1").

  ---

  ## DRAFT REPLY — not sent, edit freely

  > Finally read this properly — it's really good. The framing that the config is
  > already scripted and the bottleneck is a human reading a ticket is exactly right,
  > and I hadn't seen anyone lay out the Twilio API surface like that before.
  >
  > Four things from the EMEA side:
  >
  > 1. CC-2893 has moved since you wrote this — it went to Ready on 12 Aug with Rick
  > Schieck assigned. Still no priority set though, so your point stands, it's just
  > "get it prioritised" now rather than "get it started".
  >
  > 2. On "default language is deterministic from country" — it is, but only inside a
  > 20-language allowlist that's bounded by Deepgram detection plus a Cartesia voice.
  > Czech, Hungarian, Greek and Romanian aren't in it, which is Kempinski Prague and
  > Danubius/Ensana. So the SF-triggered flow needs an explicit "unsupported language
  > → English + raise a ticket" branch, otherwise the automation will quietly
  > mis-configure exactly the accounts we're trying to land. Adding a language is a
  > code change plus picking a vendor voice, so it can't live inside the onboarding
  > script.
  >
  > 3. Your deterministic list is missing the EU AI Act disclosure string. Nathan has
  > EMEA CS hand-editing opening messages to say "AI assistant" right now, and says
  > Jonathan's team is 2-3 weeks from automating it as a config item — worth joining
  > up with that rather than building it twice. One catch: Aksel found the Spanish
  > version came out as "automated" instead of "artificial intelligence", so it's a
  > reviewed string per locale, not a region flag.
  >
  > 4. On your bundle end-user question — #ext-canary-tech-twilio is a Slack Connect
  > channel with our Twilio reps. Jonathan asked a bundle question there in June and
  > got a straight answer within a day. Also worth knowing from that thread: the
  > bundle is required even for demo numbers, which bites us on EMEA pilots.
  >
  > One more that might feed your pre-flight checklist question: caller ID. If a
  > hotel's PBX doesn't preserve ANI, "supplies caller phone number" has to be
  > unchecked or we flag the PBX as spam and block all their calls. Can't be derived
  > from Salesforce — it's per-PBX — and it's the same failure shape as CC-2893.
  >
  > Happy to walk any of this through if it's easier than Slack.

  ### Not verified / open
  - Didn't find the "EMEA Onboarding Automation session with James Saram, 29 Jul"
    that her doc cites as a source — not in Bear, not in Slack search. If you have
    notes from it (Granola?), they may add more.
  - Didn't check whether the language-fallback gap already has a ticket.
  - The Cartesia/Deepgram constraint is read from the enum's docstring; I did not
    confirm against current vendor coverage, which may have widened.
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1786116050284199
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Stephanie Barry re: AI Voice configuration research doc'
updated: 2026-08-14 07:22:40.000000
waiting_on: null
waiting_since: null
working_on: false
---

DM Aug 7: shared her personal aggregation doc on automating AI Voice configuration, specifically because I'm collecting EMEA feedback on it.
https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1786116050284199