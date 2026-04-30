---
area: null
contexts:
- computer
created: 2026-04-29 09:56:28.125429
defer_until: null
due: null
energy: medium
id: 2026-04-29T0956-reply-to-asher-in-epd-internal-tools-review-tool-1
order: null
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1777393154544039?thread_ts=1776461807.622889&cid=C0AMJPBUH60
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Reply to Asher in #epd-internal-tools: review TOOL-121 AI branding eng design'
updated: 2026-04-30 07:07:39.848614
waiting_on: null
waiting_since: null
---

Asher @s me + Laura on eng design doc (used Claude to write). I'd promised to review this evening when I posted I'd been under the weather. Notion doc: https://www.notion.so/canarytechnologies/Using-AI-to-update-hotel-branding-3448146861518002a687c41b5ad845cf
https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1777498971902099?thread_ts=1776461807.622889&cid=C0AMJPBUH60

Long branding-tools thread (TOOL-95/TOOL-121). I parked it saying I'd review when feeling better. Asher started an eng design doc. Laura suggested ChatGPT/Claude plugin angle. Asher pushed back, wants in-product UI. Need my take on direction + design doc.
https://canarytechnologies.slack.com/archives/C0AMJPBUH60/p1777393154544039?thread_ts=1776461807.622889&cid=C0AMJPBUH60

  Current state
  - ~250 demos/year, mostly on Statler. ~5/month are custom-themed for high-value (6-figure) prospects.
  - Branding/theming a custom demo takes ~1 hour. Voice setup (new Twilio number + admin wiring) is the worst part — manual ticket, takes days.
  - Mohsin would do custom demos for mid-value (5-figure) prospects too if it were faster.

  Asher's proposed direction
  1. Improve demo creation tool + auto-acquire Twilio numbers (rejects the "django graph parser" option as too brittle).
  2. Speed up custom theming via AI URL extractor + a chrome extension/embedded sub-page for picking colors/fonts/images.

  Discussion (your inputs)
  - You pushed to decouple the problems (voice config, product config, branding, demo data) and to consider reusable brand configs.
  - Stephanie: branding tooling has value beyond demos — for all CSA branding setup.
  - They've narrowed the first project to AI branding extraction from a URL (Linear: TOOL-121). Internal-only behind a flag at first.

  Open debate (today)
  - Laura thinks AI branding is bigger than original scope, wants eng design doc, and questions whether the "1 hour" figure is real — pushed for a Loom from Mohsin.
  - Laura suggested a Claude/ChatGPT plugin instead of custom UI (lower lift, no UI to maintain). Asher pushed back: discoverability matters for non-technical users, and the tool
  also imports restaurants/amenities/hours/blurbs not just colors. He now claims ~90%+ accuracy (revised up from 50%).
  - Wenjun has an unreleased branding-page PR (#32729) being re-released by Wenjun + Connor.
  - Asher is starting an eng design doc. You said you'd review this evening (you've been under the weather).

  Action on you: review Asher's points + eng design doc when it lands. Laura's enterprise-vs-independent split question (CSAs on enterprise should already be using onboarding
  scripts) is worth weighing in on.