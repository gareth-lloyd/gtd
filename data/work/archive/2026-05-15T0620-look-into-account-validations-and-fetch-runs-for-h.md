---
area: null
contexts: []
created: 2026-05-15 06:20:52.013256
defer_until: null
due: null
energy: low
id: 2026-05-15T0620-look-into-account-validations-and-fetch-runs-for-h
order: -18
output: "## Agent run 2026-05-15T07:00 — HotelKey AccountValidations & fetch runs\n\nQuestion:
  What does the PMS gateway support for HotelKey AccountValidation\ntypes, and can
  it do fetch runs? Answer below, all paths under\nbackend/pms-gateway/.\n\n### AccountValidation
  types: NONE are registered for HotelKey\n\nvendors/integrations/hotelkey/services/configuration.py:113-117\n
  \ - get_validations() returns []\n  - update_validations() returns []\n\nThis means
  NO AccountValidation rows are configured for HotelKey accounts,\nso HotelKey has
  no scheduled/automated account-validation or monitoring\nchecks the way other PMSes
  do. The Validation type enum\n(accounts/models/validation.py) offers: IP_WHITELIST,
  FETCH_RESERVATION,\nFETCH_RESERVATIONS, FETCH_EVENTS, AUTHENTICATE, FETCH_RUN_EXISTS
  — HotelKey\ndeclares none of them.\n\nNote the distinction: a HotelKeyValidationService
  DOES exist and is\nregistered as a provider (services/validation.py:31-42), so the
  validation\n*primitives* are partially implemented:\n  - fetch_reservation()  ->
  implemented (validation.py:44-45)\n  - fetch_reservations() -> implemented (validation.py:47-55)\n
  \ - ping()               -> implemented (validation.py:57-61)\n  - authenticate()
  \      -> raises FeatureNotImplemented (validation.py:63-65, TODO)\n  - fetch_events()
  \      -> raises FeatureNotImplemented (validation.py:67-68)\n  - fetch_run_exists()
  \  -> raises FeatureNotImplemented (validation.py:70-71)\nBut because get_validations()
  returns [], none of these run as configured\nAccountValidations. The capability
  exists; the wiring to schedule it does not.\n\n### Fetch runs: YES, supported in
  code, but heavily gated\n\nvendors/integrations/hotelkey/services/fetch.py\n  -
  HotelKeyFetchService is registered as a fetch provider (fetch.py:83-85)\n  - Two
  FetchConfigurations declared (fetch.py:91-123):\n    1. \"hotelkey.fetch_reservations_due_in_3_days\"
  — every 12h, backstop for\n       missed webhooks; window now..+3 days. GATED: only
  HotelKey accounts\n       with a non-empty brand_identifier (fetch.py:107-109, TODO
  PMS-6643 to\n       remove the filter once all accounts have brand_identifier).\n
  \   2. \"hotelkey.on_demand\" — on-demand; but get_configurations returns\n       HotelKey.objects.none()
  (fetch.py:121), so effectively no accounts\n       qualify for on-demand fetch today.\n\n###
  Reconciling the apparent contradiction\n\nconfiguration.py:100-101 requires_fetch_service()
  returns False. This is NOT\n\"fetch unsupported.\" HotelKey is webhook-driven; the
  fetch service is an\noptional backstop for missed webhook events, not a required
  sync path.\nrequires_fetch_service=False just means an account is healthy without
  the\nfetch service running. Opera behaves the same way.\n\n### Bottom line\n\n-
  AccountValidations: zero registered for HotelKey. Validation service\n  primitives
  are partly built (fetch_reservation/fetch_reservations/ping\n  work; authenticate/fetch_events/fetch_run_exists
  are stubs raising\n  FeatureNotImplemented). No automated account validation today.\n-
  Fetch runs: yes, a scheduled 12h reservation-backstop fetch and an\n  on-demand
  fetch exist, but both are gated — the scheduled one only runs\n  for accounts with
  brand_identifier set (PMS-6643), the on-demand one\n  matches no accounts at all
  currently.\n- Practical gap vs a fully-featured PMS: no AUTHENTICATE/credential\n
  \ validation, no fetch_run_exists health check, and fetch coverage limited\n  to
  brand_identifier-configured accounts.\n"
project: null
source_id: null
tags: []
time_minutes: 5
title: Look into account validations and fetch runs for hotelkey. What does gateway
  support for AccountValidation types and can it do fetch runs?
updated: 2026-05-15 06:32:53.312819
waiting_on: null
waiting_since: null
working_on: false
---