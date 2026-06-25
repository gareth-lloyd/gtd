---
area: null
contexts: []
created: 2026-06-24 20:53:36.990441
defer_until: null
due: null
energy: low
id: 2026-06-24T2053-examine-whether-it-s-a-security-flaw-to-open-up-us
order: null
output: |
  ## Agent run 2026-06-24T22:45:00

  **Verdict: NOT a security flaw.** Opening usernames for re-use, as implemented, is
  sound. User identity is anchored on the immutable primary key everywhere it matters,
  so a re-used username string inherits nothing from the previous holder. The genuine
  residual risk is human-layer impersonation confusion, which the code already has a
  detective control for.

  ### How re-use works
  `HotelStaffUserService._delete_user` (backend/canary/hotel_staff/services/hotel_staff_user.py:737)
  does NOT hard-delete. It:
  - renames `username` -> `{username}__deactivated_{user_id}` (get_deactivated_username, :722)
  - sets `is_active=False`
  - revokes all roles (`RoleService.remove_all_user_roles`)
  - for SSO users, deletes their CompanyHotelUser rows
  The row, its PK, and all FK relationships are kept (audit trail intact). The original
  username string is freed for a new user to register. SSO users cannot be deleted at all
  (CannotDeleteSsoUser, delete_user:676) — this closes the external-IdP identity-reuse hole.

  ### Why it's safe (verified, with file:line)
  1. Identity = immutable PK, not the username string. A re-used name produces a brand-new
     User row with a new PK; nothing the old user owned (roles, CompanyHotelUser, events,
     sessions) transfers.
  2. Username lookups rely on uniqueness, not is_active filtering:
     - find_user_by_username -> User.objects.get(username__iexact=...) (hotels/services/user.py:285)
     - get_user_by_username_case_insensitive -> same (shared/shared/utils/username.py:39)
     After the rename, only the NEW active user matches iexact="alice"; the old row is
     "alice__deactivated_42" and does not match. Correct because the rename preserves uniqueness.
  3. Password reset / account activation tokens are PK-bound, NOT username-bound. A random
     20-char key is stored in ResetSystemPassword with a FK to the user (UserPasswordService,
     hotels/services/user_password.py:40/63). A link issued for old alice resolves to her
     (now-inactive) PK; it can never set the new alice's password. No cross-contamination.
  4. Roles revoked on delete; new user starts with only newly granted roles — no permission
     inheritance.
  5. Sessions are keyed on user PK (Django _auth_user_id), unaffected by username changes.

  ### Existing detective control
  HotelStaffUserService._check_and_log_username_reuse (:270), called from create_user_profile
  (:310), logs `hotel_staff_user.username_reused_after_deletion` with a `same_email` flag
  whenever a previously-deactivated name is reclaimed. same_email=False is the impersonation
  signal. This is logging-only (not preventive) — appropriate, since the technical re-use is safe.

  ### Residual risks / recommendations (none block the feature)
  - IMPERSONATION (human layer, inherent to any reuse policy, not a code bug): a new employee
    re-registering a departed colleague's username could be socially mistaken for them. No
    technical access is gained — old creds/roles are gone. RECOMMEND: alert/monitor on the
    `username_reused_after_deletion` warning where same_email=False, so security can review.
    (Worth confirming an alert exists — the log line is only useful if something watches it.)
  - EXTERNAL SYSTEMS keyed on username string: I verified all *in-app* identity anchors are
    PK-based, and SSO (the main external-identity vector) is exempt from deletion. NOT
    exhaustively verified: whether any downstream integration (analytics, exported reports,
    log-based identity correlation) keys a *person* on the username string rather than user id.
    If one does, it could conflate two people. Low risk; worth a confirming check. (My broad
    grep for this was interrupted; flagging as the one unverified item.)
  - CASE-INSENSITIVITY / MultipleObjectsReturned (pre-existing, not introduced by reuse):
    iexact lookups assume at most one active match. Django's stock unique constraint on
    username is case-SENSITIVE at the DB level, so a case-variant pair (or a TOCTOU race on
    concurrent signup) could make these getters raise MultipleObjectsReturned. It fails closed
    (raises, no takeover), so this is a robustness note, not a security hole.
  - NO QUARANTINE/grace period (immediate reuse). Acceptable here precisely because nothing
    references the freed name — the risk a grace period would mitigate is already neutralized.

  Bottom line: ship-safe. The single concrete follow-up worth doing is an alert on
  same_email=False reuse; the external-system-keyed-on-username check is a nice-to-confirm.
project: null
source_id: null
tags: []
time_minutes: 5
title: examine whether it's a security flaw to open up usernames for re-use
updated: 2026-06-25 08:57:22.094042
waiting_on: null
waiting_since: null
working_on: false
---