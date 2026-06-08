---
area: null
contexts: []
created: 2026-06-04 16:51:35.034673
defer_until: null
due: null
energy: low
id: 2026-06-04T1651-find-out-about-the-has-standard-monitoring-flag
order: null
output: |
  ## Agent run 2026-06-04T16:55Z — "has_standard_monitoring" flag (ENT-6421)

  ### What it is
  `has_standard_monitoring` is a per-PMS-configuration BooleanField (default=True),
  defined on the abstract `PMSConfiguration` base in
  backend/pms-gateway/pms_base/models/pms_configuration.py:75 and inherited by every
  PMS integration's config (opera, autoclerk, cloudbeds, ohip, synxis, etc.). It lives
  in the pms-gateway service, NOT in canary.

  ### What it enables
  It gates whether an account contributes "standard monitors" to the health/incident
  system. Every integration's monitor provider (e.g. opera/services/monitor.py) returns
  its monitor set ONLY when `is_enabled AND has_standard_monitoring` are both true;
  otherwise it returns []. Pattern is identical across all ~40 integrations.

  Those standard monitors are (metrics/services/monitor.py):
    - ReservationsStandardMonitor — fires NO_RESERVATIONS_UPDATED incident when no
      reservation create/update events arrive within the interval (WARNING @ 1 day,
      CRITICAL @ 2 days). This is the core "reservations stopped flowing" alert.
    - Some integrations also add API error-rate and report-received monitors.

  Flow: MonitorService.refresh_incidents() (scheduled) -> get_unhealthy_monitors()
  walks MONITOR_PROVIDERS -> each provider is gated on the flag -> unhealthy monitors
  open/close Incident rows (source=MONITOR) -> these incidents drive the reservations
  health dashboard / alerting.

  => ANSWER to ticket Q1 ("if unchecked, reservations health dashboard won't be active?"):
  Correct. With has_standard_monitoring=False, the provider short-circuits, no standard
  monitors run, and no reservation-freshness/API-error incidents are generated for that
  hotel. You lose health monitoring + alerting. (The integration itself still works —
  reservations still sync; you just aren't watching for them stopping.)

  ### Is it vital to set?
  For any LIVE/production hotel you want monitored: yes — without it you get no alert if
  reservation sync silently breaks. It does NOT affect data flow / reservation fetching
  itself (that's `is_enabled`). So "not breaking but flying blind" is the right framing.

  ### Why it wasn't enabled by the validate step (the actual ENT-6421 cause)
  - The "validate PMS" onboarding step (onboarding/plans/configure_pms_integration_validate_plan.py)
    only runs PMS validations (authenticate / fetch reservation / etc.). It NEVER touches
    has_standard_monitoring. So expecting validate to enable it is a wrong assumption.
  - The flag defaults to True on the model, BUT the create/upsert path actively turns it
    OFF: AccountService.__upsert_configuration (accounts/services/account.py:421) calls
    `service.disable_standard_monitoring(configuration)` unconditionally on every upsert,
    and upsert_configuration also calls MonitorService.disable_monitors(account). So after
    config creation the flag is False.
  - Nothing in the automated onboarding/enable path turns it back on:
    `enable_standard_monitoring` exists on every service but is NOT called anywhere outside
    tests (grep-confirmed in both pms-gateway and canary). `enable_configuration` only flips
    `is_enabled`, not monitoring. So today it appears to require a manual flip (Django admin —
    it's an admin list field/fieldset on host, ulyses, opera, ohip, skytouch, shiji_daylight).

  => ANSWER to ticket Q2 ("deactivate PMS disabled the integration but kept monitoring on —
  can monitoring be disabled too?"): Functionally it's already moot. Once is_enabled=False,
  the provider's `is_enabled AND has_standard_monitoring` guard returns [] regardless, so a
  deactivated hotel produces no monitors / no incidents even with the flag still reading True.
  The lingering True is cosmetic in admin. If they want it tidied, deactivate could also call
  disable_standard_monitoring — but it changes nothing operationally.

  ### Suggested reply direction (NOT yet sent — needs your approval)
  1. Confirm: yes, no standard-monitoring = no reservations health monitoring for that hotel.
  2. Clarify the validate step never sets this flag; creation actively disables it and no
     automated step re-enables it, so it's effectively a manual admin toggle today. That gap
     is arguably the real bug to fix (auto-enable on go-live, or an onboarding step).
  3. Deactivate doesn't need to also clear the flag — is_enabled=False already stops all
     monitoring; clearing it would be cosmetic only.

  Caveat: I did not exhaustively trace every onboarding plan; the "nothing re-enables it"
  conclusion is from a full grep of enable_standard_monitoring / enable_monitors callers
  (only test usages found). Worth a 5-min confirm with whoever owns the onboarding go-live
  plan before replying on the ticket.
project: null
source_id: null
tags: []
time_minutes: 5
title: Find out about the "has standard monitoring" flag
updated: 2026-06-05 15:26:30.200398
waiting_on: null
waiting_since: null
working_on: false
---

* what does it enable?
* is it vital to get it set?
https://linear.app/canary-technologies/issue/ENT-6421/has-standard-monitoring-did-not-enabled-when-we-run-validate-pms-step