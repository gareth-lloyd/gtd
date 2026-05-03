---
area: null
contexts: []
created: 2026-04-30 07:59:37.498287
defer_until: null
due: null
energy: low
id: 2026-04-30T0759-rule-suggestion
order: null
project: 2026-04-16T1319-rules-based-config
source_id: null
tags: []
time_minutes: 5
title: 'Rule suggestion: copy check-in payment slot → PMS auths slot when auths is empty'
updated: 2026-04-30 07:59:37.502784
waiting_on: null
waiting_since: null
---

Candidate rule from David Thomson (ENT-6056 triage thread, 2026-04-30):

> If a hotel has `Check In - Pms payment slot identifier` set but
> `PMS Integration - Pms payment slot identifier auths` is empty,
> copy the check-in value into the auths slot.

**Why it's a good rules-engine candidate:**

- 417 hotels / 12,366 auth-post failures in 7 days are caused by the auths
  slot being unset. Mostly Wyndham (Synxis + OHIP).
- Hotels that bothered to configure the check-in slot almost certainly want
  the same value for auths — David's hypothesis is that this covers "most"
  of the affected fleet, leaving a small residual to chase manually.
- One-off scripting works for the immediate fix, but the underlying gap is
  permanent: future onboardings will keep landing in the same broken state
  unless something enforces the invariant. That's exactly what the
  rules-based config project is for.

**Open questions for the rule design:**

- Trigger: on save of `pms_payment_slot_identifier` (check-in), or on a
  scheduled sweep?
- Override: should manual `pms_payment_slot_identifier_auths = null` stick,
  or always re-fill from check-in? (i.e. is this a default or an invariant?)
- Audit: log when the rule fires so we can diff against David's one-off
  script run and confirm coverage.

**Links:**

- Thread: https://canarytechnologies.slack.com/archives/C04STT7UPRQ/p1777501210457089?thread_ts=1777497151.022479&cid=C04STT7UPRQ
- ENT-6056: https://linear.app/canary-technologies/issue/ENT-6056/p1-auth-form-cc-posting-fails-on-428-hotels-missing-payment-slot
- Affected hotels sheet: https://docs.google.com/spreadsheets/d/1LNo1NBe9ztm2PkfQjgrOqPsgyio_mvU3oAnBrxlg6Ms/edit
