---
area: null
contexts: []
created: 2026-06-15 12:32:31.153554
defer_until: null
due: null
energy: low
id: 2026-06-15T1232-review-document-and-overview-prs
order: null
output: |
  ## Agent run 2026-06-15T13:05 — review of OpenAPI-in-monorepo doc + PRs

  **Source:** Arihant Daga's review request in Slack
  https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1781511958676179
  (cc Jordan Sterling, Tommy). EE-1340.

  **Design doc (Notion):** "OpenAPI Specs in the Monorepo"
  https://www.notion.so/canarytechnologies/OpenAPI-Specs-in-the-Monorepo-38081468615180259443fca1f29fe831
  Status: IN REVIEW. Owner: Arihant. Team: Engineering Enablement.
  UPDATE: I have now read the doc (Notion reconnected). It is short and clear,
  and the 3 PRs faithfully implement all four of its steps:
    1. "You generate it locally" → PR1 (make command, committed spec)
    2. "CI won't let it drift" (staleness diff) → PR2
    3. "CI blocks breaking changes" (vs master, label override) → PR2
    4. "Spec mirrored to ApiCurio via GitOps on merge" → PR3
  The doc's one deliberate choice — fixed meaningless version `0.0.0` to avoid
  unrelated PRs colliding on a version line — is exactly what PR1 implements.
  No daylight between doc and PRs. Doc itself is approvable as-is; only nit is
  it omits the operational caveats the PRs surface (merge order, the manual
  required-status-check swap, cross-repo canary-kubernetes dependency).

  ### The 3 PRs (stacked, all by arihantdaga, base master)
  - **PR1 #47537** — Foundation: per-service generation + service discovery, commits initial specs. +10864/-29, 20 files. Stacked base for PR2.
    https://github.com/canary-technologies-corp/canary/pull/47537
  - **PR2 #47538** — CI cutover: new unified `openapi_ci.yml` (staleness + stability), deletes old per-service specs/checks. +287/-5362, 14 files. Stacked on PR1.
    https://github.com/canary-technologies-corp/canary/pull/47538
  - **PR3 #47539** — GitOps publish to Apicurio: `openapi_publish.yml`, modeled on the Kafka Avro schema sync. +285, 1 file. Stacked on PR2.
    https://github.com/canary-technologies-corp/canary/pull/47539

  ### Overall assessment
  High quality. Descriptions are unusually thorough and self-aware; the design
  is sound (determinism-pinned serialization, discovery-driven matrix with no
  hardcoded service names, an always-running gate job that solves the
  "skipped required check leaves PR pending" problem, and a publish path that
  reuses the trusted Kafka GitOps trust model — no direct REST writes). Good
  unit-test coverage on the discovery script (incl. a real-tree pin test).
  I'd approve PR1 and PR3; PR2 is the one to scrutinize (it deletes 5.3k lines
  and changes required-check semantics).

  ### Things to verify / call out before merging
  1. **Read the Notion doc yourself** — I couldn't (auth). Confirm the 4 steps map as the PRs claim.
  2. **Merge order is load-bearing** (from the PR bodies, worth confirming with Arihant):
     - PR1 → PR2 → PR3, in order.
     - PR2's stability baseline reads `origin/master:<service>.yml`, which only
       exists once PR1 lands (self-skips until then — so PR2's own stability leg
       is unexercised on its CI; fine but means less signal).
     - PR3 requires the **canary-kubernetes ingestion PR**
       (`arihantdaga/ee-1340-apicurio-openapi-ingestion`, adds
       `apps/external/apicurio/openapi/` + helmfile ingestion) to merge FIRST,
       else mirrored files aren't ingested. Confirm that PR exists/is ready.
  3. **PR2 manual repo setting (not in any diff):** required status checks in
     branch protection / merge queue. The removed job names (canary
     `check-openapi-stability`, task-management/credential-manager
     `openapi-check`) must be swapped for the new `OpenAPI specs` gate context.
     If skipped, a required check disappears and either blocks or silently stops
     gating. This is the highest-risk human step in the whole stack.

  ### Minor / nits (non-blocking)
  - `discover_services.py::_spec_command` special-cases the literal
    `"credential-manager"` name to pick `generate_openapi_merged`. Mild tension
    with the PR's "no service names hardcoded" goal — would be cleaner as a flag
    in that service's `internal-service.yml` (e.g. `openapi_merge_legacy: true`).
    Acceptable as-is given it's one service; worth a one-line note.
  - PR3 mirror does `find -maxdepth 1 -name '*.yml' -delete` then copies by
    basename into a flat dir — correct only while all `<name>.yml` are unique
    (they are). README.md survives by design (verified in the diff). Fine, but
    a future same-named spec in a subdir would silently collide.
  - merge_group caveat (preserved from old job): the
    `api:breaking-change-approved` bypass label can't apply inside the merge
    queue because `github.event.pull_request` is empty there. Documented and
    matches prior behavior — relies on the label clearing the PR's own checks
    before it enters the queue. No change needed, just be aware.

  ### Suggested reply to Arihant (NOT yet sent — needs your approval to post)
  > Reviewed the 3 PRs end-to-end — design is solid, descriptions are great.
  > Approving PR1 + PR3. Two things before we land PR2: (1) confirm the required
  > status checks in branch protection get swapped from the old job names to the
  > new "OpenAPI specs" gate, and (2) confirm the canary-kubernetes ingestion PR
  > is ready to merge first. One nit on PR1: the credential-manager special-case
  > in discover_services could be a flag in internal-service.yml instead of a
  > name check.

  I did NOT post anything to Slack or GitHub. Let me know if you want that reply sent.
project: null
source_id: null
tags: []
time_minutes: 5
title: review document and overview PRs
updated: 2026-06-15 13:18:00.000000
waiting_on: null
waiting_since: null
working_on: false
---

https://canarytechnologies.slack.com/archives/C0ACQT82JLA/p1781511958676179