---
area: management
contexts:
- deep
- craft
created: 2026-05-12 10:11:27.841321
defer_until: null
due: 2026-05-12
energy: medium
id: 2026-05-12T1011-review-the-pre-production-hotels-design-doc-ryan-r
order: null
output: "## Agent run 2026-05-12T15:55Z\n\nRe-reviewed the Pre-Production Hotels design
  doc (Notion: 35881468...) after\nRyan's v4 response cycle. Three reviewer concerns
  from the prior round; all\nthree have responses. Summary:\n\n### Concerns addressed
  well\n1. **`hotel_belongs_to_portfolio_by_identifier()` shim — dropped (good).**\n
  \  Ryan audited the codebase and confirmed the shim covered ~50 direct\n   callsites
  but silently missed ~30 others: `PORTFOLIO_TO_LOYALTY_PROGRAM_IDENTIFIER_MAP`\n
  \  (`hotels/services/membership_level_new.py`), `GROUP_USE_CASES_BY_PORTFOLIO_IDENTIFIER`,\n
  \  MSA products, frozensets (WYNDHAM_IDENTIFIERS, ALL_IHG_PORTFOLIO_IDENTIFIERS,\n
  \  ENTERPRISE_PORTFOLIO_IDENTIFIERS), and `portfolio__identifier__in=` ORM\n   filters
  scattered through tips/voice/guest_journey/tmp commands. Spot-checked\n   several
  — his references are accurate. Replacing with explicit per-domain\n   wiring is
  the right call; this was the load-bearing concern from v3.\n\n2. **OHIP environment
  work (Chunk 2) — now gated on PMS Gateway review.**\n   Good. Ryan added a pre-implementation
  prereq: model shape + webhook routing\n   pattern reviewed with PMS Gateway team
  before any model code is written.\n   Mirroring PMS-7177 keeps the precedent tight.\n\n3.
  **Andrea's identifier-vs-`is_staging`-flag question** — well-defended.\n   Per-brand
  identifiers are needed regardless (~50 direct references to\n   `Portfolio.Identifier.WYNDHAM`
  et al), flag doesn't simplify GrowthBook\n   targeting, and migration-pain has gone
  away post-#33879. Andrea seems\n   satisfied. Leaves room to add a flag later if
  non-enterprise teams (tipping,\n   payments) want their own staging portfolios.\n\n###
  Outstanding — needs to land in the doc body, not just comments\nThe Notion page
  body still reads as v3: the \"v3 changes (2026-05-06)\" header\nis the latest, architecture
  bullet 4 still describes the\n`STAGING_TO_PRODUCTION` shim, §6.3 still says \"single-method
  change\", and the\nRisks section still defends the shim as \"intentional and desired\".
  Ryan's v4\nprose lives only in the comment replies (and possibly a separate\n`docs/eng-design-pre-production-hotels.md`
  he mentioned — I checked the\ncanary repo and that file does not exist locally;
  either unpushed or planned).\n**Ask Ryan to fold v4 into the page body before approval**
  — the audit table\nand per-pattern playbook are the contract for explicit wiring;
  reviewers and\nfuture contributors need to see it in the prose, not threaded comments.\n\n###
  New points worth raising\n- **Discovery-burden risk for explicit wiring.** With
  the shim gone, the\n  contract becomes \"every identifier-keyed dict / frozenset
  / ORM filter has\n  a staging row where appropriate.\" Worth adding a lightweight
  guard: a unit\n  test that iterates `Portfolio.STAGING_PORTFOLIO_IDENTIFIERS` against
  a\n  registered list of identifier-keyed maps and asserts presence (or explicit\n
  \ opt-out). Otherwise future contributors silently add new mappings missing\n  staging
  entries — exactly the kind of trap I flagged in the original\n  review.\n- **Defense-in-depth
  credential check (§6.5 step 3)** — confirm where the\n  \"validated credential's
  portfolio matches resolved hotel's portfolio\" check\n  fires. Should be in a single
  middleware/auth path, not duplicated per view.\n  Worth a line in the doc.\n- **OHIP
  migration cutover window.** Order (add nullable FK → backfill →\n  set non-null
  → swap unique constraint) is correct, but if any new\n  `OracleOhip` row is inserted
  between FK add and backfill it'll be NULL.\n  Either run during a quiet window or
  add a temporary `DEFAULT` to the\n  production-environment record at the DB level.
  Minor — call it out.\n- **`create_staging_hotel` recovery path.** Command errors
  if staging hotel\n  exists (idempotency). What's the operator workflow if creation
  fails\n  halfway (e.g., a plan provider raises after the Hotel row is created)?\n
  \ Likely just \"delete the half-created row and re-run\", but a sentence on\n  recovery
  would save EPD a Slack ping later.\n\n### Ryan's direct question to me\nHe asked
  who from PMS Gateway should review the OHIP env work. Defaulting to\nPMS-7177's
  owner is reasonable; I don't have that name in head — will check\ngit blame on the
  HAPI environment files and reply in Slack (separate\naction). Not done in this run.\n\n###
  Verdict\nv4 conceptually resolves all three blocking concerns. **Not approving yet**
  —\nconditional on (a) v4 prose actually landing in the doc body, (b) the four\nnew
  points above getting a response (most are small/clarification-grade).\n\nDraft Notion
  comment / Slack reply: NOT POSTED. Will paste when user\napproves — see this output
  field as the source.\n"
project: 2026-04-16T1210-unblock-team
source_id: https://canarytechnologies.slack.com/archives/C0B1VTR4Q4B/p1778531996764439
tags:
- morning-gtd
- slack
time_minutes: 15
title: Review the Pre-Production Hotels design doc (Ryan ready for re-review)
updated: 2026-05-12 21:58:37.799892
waiting_on: null
waiting_since: null
working_on: false
---

Ryan: 'responded to comments and made changes; doc ready to look at again cc @glloyd @andrea'. Notion: 'Pre-Production Hotels'. https://canarytechnologies.slack.com/archives/C0B1VTR4Q4B/p1778531996764439