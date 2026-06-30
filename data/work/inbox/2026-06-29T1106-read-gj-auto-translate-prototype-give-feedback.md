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
project: null
source_id: https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1782205770503279
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 10
title: Read GJ auto-translate prototype + give feedback
updated: 2026-06-29 15:05:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

James Saram shared the guest-journey auto-translate prototype; proposes scoping tightly to Option A for the starter project, later expanding to Option B + reg-card/compendium fields. https://canarytechnologies.slack.com/archives/C0AB9E7AE59/p1782205770503279