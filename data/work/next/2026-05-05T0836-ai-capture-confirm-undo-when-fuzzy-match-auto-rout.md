---
area: engineering
contexts: []
created: 2026-05-05 08:36:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T0836-ai-capture-confirm-undo-when-fuzzy-match-auto-rout
order: null
project: 2026-04-27-gtd
source_id: null
tags: []
time_minutes: 45
title: 'AI capture: confirm/undo when fuzzy-match auto-routes'
updated: 2026-05-05 15:05:42.851088
waiting_on: null
waiting_since: null
working_on: false
---

`capture_ai` resolves freeform project titles with `difflib.get_close_matches(cutoff=0.6)`. If a match is found, the item auto-moves from inbox to next, skipping review. Cutoff 0.6 is loose — silent miscategorization is real.

Options:
- Raise the cutoff (0.8?) and require human confirm at lower   confidence.
- Always land in inbox; just *suggest* the project; user moves   with one click.
- Surface confidence score + an inline "undo / move back to   inbox" in the response toast.