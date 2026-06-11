---
area: null
contexts: []
created: 2026-06-10 21:32:32.349431
defer_until: null
due: null
energy: low
id: 2026-06-10T2132-figure-out-this-ai-tools-thread-implications
order: null
output: |-
  ## Agent run 2026-06-11T14:00:00+03:00

  **What's happening:** Non-engineers across GTM/implementation have vibe-coded real
  internal apps with Claude, and the company is now formalizing a path to host them.
  Channel #tmp-internal-ai-apps (C0B4EPLJQD9), driven by Gurtej Gill (sponsor),
  Zivago Lee "Z" (platform), Stephanie Barry (product), Laura DeWald. The linked
  thread (https://canarytechnologies.slack.com/archives/C0B4EPLJQD9/p1779920236596699)
  is the operational step: apps get uploaded to a new GitHub repo for security
  review, then Z figures out hosting — Cloudflare Workers is the chosen platform.

  **The apps so far:**
  - *golive-checklist* (Mohsin Saeed, sales/implementation): product go-live checklist
    generator, shareable with customers behind per-checklist passwords. Static
    HTML + Cloudflare Worker (wrangler.toml present), currently on his PERSONAL
    Cloudflare account, with a Firebase DB tied to his Canary Google account for
    real-time sync. Was live at tools.thesaeed.com (pwd canary2026 — posted in channel!).
  - *Parakeet* (Baylee Magee, sales): full Next.js sales copilot — meeting prep,
    Q&A knowledge base, live in-call copilot (demo mode), post-meeting follow-up.
    Integrates Salesforce CRM, Gong transcripts, Notion, Google Calendar, VoyageAI
    embeddings, Claude. Was hosted on Railway (sales-copilot-production-70a4.up.railway.app).
  - *PMS Intelligence* (Gemma Hughes, EMEA SDR, joined 2026-06-10): FastAPI + Playwright
    scraper that detects which PMS/hotel-tech a property runs, for SDR prospecting.
    Dockerised, runs locally, asking whether Cloud Run or Cloudflare Workers.

  **How it's being done:**
  1. Intake questionnaire (Gurtej/Laura): what it does, what data it touches,
     third-party deps, pilot users, production-readiness.
  2. Upload into shared repo canary-technologies-corp/canary-apps-makerspace
     (https://github.com/canary-technologies-corp/canary-apps-makerspace), one
     directory per app (golive-checklist/, parakeet/). GitHub access via Okta now.
  3. Security review by engineering, then migrate hosting to Canary-owned
     Cloudflare Workers. Both app dirs already have .github/workflows files.
  4. Friction already visible: Parakeet "needs to be rewritten entirely" for
     Workers (Next.js/Node); Firebase dependency questioned by Z ("does it have
     to be firebase?" — answer: only for realtime sync, any WebSocket DB works).

  **Implications:**
  - This is sanctioned shadow-IT formalization: company apps with customer names,
    CRM data, and Gong transcripts have been running on personal Cloudflare,
    personal Firebase, and Railway. Getting them into the repo/review pipeline is
    the right move, but data exposure to date is unexamined (e.g. shared password
    in a Slack channel, Salesforce data flowing through Railway).
  - A repeatable "makerspace" platform path is being defined now — hosting,
    DB, auth, deploy model. Stephanie's open question is who owns updates so
    Platform/EPD doesn't become the bottleneck; Gurtej is positioned as gatekeeper
    for what graduates to production. Whatever defaults Z picks (Workers + ?DB +
    Okta/Google auth) will become the de facto standard for the growing queue
    (Gemma's app is #3; Stephanie says more are coming, incl. Jen's proposalbot).
  - Engineering touchpoints to expect: security reviews of vibe-coded apps,
    possible overlap with real product (Parakeet wants to reuse Voice AI
    backbone; go-live checklist overlaps Canary onboarding flow in admin —
    Stephanie already flagged convergence questions).
  - For Gareth specifically: nothing assigned to you, but a security review of
    the makerspace repo is the stated next step and no engineer reviewer has been
    named in-thread. The CF Workers constraint vs Next.js/FastAPI mismatch
    suggests the platform choice may need a second opinion.
project: null
source_id: null
tags: []
time_minutes: 5
title: figure out this ai tools thread implications. What is happening? how is it
  being done?
updated: 2026-06-11 13:54:22.704969
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0B4EPLJQD9/p1779920236596699