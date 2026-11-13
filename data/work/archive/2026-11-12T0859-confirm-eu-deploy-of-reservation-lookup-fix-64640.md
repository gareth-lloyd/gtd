---
area: null
completed_at: 2026-11-12 10:55:28.505446
contexts:
- react
created: 2026-11-12 08:59:20.657356
defer_until: null
due: 2026-11-12
energy: medium
id: 2026-11-12T0859-confirm-eu-deploy-of-reservation-lookup-fix-64640
order: null
output: |
  ## Agent run 2026-11-12T09:12Z

  **EU has the fix.** Ishwar re-ran the deploy for eu-central-1 only, two minutes after reporting the failure, and it succeeded. Nothing for you to do.

  Evidence, in order:
  - Failed run: "Deploy Production - All Regions" (https://github.com/canary-technologies-corp/canary/actions/runs/43166907195), started 06:15 UTC. us-west-2 and ap-southeast-1 deployed; only `deploy-eu-central-1 / gitops-commit` failed, at 06:36 UTC.
  - Cause: the runner could not reach GitHub to download actions ("Failed to resolve action download info", three attempts). A transient runner network fault, not a problem with the change. EU pre-deploy and migrations had already passed.
  - Retry: EU-only run by Ishwar (https://github.com/canary-technologies-corp/canary/actions/runs/43170056914), started 06:42 UTC, all jobs green, gitops-commit succeeded 06:53 UTC. Release v2026.39.61, master SHA d28c5c6805.
  - Gitops repo: canary-kubernetes commit 843ebf9873 "[BOT] Deploy production canary eu-central-1 v2026.39.61" at 06:53:12 UTC. `values/production/eu-central-1.yaml` now pins django digest `d28c5c6805...@sha256:e9dc224d...`.
  - Live cluster (Groundcover, prod-main-eu-central-1): the two running django pods I sampled run image digest sha256:e9dc224d..., matching the release. The oldest running django pod was created 06:54:08 UTC, so no pod predates the rollout.

  What d28c5c6805 contains (all three verified as ancestors or the SHA itself):
  - PR #64640 (https://github.com/canary-technologies-corp/canary/pull/64640): refuse anonymous lookups at hotels with no guest product.
  - PR #64645 (https://github.com/canary-technologies-corp/canary/pull/64645): narrows the gate to check-in or compendium hotels, after SJ's challenge in the thread.
  - PR #64650 (https://github.com/canary-technologies-corp/canary/pull/64650): gates the upsell lookup link the same way. It is the head commit of the deploy.

  So all three regions run the same code. US and AP are on release tag v2026.39.60, EU on v2026.39.61; both tags were built from d28c5c6805.

  Not verified:
  - I did not call the EU endpoint to see a 404. The check is on deployed image, not behaviour.
  - I sampled 2 of 10 running django pods for the digest; the rest are inferred from creation times.
  - Nobody posted in the Slack thread that EU was fixed. The last deploy message there is still Ishwar's "gitops-commit failed" at 06:40 UTC (https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794465649157039?thread_ts=1794453425.407239&cid=C0CFU7HBZEK). The thread ends with Z saying the properties are in Nashville (US), so the customer reply did not depend on EU.

  Optional, as IC: a one-line reply in the thread closing the loop. Draft, not sent:
  > Confirming EU: the eu-central-1 retry (run 43170056914) succeeded at 06:53 UTC and EU django pods are on d28c5c6805 (v2026.39.61), so all three regions have #64640, #64645 and #64650. The first failure was the gitops runner failing to download actions.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794458611900899?thread_ts=1794453425.407239&cid=C0CFU7HBZEK
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Confirm EU deploy of reservation-lookup fix #64640 landed (SEC-1762)'
updated: 2026-11-12 10:55:28.505442
waiting_on: null
waiting_since: null
working_on: false
---

Ishwar asked me for a review; PR merged 05:03 UTC without me. But he reported the EU gitops-commit FAILED on deploy at 06:40 UTC (US went out manually). I am Incident Commander shift 2 from today - verify EU has the fix.
https://canarytechnologies.slack.com/archives/C0CFU7HBZEK/p1794458611900899?thread_ts=1794453425.407239&cid=C0CFU7HBZEK