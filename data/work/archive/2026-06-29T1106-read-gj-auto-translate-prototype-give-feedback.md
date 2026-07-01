---
area: null
contexts:
- consume
created: 2026-06-29 11:06:24.578470
defer_until: null
due: null
energy: low
id: 2026-06-29T1106-read-gj-auto-translate-prototype-give-feedback
order: null
output: |
  ## Agent run 2026-06-29T15:05:00

  Read the prototype + the Linear design doc and formed feedback. Did NOT post
  anything to Slack/Linear — draft reply is below for you to send if you want.

  ### What was shared
  - Slack (James Saram, #C0AB9E7AE59):
    https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1782205770503279
    "scope tightly to Option A for this starter project; near-future expand to
    Option B + apply to Reg card fields and Compendium."
  - Prototype: https://gj-translation-v2.vercel.app/settings/guest-journey
  - Linear project "Auto-translate: GJ templates":
    https://linear.app/canary-technologies/project/auto-translate-gj-templates-e069adf00275
  - Eng design doc (Notion):
    https://app.notion.com/p/canarytechnologies/Auto-translate-GJ-template-messages-38881468615180aeac9ddd2e3b3b4c3f

  ### What the prototype actually shows
  Statler New York GJ editor across Pre-Arrival / Arrival / In-House / Departure /
  Post-Departure. Per-message language toggles (EN/ES/FR/DE/IT). The A/B/C
  variants are purely the EDITOR-TRIGGER UX — i.e. *when the translate chip fires*:
  - Option A — "Translate in-line": chip appears below the edited field, user
    clicks, translation applied; chip stays in editor.
  - Option B — "Translate in-line + on Save": same chip, plus re-runs on save.
  - Option C — "Translate upon Save": no in-line chip; only fires at save.

  ### My feedback (the substance)
  1. **Agree with scoping to Option A** as the trigger. It's the most intuitive
     and lowest-risk (user-initiated action button, no double-translation, no
     surprise LLM spend). Option B adds wasted/ambiguous double-translation; C
     loses immediacy. A is the right starter.

  2. **The Slack proposal conflates two independent axes** — worth untangling
     before it sets the roadmap:
       - Axis 1 = editor-trigger UX: Option A / B / C
       - Axis 2 = surfaces: GJ messages → Reg card → Compendium
     These are orthogonal. You can ship Option A on GJ now and later expand
     surfaces without ever needing Option B; or adopt B on GJ without touching
     surfaces. "Option A now, Option B + reg-card/compendium later" reads as if
     B and the new surfaces are one step — they aren't. Recommend stating the
     roadmap as two separate dimensions.

  3. **The A/B/C choice is the cheap part; it doesn't shrink the hard scope.**
     The genuinely hard, must-build-for-v1 work is all backend and independent
     of the trigger:
       - per-language storage of templates + hotel customisations
       - send-time language resolution from PMS/reservation language + English
         fallback when the guest's language isn't configured
       - placeholder / URL / SMS opt-out keyword preservation ({{ }}, links,
         QUIT) — the doc flags this; it's the highest-correctness-risk item and
         should get explicit tests, not just a prompt instruction
       - re-translation / override policy when English source changes
     Picking Option A doesn't de-risk any of these. Make sure "scope tightly"
     means the backend slice is also narrowed, not just the editor.

  4. **WhatsApp: cut it from the starter, spike the approval path in parallel.**
     There's real tension in the doc — WhatsApp is listed as a v1 target, but
     the eng flag (Twilio/Meta template re-approval on any translated body)
     realistically pushes it out. James's "must consider WhatsApp as fast-follow"
     is the right instinct; just make it explicit that the starter ships Email +
     SMS only, with the WhatsApp/Twilio re-approval feasibility spike running
     alongside (the CSAs' Claude-built approved-templates tool is a strong head
     start there). Don't let WhatsApp gate the starter.

  5. **Pin down re-translation/override policy now (open decision #1)** — it's the
     single thing that most drives editor scope. Recommend the cheapest viable
     rule for the starter: on an English-source edit, mark the other languages
     "needs review" (don't silently overwrite a human override). Avoid building a
     full staged-diff review UI for v1 — the doc already lands review inside the
     GJ editor via the language dropdown, which is the right minimal call.

  6. **Confirm "in-line / real-time" ≠ translate-on-keystroke.** The doc says it's
     an Action button (good — cost + jank), but the prototype copy says
     "real-time while editing." Worth a one-line clarification that it's
     user-triggered, not per-keystroke.

  7. Keep: per-segment translation scope, feature-flag rollout for CS/CSA
     feedback, and usage tracking from day one (all in the doc). Reg card +
     Compendium correctly out of scope for this project.

  ### Draft Slack reply (NOT sent — say the word and I'll post it)
  > Looks great. +1 on Option A as the starter trigger — most intuitive and
  > avoids the double-translate ambiguity of B. Two things worth separating in
  > the roadmap: the trigger UX (A/B/C) and the surfaces (GJ → reg card →
  > compendium) are independent axes — we can expand surfaces later without ever
  > needing Option B. And the A/B/C choice is the cheap part; the real v1 risk is
  > backend — per-language storage, send-time language resolution + EN fallback,
  > and especially preserving {{ placeholders }}/URLs/opt-out keywords. Suggest
  > the starter ships Email + SMS only and we run the WhatsApp/Twilio re-approval
  > spike in parallel rather than gating on it. Happy to dig in on the
  > re-translation/override policy (open decision #1) since it drives editor scope.

  ## Agent run 2026-07-01T11:34:00Z

  Re-read the Notion design doc fresh (it was last edited 2026-07-01T08:41,
  Status = IN REVIEW). **The doc has moved a lot since the 06-29 run — most of
  that feedback is now baked in.** Did NOT post anything. Updated draft below.

  Doc: https://app.notion.com/p/38881468615180aeac9ddd2e3b3b4c3f

  ### What the doc now resolves (prior feedback that's landed — don't re-raise)
  - **Option A** is committed; A/B/C moved to "Alternative solutions". (prior #1)
  - **Two axes untangled**: Compendium + Reg Card are explicitly in "Scope
    Creep"; trigger vs. surfaces no longer conflated. (prior #2)
  - **Backend hard scope is now spelled out**: translation service reusing
    `PromptGatewayService` (Google Translate fallback), guardrails that check
    merge-tag set match / URL + opt-out keyword preservation / email HTML /
    SMS length, per-language i18n fields, send-time selection by reservation
    language with English fallback. (prior #3 — largely addressed)
  - **WhatsApp cut from v1**: Email + SMS first; WhatsApp/Meta re-approval is a
    held-back follow-up spike, plus Expedia + Booking.com. (prior #4)
  - **"In-line" clarified**: button only appears when a field changes, click to
    translate — not per-keystroke. (prior #6)
  - v1 tickets exist: EMEA-394 (guardrails) → 395 (service) → 396 (endpoint) →
    397 (Option A button) + 398 (observability).

  ### NEW issues in the current draft (the substance for this pass)

  1. **Feature-flag contradiction — and dropping the flag is the risky call.**
     The Goals bullet still says it "ships behind a feature flag so we can pilot
     with a few properties before rolling out widely," but the rollout section
     AND the v1-scope line now say the opposite: "no feature flag… releasing it
     across the board once it's ready." These directly contradict — one has to
     go. More importantly, the doc's own #1 risk is "output may be off, and it
     goes live without review." Removing the flag removes the one blast-radius
     control for exactly that risk. I'd push back: keep at least a pilot flag or
     a kill switch. "Not guest-facing" is the justification given, but the
     *output* is 100% guest-facing (it's the message guests receive) — only the
     trigger is staff-side. This is the most important point.

  2. **Silent overwrite of hand-tuned translations — an unaddressed gap, not a
     documented trade-off.** What the doc states explicitly: "editing the English
     source brings the button back, and clicking it overwrites the stored
     translations for that field" (Goals), and "A 'needs review' or 'stale'
     workflow" is in Scope Creep. What it does NOT address: the overwrite is
     described as clobbering "the stored translations" with no distinction
     between machine-generated and human-edited content. Concrete failure: a CSM
     hand-corrects the Spanish body; later someone edits English and clicks
     Translate → the hand-tuned Spanish is silently overwritten, no warning. The
     doc never mentions this case — so it's a blind spot, not an acknowledged
     "acceptable for v1" call. (Correcting my own earlier phrasing: I first wrote
     this was an "explicitly accepted risk" — it isn't; the overwrite behavior is
     explicit, the human-override consequence is simply unmentioned.) Combined
     with #1 (no flag), both the quality risk and this data-loss path go live
     unguarded. Cheapest guard: only overwrite languages still machine-generated
     / unedited for that field.

  3. **Partial-language failure UX is unspecified.** Guardrails store per-language
     and "return an error for that language." So one click can yield ES+FR stored
     but DE failed. What does the button do then — stay, offering a retry for
     just the failed language(s)? The per-language partial-success state isn't
     described in the UI section and is worth pinning down before EMEA-397.

  4. Minor: Goals says translations "save immediately" while Proposed solution
     says the endpoint "runs asynchronously with a loading state." Not a
     contradiction (async completes → saved) but the wording could align.

  ### Updated draft comment (NOT posted — Notion comment or Slack reply)
  > Doc's in good shape — Option A, backend guardrails, WhatsApp-as-follow-up
  > all read well. Two things I'd resolve before build: (1) the feature-flag
  > decision contradicts itself — Goals says "pilot behind a flag," rollout says
  > "no flag, across the board." Given your own #1 risk is bad output going live
  > without review, I'd keep at least a pilot flag or kill switch; the trigger is
  > staff-side but the translated output is 100% guest-facing. (2) Overwriting
  > stored translations on re-translate will silently clobber any hand-tuned
  > language for that field — fine if that's an explicit v1 call, but worth
  > stating it, or only overwriting still-machine-generated languages. Minor:
  > spec the partial-failure UX when some languages pass guardrails and others
  > fail on the same click.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1782205770503279
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: Read GJ auto-translate prototype + give feedback
updated: 2026-07-01 15:07:15.246617
waiting_on: null
waiting_since: null
working_on: false
---

https://app.notion.com/p/canarytechnologies/Auto-translate-GJ-template-messages-38881468615180aeac9ddd2e3b3b4c3f