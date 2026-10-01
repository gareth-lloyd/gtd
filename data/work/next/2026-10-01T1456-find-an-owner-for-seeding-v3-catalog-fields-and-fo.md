---
area: null
completed_at: null
contexts:
- react
created: 2026-10-01 14:56:39.851980
defer_until: null
due: null
energy: medium
id: 2026-10-01T1456-find-an-owner-for-seeding-v3-catalog-fields-and-fo
order: null
output: ''
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 30
title: Find an owner for seeding V3 catalog fields and forms from onboarding scripts
updated: 2026-10-01 15:00:56.844107
waiting_on: null
waiting_since: null
working_on: false
---

From: call with Leandro Alvarez and Andrea Bradshaw, 2026-09-30 ("Step configurator and rules-based", https://notes.granola.ai/d/c12bc682-f460-41f8-83c1-65437690c98c).
Full notes and code references: data/work/archive/2026-10-01T1140-write-up-notes-from-call-with-leandro-actions-for.md
Derived from the call and a code check, not a commitment made on the call.

Why now: since #57957 (ENT-7607, merged 2026-09-28, https://github.com/canary-technologies-corp/canary/pull/57957) the registration card plan refuses every V3 hotel and rolls back the whole script run. Once an IHG hotel is on V3, a card or country-settings change has no script path. Caitlin's thread of 2026-09-24 says the aim is to move all IHG to V3.

- Leandro and Andrea both described the scripts creating a default set of catalog fields plus forms. The A&D TDD assigns seeding to enterprise (https://app.notion.com/p/365814686151808c805efb429b821412). The Binding Rules Tree doc puts onboarding out of scope.
- Interim route from Leandro: write a registration card and run the script that converts it to catalog fields. It stops working once CS splits a card into several step forms.
- First step: read ENT-7607 (https://linear.app/canary-technologies/issue/ENT-7607) for what follow-up was agreed. Then a ticket, IHG first.
- Related wait: Leandro is asking Guido how many properties run V3 and which are IHG.