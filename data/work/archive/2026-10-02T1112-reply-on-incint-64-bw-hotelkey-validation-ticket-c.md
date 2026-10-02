---
area: null
completed_at: 2026-10-02 12:27:20.850545
contexts:
- react
created: 2026-10-02 11:12:14.524524
defer_until: null
due: null
energy: medium
id: 2026-10-02T1112-reply-on-incint-64-bw-hotelkey-validation-ticket-c
order: null
output: ''
project: null
source_id: https://linear.app/canary-technologies/issue/INCINT-64/bw-hotelkey-transition-validation-failed-despite-fetch-run-completing#comment-9fa73325
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Reply on INCINT-64: BW HotelKey validation ticket closed while failures continue'
updated: 2026-10-02 12:27:20.850522
waiting_on: null
waiting_since: null
working_on: false
---

jbalian closed it Oct 1: 'open for 6 weeks on the wrong triage queue, so I'll close. Reopen if problem happens again.' It is still happening: ENT-7694 (BW 29096, same pms_validation_failed_fetch_reservation) sits in ENT triage, and 12 BW hotels failed validate_pms_configuration overnight (pms_validation_no_reservations_on_gateway / pms_validation_failed_fetch_run_exists). Decide where this should live.
https://linear.app/canary-technologies/issue/INCINT-64/bw-hotelkey-transition-validation-failed-despite-fetch-run-completing
https://linear.app/canary-technologies/issue/ENT-7694/bw-property-29096-hotelkey-pms-validation-failing-despite-successful