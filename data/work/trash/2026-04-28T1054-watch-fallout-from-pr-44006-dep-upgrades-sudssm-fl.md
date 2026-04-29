---
area: null
contexts:
- computer
created: 2026-04-28 10:54:36.105656
defer_until: null
due: null
energy: low
id: 2026-04-28T1054-watch-fallout-from-pr-44006-dep-upgrades-sudssm-fl
order: null
project: null
source_id: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1777319641935439
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Watch fallout from PR #44006 dep upgrades (Sudssm flagged 2 prod issues)'
updated: 2026-04-28 11:07:27.960242
waiting_on: null
waiting_since: null
---

Sudarshan flagged in #eng-leads that 2 issues today were caused by the PR that upgraded a bunch of deps across infrastructure. Skim the upgraded deps and watch for related fallout in our area.

Sudssm: "the two issues we saw were on go-bridge and frontend-chat" — narrow focus there first.

PR #44006 by bpietraga (SEC-296), merged 2026-04-27 14:27 UTC, +712/-637 across 23 files. Highlights:
- `bandwidth-livekit-bridge`: Go 1.24 → 1.25 (most likely culprit for go-bridge regression)
- `frontend-chat`: Node 20.19.0 → 20.20.2 + pnpm overrides (handlebars, cross-spawn, socket.io-parser, path-to-regexp, minimatch, glob)
- `canary-django` / `canary-lambda`: bumped litellm (Critical), django, pillow, cairosvg, curl-cffi, langchain-core, pyjwt, lxml, ujson
- `pms-gateway`: django, pyjwt, lxml
- `routing-service`: django, cryptography 45→46, pyopenssl 25→26
- `credential-manager`: django, pyjwt
- `inference`: django, pillow

Slack thread: https://canarytechnologies.slack.com/archives/C02MVAEJD0Q/p1777319641935439
PR: https://github.com/canary-technologies-corp/canary/pull/44006