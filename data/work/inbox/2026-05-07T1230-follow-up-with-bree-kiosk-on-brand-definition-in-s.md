---
area: null
contexts: []
created: 2026-05-07 12:30:52.101901
defer_until: 2026-05-18 09:00:00
due: null
energy: null
id: 2026-05-07T1230-follow-up-with-bree-kiosk-on-brand-definition-in-s
order: null
output: ''
project: null
source_id: null
tags: []
time_minutes: null
title: Follow up with Bree/Kiosk on Brand definition in step configurator
updated: 2026-05-12 10:46:41.377096
waiting_on: null
waiting_since: null
working_on: false
---

## How the kiosk step system looks at brand

- **Single source of truth:** `KioskConfiguration.kiosk_management_group` — a `CharField` with choices from `KioskManagementGroup` (`marriott`, `ihg`, `wyndham`, `delaware_north`, `apple_app_store`).
- **One read site:** `kiosk/services/session.py:71` passes `session.config.kiosk_management_group` into `StepFramework.get_steps(management_group=...)`.
- **Filter rule** (`framework.py:137-139`): include a step if its `get_management_group()` returns the same value, OR if it returns `None` (generic). Steps tagged for *other* brands are skipped.
- **How a step "tags" itself:** brand-specific subclasses (e.g. `MarriottUnavailableStep` in `kiosk/steps/brands/marriott/`) override `get_management_group()` to return their `KioskManagementGroup`. Generic steps don't override it.
- **Ad-hoc inline checks:** scattered code does `kiosk_config.kiosk_management_group == KioskManagementGroup.MARRIOTT` for branching inside steps/services (e.g. `early_check_in/step.py:75`, `utils/payment.py:93`) — outside the framework, harder to govern.
- **Not consulted:** `Hotel.brand` (FK to `Brand` model), `Portfolio`, `country_code`. The `Brand` model is display metadata only.
- **Implication:** brand for step routing is a denormalized string key on KioskConfiguration, decoupled from the `Brand` entity it nominally represents.