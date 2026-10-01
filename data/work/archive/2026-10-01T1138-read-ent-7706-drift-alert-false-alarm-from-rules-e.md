---
area: null
completed_at: 2026-10-01 14:42:57.385126
contexts:
- consume
created: 2026-10-01 11:38:05.360811
defer_until: null
due: null
energy: low
id: 2026-10-01T1138-read-ent-7706-drift-alert-false-alarm-from-rules-e
order: null
output: |
  ## Agent run 2026-10-01T14:33:32

  **Verdict: the Sep 30 alert was caused by your ENT-7614 change, and it is not really a false alarm.** The 29 hotels were already non-conforming; the old resolver was not checking those keys. Tincho closed ENT-7706 as Done five minutes after opening it, with one comment and no follow-up ticket.

  ### What Tincho found
  ENT-7706 (https://linear.app/canary-technologies/issue/ENT-7706/investigate-the-sep-30-drift-alert-29-new-wyndham-hotels), single comment, 2026-09-30:
  - Nobody edited these hotels. The drift appeared because ENT-7614 (https://linear.app/canary-technologies/issue/ENT-7614/rules-engine-make-key-resolution-define-aware-and-reject-ambiguous, PR #57673 https://github.com/canary-technologies-corp/canary/pull/57673) deployed on Sep 29 between two nightly drift runs (v2026.34.48 to v2026.34.89).
  - All 29 are Wyndham hotels matching GMS + live Connect Plus. Before the fix, keys defined on the lighter sibling were silently dropped for them; now they resolve and are measured against existing config.
  - His example: hotel 2547 has live MSAs GMS + "Wyndham Connect Plus GSP", so `has_chat` (defined on the GMS root) now resolves and exposes a long-standing `has_chat=False`.
  - His evidence that no settings changed: no `has_chat` change event ever on 2547; zero `config_changed` events in 120 days for `require_credit_card_postal_code` (1264) and auth `payment_gateway_config_id` (1153); drift counters flat all week (about 4912 checked, 2 skipped, 199 drifting) until Sep 30 (228).

  ### What the alert surfaced (hotels, expected to actual)
  - `authorization_configuration.payment_gateway_config_id`: 8 (set to null)
  - `check_in_configuration.payment_gateway_config_id`: 1 (set to null)
  - `require_credit_card_postal_code`: 6 (True to False)
  - `blocked_card_types`: 6 ([] to Debit/Prepaid/Unknown)
  - `is_tokenizing_with_hotel_payment_gateway`: 4 (True to False)
  - `match_cardholder_and_client_name`: 4 (False to True)
  - One hotel each: `blocked_card_networks`, `disable_stripe_validation`, `integration_auto_post_to_pms_udf`, `integration_precheckin_method` (prereg to notes), `require_preexisting_reservations`, `has_chat`

  ### What I checked myself
  - The commit message of f4bcf79d995 (ENT-7614) predicts exactly this: hotels matching "Wyndham GMS + live Connect Plus, IHG GMS Core + Pilot ... gain keys; no resolved value changes anywhere else." So the outcome matches the stated design.
  - I did not re-verify Tincho's per-hotel evidence (event history, drift counters). The canary MCP servers and Teleport were down this session, so those claims are his, not confirmed by me.

  ### Open threads
  1. **The triage pass has no owner.** Tincho's comment ends "still worth a triage pass on the surfaced gaps, especially the ~8 hotels with a null payment_gateway_config_id ... fix or acknowledge per case", but the ticket is Done and I found no follow-up ticket in Enterprise (searched "drift" over the last 3 days; only ENT-7706 and ENT-7705 came back on the first page). The 9 null `payment_gateway_config_id` and 4 `is_tokenizing_with_hotel_payment_gateway=False` hotels are the ones most likely to be real payment problems.
  2. **IHG gained keys too, but nothing watches them.** The commit says IHG GMS Core + Pilot hotels gain keys the same way. The nightly drift job only covers `WYNDHAM_CONNECT_GMS`, ESA and Four Seasons (`rules_based_configuration/services/drift.py:32-34`), so any equivalent newly-exposed IHG non-conformance would not have alerted.
  3. Related, not caused by this: ENT-7705 (https://linear.app/canary-technologies/issue/ENT-7705/add-links-to-each-property-in-config-drift-notices) adds property links to drift notices, Backlog, Tincho. ENT-7699 ("a heavier sibling shadows a lighter one on a definition the hotel does not match") is linked to ENT-7614 and I did not read it.

  No external writes made.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-7706/investigate-the-sep-30-drift-alert-29-new-wyndham-hotels
tags:
- morning-gtd
- linear
- from-awareness
time_minutes: 10
title: 'Read: ENT-7706 drift alert false alarm from rules-engine change'
updated: 2026-10-01 14:42:57.385118
waiting_on: null
waiting_since: null
working_on: false
---

Promoted from the 2026-10-01 awareness report (Linear watching, item 14).
https://linear.app/canary-technologies/issue/ENT-7706/investigate-the-sep-30-drift-alert-29-new-wyndham-hotels