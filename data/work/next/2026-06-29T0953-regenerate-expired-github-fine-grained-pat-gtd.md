---
area: null
completed_at: null
contexts:
- autopilot
created: 2026-06-29 09:53:21.810051
defer_until: null
due: null
energy: low
id: 2026-06-29T0953-regenerate-expired-github-fine-grained-pat-gtd
order: null
output: |-
  ## Agent run 2026-09-11T08:50:32Z

  **Not regenerated — needs you (5 min).** Regenerating a PAT requires the GitHub web UI while signed in, and the new value has to be pasted into Render's dashboard. The Render CLI on this machine is logged out (`render whoami` → unauthorized), so I couldn't check or change the service from here either.

  ### What the "gtd" PAT is actually used for
  Only one place: the **Render `gtd-mobile` service** (render.yaml:35, `GITHUB_TOKEN`, `sync: false`, so it's set by hand in the dashboard). `scripts/render-entrypoint.sh` uses it to (a) fetch/align to origin/main on boot and (b) push mobile captures back to `gareth-lloyd/gtd`. It needs **Contents: read & write** on that repo.

  Local tooling is **not** affected:
  - The `origin` remote is SSH (`git@github.com:gareth-lloyd/gtd.git`), so `snapshot --push` and the Sync button don't use the PAT.
  - `gh` is logged in via the keyring with a classic OAuth token (repo, read:org, gist), not this fine-grained PAT.
  - CI (`.github/workflows/ci.yml`) references no secrets.

  ### Impact so far
  The token expired on 2026-06-28 (GitHub email: https://mail.google.com/mail/u/0/#inbox/19f0ca2fd1f4a81e). Since then, every boot of the Render container will fail its `git fetch` (it logs a warning and serves build-time data) and mobile captures can't push. The capture endpoint returns `synced:false` in that case (gtd_api/mobile_views.py:121-129). Because the container filesystem is ephemeral, any mobile capture since 2026-06-28 is probably lost.

  Usage looks negligible, though: origin/main has only **one** `gtd-mobile` commit ever (515aab94, 2026-05-29, "mobile capture: Hi", which looks like a test) and none since the expiry. It's worth deciding whether to keep the mobile service at all, rather than rotating by reflex.

  ### Steps if you keep it
  1. Open https://github.com/settings/personal-access-tokens/15189825/regenerate, pick a new expiry (a longer one, or no expiry, avoids a repeat of this item), and confirm the scope is still repo `gareth-lloyd/gtd`, Contents: Read and write. Copy the token.
  2. Render dashboard → service `gtd-mobile` → Environment → set `GITHUB_TOKEN` to the new value → Save. This triggers a redeploy. While you're there, check that `GTD_GIT_REMOTE` = `gareth-lloyd/gtd`.
  3. Verify: the deploy logs should *not* show "could not align to origin/main". Then do a test capture from the phone. It should return `synced:true` and a `mobile capture:` commit authored by `gtd-mobile` should appear on origin/main.
  4. Optional: run `render login` so a future agent run can check the service/logs itself.

  ### Steps if you drop it
  Suspend or delete the `gtd-mobile` service in Render and let the PAT stay expired (or delete it at https://github.com/settings/personal-access-tokens).
project: 2026-04-27-gtd
source_id: https://mail.google.com/mail/u/0/#inbox/19f0ca2fd1f4a81e
tags:
- morning-gtd
- gmail
time_minutes: 5
title: Regenerate expired GitHub fine-grained PAT (gtd)
updated: 2026-09-11 11:50:32.000000
waiting_on: null
waiting_since: null
working_on: false
---

My 'gtd' fine-grained PAT expired (GitHub email). Regenerate so GTD tooling keeps working. https://mail.google.com/mail/u/0/#inbox/19f0ca2fd1f4a81e