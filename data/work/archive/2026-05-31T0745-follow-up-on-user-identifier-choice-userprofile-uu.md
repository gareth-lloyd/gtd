---
area: null
contexts:
- react
created: 2026-05-31 07:45:57.285116
defer_until: null
due: null
energy: low
id: 2026-05-31T0745-follow-up-on-user-identifier-choice-userprofile-uu
order: null
output: |
  ## Agent run 2026-06-02T13:40

  ### Decision: use `UserProfile.uuid` (NOT `username:email`)

  Recommendation is unambiguous after grounding in code. The current
  `username:email` reference is the wrong key for the OAuth global-login
  identity, and the code already half-knows it.

  ### The smoking gun: code contradicts its own comment
  `backend/canary/hotels/views/views.py:494-496`:
  ```python
  # userprofile.uuid is stable + globally unique; username/email (mutable)
  # or user.pk (region-ambiguous) would break the identity dedup contract.
  reference = StaffUserReference(username=str(user.username), email=str(user.email))
  ```
  The comment justifies uuid; the line below it uses username:email. This is
  almost certainly the residue of Andrea's rebase ("I believe we originally
  used uuid and then changed when I rebased") — the uuid rationale survived,
  the implementation reverted. Note `user.userprofile.uuid` is already loaded
  10 lines up (views.py:479) to verify the profile exists, so the better key
  is already in hand.

  ### Why username:email is unsafe as the identity key
  The identity_sid is a *deterministic hash of (type, reference)* —
  `IdentitySid.hash_of(type, str(reference))` in
  `api_gateway/services/identity_service.py:95`. So the reference MUST be
  stable + globally unique, and username:email is neither:
  - **Mutable** → breaks stability. Change a username or email and the sid
    changes, orphaning every OAuth grant pointing at the old sid. They already
    got bitten by the milder version of this (casing/whitespace drift in prod,
    patched by normalization PR #46698) — that's a band-aid on a mutable key,
    not a fix.
  - **Not globally unique** → username is unique only *per region* (Django
    auth_user constraint is per-DB). Two different humans can share the same
    username:email across regions → sid collision → identity confusion. This
    is exactly the "dupes across region" Jordan found in his sheet.

  `UserProfile.uuid` (`hotels/models/user_profile.py:40`,
  `UUIDField(default=uuid4, editable=False, unique=True)`) is immutable and
  globally unique by construction — both properties the dedup contract needs.

  ### The one real open question (worth a sentence back to Jordan/Andrea)
  uuid is generated *per row*. If the SAME human has independent UserProfile
  rows in multiple regions, those rows carry DIFFERENT uuids — so uuid alone
  won't recognize them as one person either. BUT: username:email "solves" that
  only by accidental string-matching, unreliably (the casing/mutability bugs
  above), and that accidental matching is the very source of the collisions.
  The clean design is one global identity per human keyed on a stable uuid,
  with the global user table (the one ENT is building anyway) mapping uuid →
  regional accounts. So the cross-region-same-human concern is an argument FOR
  a deliberate uuid-keyed global mapping, not for keeping the fragile composite.

  ### Cost of switching: low — do it now
  Blast radius is tiny. Only producer is views.py:496; reference shape is
  `StaffUserReference` in identity_service.py; no resolver consumes the
  reference yet (cross-region lookup is still ~2 weeks of unstarted work per
  Jordan). Changing now = edit StaffUserReference to carry uuid + the one call
  site. Caveat: any identity records / OAuth grants already minted with
  username:email would need re-minting/backfill — cheapest to do before the
  resolver lands and before more prod data accrues.

  ### Suggested next step (NOT yet done — needs your go-ahead)
  1. Reply in the group DM confirming the decision (draft below).
  2. File/assign a ticket to swap StaffUserReference → uuid + backfill existing
     identity records.

  Draft Slack reply (NOT sent — say the word and I'll post it):
  > Decision: switch to UserProfile.uuid. The identity_sid is a deterministic
  > hash of the reference, so the key has to be stable + globally unique —
  > username:email is mutable (the casing fix in #46698 is a band-aid) and
  > username is only unique per-region, which is where the cross-region dupes
  > come from. The view comment already argues for uuid; the rebase just
  > dropped the implementation. uuid is already loaded in the view to null-check
  > the profile. Resolver isn't built yet so the swap is cheap now — only cost
  > is re-minting the identity records already written with username:email.

  NOTE: I did not edit code or post to Slack — recommendation only, per scope.
project: null
source_id: https://canarytechnologies.slack.com/archives/C0B5597H1FC/p1780062405631419
tags:
- morning-gtd
- slack
time_minutes: 10
title: 'Follow up on user-identifier choice: UserProfile.uuid vs username:email (cross-region)'
updated: 2026-06-02 13:34:05.425058
waiting_on: null
waiting_since: null
working_on: false
---

Group DM with Andrea & Jordan: Jordan flagged that CONCAT(username, ':', email) isn't unique cross-region; uuid likely better. Decide on the identifier.
https://canarytechnologies.slack.com/archives/C0B5597H1FC/p1780062405631419