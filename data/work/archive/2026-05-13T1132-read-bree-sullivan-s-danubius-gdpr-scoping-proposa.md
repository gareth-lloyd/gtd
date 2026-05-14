---
area: null
contexts:
- consume
created: 2026-05-13 11:32:58.763105
defer_until: null
due: null
energy: medium
id: 2026-05-13T1132-read-bree-sullivan-s-danubius-gdpr-scoping-proposa
order: null
output: '## Agent run 2026-05-13T14:05Z


  Read the full 70-message Slack thread (C0A83PDRP3P), Bree''s Notion scoping proposal,
  Sebastian''s WIP PRD (v1+v2), and both Linear projects (ID purge + PII deletion).


  ### What the proposal says


  Bree''s doc ("Danubius GDPR Compliance — Scope & Pricing Proposal") splits the work
  into two buckets:


  **1. Included at no cost (platform GDPR work)**

  - Contact PII obfuscation across all guest-facing surfaces (reservations, reg cards,
  signatures, additional guests, kiosk)

  - Configurable per-property retention policy (time-based: X days after departure,
  check-in, or hours after submission)

  - Downstream system remediation (Snowflake, Datadog, Groundcover, Mindee)

  - Read-only compliance dashboard in Product Settings

  - Framed as standard EMEA compliance — applies to all EU customers


  **2. Optional Danubius add-on — $20,000 (2 weeks × $250/hr × 80hr)**

  - PII purge triggered by completion of full pre-check-in flow (not PMS sync — Martijn
  corrected this mid-thread)

  - Incomplete/non-submitted check-ins purged on reservation status change (In House
  / Canceled)

  - Block re-ingestion if PMS re-pushes reservation post-purge

  - Audit instrumentation for per-reservation compliance evidence

  - Key consequence: after purge fires, no guest PII visible in Compendium, Messaging,
  Voice, Upsells, Payments


  **Explicitly out of scope:** staff/admin PII, hard deletion (obfuscation only),
  per-jurisdiction defaults (future Phase 3), PII backfill for existing checked-out
  guests.


  ### Eng estimates from the PRD (Sebastian''s v2)


  | Track | Item | Estimate |

  |-------|------|----------|

  | Done | Property-level retention config (PMS GW) | Shipped |

  | Done | ID purge after check-in | Shipped (kiosk WIP) |

  | 1A | Core Canary PII obfuscation | ~1 week |

  | 1A | Per-property retention config | ~0.5 week |

  | 1A | Dashboard surfacing | ~0.5 week |

  | 1B | Downstream vendor audit + remediation | ~1 week eng + unknown vendor elapsed
  |

  | 2A | Danubius PMS sync trigger + block re-ingestion | ~2 weeks (TBC) |


  Total platform (Track 1): ~3 weeks eng. Danubius add-on (Track 2): ~2 weeks eng.


  ### Key tensions / open items from the thread


  1. **Obfuscation vs. hard deletion** — Danubius indicated obfuscation is insufficient,
  wants full deletion. Sebastian''s email to them emphasizes obfuscation and omits
  deletion. Awaiting their response. Blake approved engaging lawyers on the legal
  question. My comment in thread: obfuscation beyond recovery satisfies GDPR (Recital
  26 anonymisation), but pseudonymisation with retained keys does NOT.


  2. **Reservation-level vs. field-level purge** — Martijn flagged that field-level
  purge (obfuscate individual fields as each is synced to PMS) would be "exponentially
  more complex" (~2 months). Bree''s proposal scopes to reservation-level (purge everything
  once full pre-check-in completes). Blake agreed field-level is unnecessary.


  3. **2-week estimate confidence** — Martijn is "100% confident it''s the minimum."
  Bree is worried about the maximum. Blake says to pad considerably ("double at least").
  The $20k pricing uses the raw 2-week estimate without padding.


  4. **Partial submissions** — Check-in v2 sends data to PMS incrementally (reg card
  first, then additional guests). There''s no single "sync complete" event. Purge
  trigger for incomplete submissions falls back to reservation status change.


  5. **Re-ingestion loop** — If PMS re-pushes a reservation post-obfuscation, PII
  gets re-populated. Block re-ingestion logic is load-bearing for the add-on. Design
  TBD (Martijn).


  6. **Downstream gaps** — Ryan noted Snowflake name+email are NOT obfuscated today.
  Reg card obfuscation was previously built but deliberately undone (AD-7379) because
  it was blanket rather than configurable. Existing PMS Gateway obfuscation logic
  can be reused.


  7. **CX workflow breakage** — Post-obfuscation, support can''t search by guest name/email.
  Replacement workflow needed before any rollout. Blocking.


  8. **Mindee** — No deletion endpoint. Accelerating in-house OCR is the permanent
  fix.


  ### Next steps per the thread (Sebastian''s summary, reply 66)

  1. Lock down legal obligation: obfuscation vs. deletion (lawyer engaged, Blake approved)

  2. Await Danubius reply on obfuscation vs. deletion preference

  3. Solidify costing for both scenarios (PMS sync + deletion, PMS sync + obfuscation)


  Thread consensus as of last message: wait for Danubius response before sending proposal.
  No immediate urgency to finalize the cost estimate today.


  ### My read on what matters for eng


  - The platform GDPR work (Track 1) is real and overdue. ~3 weeks for 1 engineer
  is plausible for the core obfuscation + config + dashboard, but the downstream vendor
  work (Snowflake, Mindee) has unbounded elapsed time.

  - The Danubius add-on estimate of 2 weeks is tight. The re-ingestion blocking and
  partial-submission edge cases add real complexity. Blake''s instinct to double is
  reasonable — 4 weeks would be safer to quote externally.

  - The $20k pricing ($250/hr × 80hr) doesn''t include the padding Blake recommended.
  If we double to 4 weeks that''s $40k.

  - The biggest architectural risk is the event audit trail — EventableModel snapshots
  contain PII at mutation time. The obfuscation pass must walk event payloads too,
  which isn''t trivial.

  - Ryan''s existing obfuscation tooling in PMS Gateway is a significant accelerant
  if it can be extended to cover the missing fields (name, email in Snowflake; reg
  card configurability).


  ## Agent run 2026-05-13T14:15Z — Codebase due diligence


  Reviewed the pms-gateway `gdpr/` app and related obfuscation infrastructure to ground
  the estimates.


  ### What already exists (PMS Gateway)


  **Mature obfuscation framework** — not a prototype, this is production infrastructure:

  - `ObfuscatableModel` mixin (adds `obfuscated_at` timestamp) + `obfuscatable_field()`
  decorator to tag individual fields

  - `ObfuscationPolicy` model: per-account, configurable lag (hours/days/weeks/months/years),
  active/inactive

  - `ObfuscationPlan` model: FSM lifecycle (created → started → completed/failed),
  audit trail of who triggered it

  - `ScheduledObfuscationService`: runs every 60s via beat, processes all active policies,
  finds guests past cutoff, obfuscates in batches (10-thread pool, capped at 1000
  guests per run)

  - `ObfuscateUtil`: the core workhorse — handles both model-level AND delta-tree
  obfuscation. Walks every Delta payload and replaces obfuscatable field values with
  `OBFUSCATED_VALUE_PREFIX + uuid4().hex`. This addresses the PRD''s risk about EventableModel
  audit trail integrity.

  - `SnowflakeDeletionService`: already coordinates deletion of guests, check-ins,
  and check-outs in Snowflake by UUID. Has SQLAlchemy models for Snowflake tables
  (Guest, CheckIn, CheckOut).


  **Models already tagged obfuscatable:**


  | Model | Obfuscatable fields |

  |-------|-------------------|

  | `Guest` | first_names, last_names |

  | `Address` | street, city, state, postal_code, country, raw_country |

  | `Email` | email |

  | `Phone` | phone, normalized_phone |

  | `GuestInformation` | first_name, middle_name, last_name, email, phone, company,
  address_1, address_2, city, state, country, raw_country, zip_code |


  **Delta tree obfuscation is solved** — `ObfuscateUtil.obfuscate_guest()` creates
  a genesis delta, walks all deltas for the guest entity, obfuscates payloads for
  Guest + related Address/Email/Phone, deletes existing related models, re-commits
  from the obfuscated snapshot, then delivers via webhook. Same pattern for `GuestInformation`
  on the reservation tree. This is the hardest part and it''s done.


  ### What does NOT exist yet


  1. **No Canary-core obfuscation infrastructure.** Canary `Guest` model has an `obfuscated_at`
  field and the reservation ingestion propagates it from PMS GW, but there''s no `ObfuscatableModel`
  mixin, no `obfuscatable_field` decorator, and no PII purge service on the Canary
  side. The PRD''s "Core Canary obfuscation" (~1 week) needs to build this from scratch
  for: Reservations, Check-ins (Registration Cards, Additional Guest Details, Signature),
  Kiosk Sessions.


  2. **No event-triggered purge** — the scheduled service only does time-based cutoffs
  from checkout date. There''s no "purge after pre-check-in completion" trigger. This
  is the entire Danubius add-on.


  3. **No re-ingestion blocking** — when PMS GW receives a reservation update, it
  processes it unconditionally. There''s no guard that says "this guest/reservation
  has been obfuscated, reject PII re-population." This is load-bearing for Track 2A.


  4. **No per-property retention config in Canary** — ObfuscationPolicy in PMS GW
  is per-account (which maps to a PMS connection, not a hotel). The proposal says
  "configurable per property" with new `pii_retention_days` / `pii_purge_strategy`
  fields on `CheckInConfiguration`.


  5. **Snowflake deletion exists but is incomplete** — `SnowflakeDeletionService`
  handles guest/checkin/checkout rows, but Ryan flagged that name and email are not
  currently obfuscated in Snowflake. Likely a CDC pipeline gap where raw PII flows
  to Snowflake before obfuscation runs.


  6. **Reg card obfuscation was built then removed** — AD-7379 undid blanket reg card
  obfuscation because it was all-or-nothing. Needs to be re-enabled behind per-hotel
  config.


  ### Estimate assessment


  **Track 1A (Core Canary obfuscation, ~2 weeks):** The PMS GW framework is reusable
  as a *pattern* but not directly importable into Canary (different service, different
  ORM patterns, no Delta tree). Need to build: PII purge service, field-level obfuscation
  for ~6 Canary models (Guest, Reservation, CheckIn/RegistrationCard, AdditionalGuestDetails,
  Signature, KioskSession), event payload walking for EventableModelMixin. 2 weeks
  is plausible if scoped carefully.


  **Track 1B (Downstream, ~1 week + vendor elapsed):** Snowflake deletion service
  exists but needs CDC pipeline audit. Datadog has 90-day auto-purge. Mindee is a
  contract/legal problem, not an eng problem (unless we accelerate in-house OCR).
  1 week eng is reasonable; vendor elapsed is the real unknown.


  **Track 2A (Danubius add-on, ~2 weeks):** This is the riskiest estimate. The three
  pieces are: (1) trigger after pre-check-in completion — need to define "complete"
  across the multi-step v2 check-in flow, (2) re-ingestion blocking — requires a new
  guard in the PMS GW load path that''s never existed, (3) status-change fallback
  for partial/non-submissions. Re-ingestion blocking alone could be a week if the
  Delta tree semantics are tricky. Blake''s "double it" is well-advised.


  **Bottom line:** The PMS GW obfuscation framework is more mature than the thread
  suggests — Ryan''s "existing tool" comment undersells it significantly. The hard
  part is Canary-core, which has no equivalent infrastructure. The estimates are credible
  minimums but the Danubius add-on has real tail risk from re-ingestion blocking complexity.

  '
project: null
source_id: https://canarytechnologies.slack.com/archives/C0A83PDRP3P/p1778598481605069?thread_ts=1778489351.316369
tags:
- morning-gtd
- slack
- from-awareness
time_minutes: 15
title: 'Read: Bree Sullivan''s Danubius GDPR scoping proposal'
updated: 2026-05-13 13:48:37.203870
waiting_on: null
waiting_since: null
working_on: false
---

Scoping doc needs eng estimates for Danubius-specific PMS sync add-on; much of the work is GDPR platform work we should do anyway for EMEA. https://canarytechnologies.slack.com/archives/C0A83PDRP3P/p1778598481605069?thread_ts=1778489351.316369