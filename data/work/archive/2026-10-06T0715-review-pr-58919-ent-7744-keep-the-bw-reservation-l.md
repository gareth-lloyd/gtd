---
area: null
completed_at: 2026-10-06 13:37:23.051323
contexts:
- react
created: 2026-10-06 07:15:43.256784
defer_until: null
due: null
energy: medium
id: 2026-10-06T0715-review-pr-58919-ent-7744-keep-the-bw-reservation-l
order: null
output: |-
  ## Agent run 2026-10-06T09:50:59Z

  **Verdict: approve. No blocking defects found.** One question is worth asking Martin before merge (EU/AP queue timeouts), plus a few non-blocking notes. Nothing was posted to GitHub.

  PR #58919 (https://github.com/canary-technologies-corp/canary/pull/58919), head `c4093896ee`, 2 files, +60/-23. Ticket ENT-7744 (https://linear.app/canary-technologies/issue/ENT-7744). CI is green on the head commit; the only non-success check is Macroscope Approvability (NEUTRAL, "human required"). No human reviews yet; review is requested from you and pod-arrivals-departures. I did not run the tests locally.

  ### What the PR does
  1. Retry interval 900s -> 300s and max attempts 33 -> 97 (1 + 96 x 300s, the same ~8h horizon).
  2. Moves the `cache.add` claim from task entry to just before the next attempt is published.
  3. Splits the `cache.add` outcomes: `False` is a duplicate and stops; `None` (Redis down) logs `claim_failed` and publishes anyway.

  ### What I checked, and it holds
  - **The root-cause fix is right.** kombu 5.4.2 never passes a visibility timeout on receive, and `broker_transport_options["visibility_timeout"] = 120` (`canary/celery/celery.py:129`) does nothing with predefined queues, so the AWS queue attribute governs. FIFO queues cannot use per-message `DelaySeconds`, so the worker holds the ETA message, and with `task_acks_late` the ack comes after execution. A 300s hold plus the worst-case execution (4 BW POSTs at 10s timeout plus 7s of backoff, about 47s) sits well inside 600s. A queue backlog does not eat the margin, because the clock starts at receive.
  - **Worker shutdown does not create copies.** kombu restores an unacked SQS message by setting its visibility to 0, not by re-sending it.
  - **The `None`/`False` split is real.** django_redis `add` returns `bool(SET NX)`, and under `IGNORE_EXCEPTIONS` (`canary/settings/base.py:266`) a connection failure returns `None`. `DualWriteRedisCache` does not override `add`.
  - **Macroscope's concern is acceptable.** It flagged that a redelivered copy now runs the association before duplicate suppression. With no confirmation code, the attempt is a local DB read and makes no vendor call. With a code, the second copy re-POSTs, BW answers ERR.001, and `ReservationAlreadyAssociatedError` is caught as a `MembershipGatewayAPIError` at `check_in/services/check_in_membership.py:217`. The only cost is a misleading `try_associate_reservation.vendor_error` warning.
  - **The accepted residual risks are small.** A copy that claims and then dies before publishing strands the chain, but the window is now two adjacent statements. Redis down plus a double delivery publishes two successors, which needs two independent faults.
  - **Tests** cover all three claim outcomes and the claim placement.

  ### Raise with Martin
  1. **Question: what are the visibility timeouts on the EU and AP default queues?** The task runs on the default queue in every region, but the PR checks the number for `canary-celery-us.fifo` only. If another region's queue is under 300s, the doubling is still live there and only the claim holds it back. The 120 in `celery.py` and the "visibility timeout (120s)" comment in `segmentation/tasks.py` show that not every queue is 600s. I could not verify this: queue attributes are not in this repo.
  2. **Non-blocking: nothing enforces the invariant.** The safety of 300s rests on a comment that hardcodes "600s on canary-celery-us.fifo". If infra lowers the timeout, nothing fails. The ticket's acceptance says `duplicate_attempt` should stay at zero in steady state, so a Groundcover monitor on `retry_membership_reservation_association.duplicate_attempt` > 0 would be a cheap tripwire. Fine as a follow-up.
  3. **Nit:** the comment on `ASSOCIATION_RETRY_INTERVAL_SEC` is three lines and names a specific queue and number, which `python-comments.md` discourages (two lines at most, no hyper-specific current values).
  4. **Rollout FYI:** messages already in flight with a 900s countdown get double-delivered one last time, and the claim absorbs it. During the rolling deploy, or after a rollback, an old worker that receives attempt > 33 logs `.exhausted` and ends that chain early. At about one miss a day this is negligible, but a brief `.exhausted` blip is possible.

  ### Out of scope
  `CELERY_TASK_MAX_COUNTDOWN = 900` in `canary/executors.py` still exceeds both the 600s default-queue timeout and the 500s high-priority one. The ticket already notes this and that the executor appears unused in production.

  ### Draft review comment (not posted)
  > Approving. The 300s interval fixes the cause, and I'm fine with the claim guarding only the publish: a duplicate association is a local read when there's no code and an ERR.001 when there is.
  >
  > One question before merge: have you checked the visibility timeout on the EU and AP default queues? The task runs on the default queue in every region and the comment only cites canary-celery-us.fifo. If either is under 300s we still double-deliver there.
  >
  > Non-blocking: nothing fails if someone lowers the queue timeout later. A Groundcover monitor on `retry_membership_reservation_association.duplicate_attempt` > 0 would catch it, since that should now be zero in steady state. Happy for that to be a follow-up.
  >
  > Nit: the interval comment is three lines and pins a queue name and number that will go stale.
project: null
source_id: https://github.com/canary-technologies-corp/canary/pull/58919
tags:
- morning-gtd
- github
time_minutes: 20
title: 'Review PR #58919: ENT-7744 Keep the BW reservation-link retry inside the SQS
  visibility timeout'
updated: 2026-10-06 13:37:23.051310
waiting_on: null
waiting_since: null
working_on: false
---

https://github.com/canary-technologies-corp/canary/pull/58919
Author: martinrodriguezcanary. Branch: tinchomartinrodriguez/ent-7744-retry-interval-under-visibility-timeout. Personally requested 2026-10-05. This is the fix behind incident #300 (celery queue backlog from retries).