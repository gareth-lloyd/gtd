---
area: null
completed_at: null
contexts: []
created: &id001 2026-09-23 17:37:29.705942
defer_until: null
due: null
energy: null
id: 2026-09-23T1737-think-through-sdk-boundary-questions-from-mobile-b
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Think through SDK boundary questions from mobile block planning (Sep 23)
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

From the 2026-09-23 mobile block planning call. Sean asked whether there is an "origin edit" that stops the SDK always catching up to web. Questions to think about:

1. **Guest SDK: headless core first?** Should custom views become the public surface of a headless flow core, with the standard UI and flavors as one consumer? Rule: no flow feature ships in the standard UI unless the core exposes it. Is the native core + RN bridge + custom views three-layer tax avoidable?
2. **Backend to SDK: server-driven flow?** Should check-in v3 hand the SDK a generic "steps" contract (type + schema) instead of a loyalty-gift screen? Generic form-schema renderer for the long tail?
3. **Staff app: share domain, not UI?** Web is Vue, staff app RN, so React-everywhere is a rewrite. Is generated OpenAPI clients + shared TS domain state in frontend/packages/shared the right seam? Webview of team chat as a cheap demand test before native port?
4. **Payments: one submitter, many providers?** Apple Pay, Google Pay, card entry, Wyndham card-on-file behind one payment-method component, mirroring Yasmin's Canary payment form model.
5. **Keys: abstract the provider before Wyndham BLE?** Old vs new OpenKey backends coexisting through the WyndhamKey sunset.
6. **Process: SDK-impact check in definition of done** for A&D and messaging specs. Cheaper than any architecture change.

Assumptions to verify: guest SDK core is native Swift/Kotlin with an RN wrapper; staff app is React Native.