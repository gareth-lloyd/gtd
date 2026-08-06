---
area: null
completed_at: 2026-08-05 20:29:58.612753
contexts:
- consume
created: 2026-08-05 07:19:55.531305
defer_until: null
due: null
energy: medium
id: 2026-08-05T0719-read-stephanie-s-q3b-internal-tools-planning-doc-b
order: null
output: |
  ## Agent run 2026-08-05T15:10:00+03:00

  Read the doc + Stephanie's DM + her inline comments + the Q3B database rows + the linked User Management overview. Prep brief for the 16:00 1:1 below.

  **The decision Stephanie wants to lock**: where features get built — /manage (customer-facing surface) vs adminland — for the two immediately impacted areas: check-in V3 (onboarding automation) and user management. Her stated lean (DM, 2026-08-04): "manage unless the tool has a lot of overlap for users. I don't love building canary-only features into adminland but if Blake/SJ actually have a strong opinion otherwise, I'm good to commit to that and move forward to unblock everyone."

  **Key doc**: Planning - Internal Tools - Q3B (Internal Notes) (https://app.notion.com/p/canarytechnologies/Planning-Internal-Tools-Q3B-Internal-Notes-3b1814686151816cb470da06f103f965). Five themes: (1) Decrease Engineering Support Dependency (AI Workup org-wide rollout + accuracy + speed + interactivity + KB enablement + model benchmark by Sept 1; User Management; Gateway config ChangeTracker), (2) PMS Capabilities (non-enterprise; OHIP likely next), (3) Onboarding Automation (Check-in V3 + AI Voice discovery), (4) Support (web form, geo phone numbers, Hotel Support ID backfill, Zendesk OAuth), (5) Pages external sharing via magic links.

  **User management — the strongest evidence in the doc** (aggregated overview: https://app.notion.com/p/3b18146861518163a0d4cff07c3389e3):
  - 78% of the Oncall queue is user management (606 tickets); 93% self-serviceable by a trained agent; 83% concentrated in just two actions (create user + grant role/permission); 38% of tickets are bulk → any tool must be batch-shaped.
  - Stephanie's inline comment on the User Management section (2026-08-03): "leaning towards a self-serve batch user-adding flow" — i.e. customer-facing, which points at /manage, consistent with her DM lean.
  - Solution options already on the table: A) SAG (already lives in Manage → Properties, rollout underway, PR #48223/TOOL-313), B) Managed Support Access proposal (Lautaro — a dedicated *internal* section inside Manage with audited actions: https://app.notion.com/p/3ae81468615181abbf82ea4f92ef9794), C) SCIM for big chains (ENT-6491, design in review, low priority), D) Trained L2 support + single intake (needs Blake sign-off → Nensy).
  - Note: both A and B already build internal tooling *into Manage*, so precedent favors /manage even for staff-facing flows.

  **Check-in V3 onboarding** (Q3B row, In Discovery): auto-generate registration card + check-in config from country + ID-capture method (OCR vs ID verification); replaces manual CSM/CSA setup; blocked on Check-in v3 landing (~next month) but built in parallel; should extend to kiosk/tablet; it's the Internal Tools slice of EMEA Registration Card Onboarding. Linear: https://linear.app/canary-technologies/project/automate-check-in-v3-onboarding-617b22ca4b48. This one is onboarding/config tooling with no hotel-user overlap → by Stephanie's own rule it's the candidate for adminland/internal, unlike user management.

  **Talking points for the 1:1**:
  1. The user-overlap test cuts differently for the two areas: user management is heavily user-overlapping (customers self-serve batch adds; SAG/Managed-Support-Access already live in Manage) → /manage. Check-in V3 onboarding config is staff-only → internal surface is defensible.
  2. The 83%-two-actions + 38%-bulk numbers mean a narrow self-serve batch flow in /manage drains most of the oncall queue without needing the full Managed Support Access build.
  3. Open dependency: does Blake/SJ actually hold a strong contrary opinion? Stephanie explicitly says she'll commit either way to unblock — so the 1:1 output should be a decision, not more discovery.
  4. Zendesk OAuth deadline is real (tokens start deactivating 2026-07-28 → already past; full stop 2027-04-30) but Stephanie commented "can push to next block".

  Slack DM: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1785855779230699
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1785855779230699
tags:
- morning-gtd
- slack
time_minutes: 20
title: Read Stephanie's Q3B Internal Tools planning doc before today's 4pm 1:1
updated: 2026-08-05 20:29:58.612746
waiting_on: null
waiting_since: null
working_on: false
---

You told Stephanie "I'll take a look at that Notion"; the 1:1 moved to today 16:00. She wants to lock the "where are we building things" decision (check-in V3, user management) — her lean is /manage unless heavy user overlap.
https://canarytechnologies.slack.com/archives/D09Q1PTAMTR/p1785855779230699