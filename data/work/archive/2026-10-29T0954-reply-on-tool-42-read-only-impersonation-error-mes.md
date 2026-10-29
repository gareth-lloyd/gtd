---
area: null
completed_at: 2026-10-29 13:25:36.176116
contexts:
- react
created: 2026-10-29 09:54:57.204201
defer_until: null
due: null
energy: low
id: 2026-10-29T0954-reply-on-tool-42-read-only-impersonation-error-mes
order: null
output: |
  ## Agent run 2026-10-29T13:27
  Read TOOL-42 (https://linear.app/canary-technologies/issue/TOOL-42/intercept-and-display-clear-message-for-read-only-impersonation-errors) and João Bueno's comment (https://linear.app/canary-technologies/issue/TOOL-42/intercept-and-display-clear-message-for-read-only-impersonation-errors#comment-521862a7). It links TIP-5594 (https://linear.app/canary-technologies/issue/TIP-5594/self-serve-contractor-error-when-adding-contractor). No reply has been posted, and none will be until you approve the exact text.

  Code checked on master:
  - backend/canary/impersonation/middleware.py:118 and :125 return a bare `HttpResponseForbidden()`, so the response has no body and no error code.
  - frontend/hotels/src/App.vue:167 already registers a global axios response interceptor that branches on `error_code` (NO_HOTEL_ACCESS, MFA_NOT_COMPLETED). That is the hook to extend.

  DRAFT REPLY (not posted):
  ---
  Thanks @jbueno, this is exactly the failure the ticket describes, and the trace makes the fix concrete.

  Proposed shape:
  1. Backend: `ImpersonateMiddleware.process_view` returns a JSON 403 with `{"error_code": "impersonation_read_only"}` in both forbidden branches, instead of the empty `HttpResponseForbidden()`.
  2. Frontend: the hotels app's global axios interceptor (`frontend/hotels/src/App.vue`) already branches on `error_code`. It adds a case for 403 + `impersonation_read_only` that shows one toast: "You're impersonating in read-only mode. Restart impersonation with write access to make changes."

  That covers every write endpoint at once, including the wallets modal, with no per-view changes. One catch: the modal would still show its own generic toast as well. Either the interceptor marks the error as handled, or we accept two toasts for now.
  ---

  Note: when this run started, the item had already been moved to archive/ with completed_at 13:25:36. I left it there and only edited output/working_on/updated.
project: null
source_id: https://linear.app/canary-technologies/issue/TOOL-42/intercept-and-display-clear-message-for-read-only-impersonation-errors#comment-521862a7
tags:
- morning-gtd
- linear
time_minutes: 10
title: 'Reply on TOOL-42: read-only impersonation error messaging'
updated: 2026-10-29 13:27:30.000000
waiting_on: null
waiting_since: null
working_on: false
---

jbueno added the Oct 28 incident (TIP-5594): a staff user impersonating in read-only mode hit an unclear error adding a contractor.
https://linear.app/canary-technologies/issue/TOOL-42/intercept-and-display-clear-message-for-read-only-impersonation-errors