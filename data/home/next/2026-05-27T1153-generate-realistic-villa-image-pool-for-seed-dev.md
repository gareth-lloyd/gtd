---
area: null
contexts:
- computer
created: 2026-05-27 11:53:10.332102
defer_until: null
due: null
energy: medium
id: 2026-05-27T1153-generate-realistic-villa-image-pool-for-seed-dev
order: null
output: ''
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 180
title: Generate realistic villa image pool for seed_dev
updated: 2026-05-27 11:53:41.688781
waiting_on: null
waiting_since: null
working_on: false
---

Plan file: ~/.claude/plans/plan-the-generation-of-cuddly-candle.md

Link this item to project `2026-05-25-villa-collective` during /gtd-inbox processing.

## Goal
Replace the 1x1 `_tiny_png()` placeholders that seed_dev currently writes into every `PropertyImage` with a small but visually rich pool of generated villa imagery, so the dev UI looks like a real product instead of grey boxes.

## Approach
- **Generator**: Stability AI — Stable Diffusion 3 (or Ultra at ~$0.08/image; total cost stays well under $10 either way).
- **Image mix**: ~20 villas × 4 images each (HERO + INTERIOR + EXTERIOR + GALLERY) = ~80 images.
- **Storage**: plain git commit, downsized JPEGs (~1200 px wide, q≈80, ~150–250 kB each, total ~15–20 MB). No Git LFS.
- **Script**: committed Django management command `core/management/commands/generate_seed_images.py`, idempotent, driven by a YAML manifest of 20 villa concepts (Amalfi, Provence, Mykonos, Bali, Caribbean, etc.) each with 4 prompts plus a shared style preamble.
- **Wiring**: replace the single HERO write in `PropertyFactory.children` (`django_res/properties/factories.py:180`) with a loop over all four kinds, drawing from a round-robin pool of villa subdirectories. Keep `_tiny_png()` only as a defensive fallback for an empty pool.

## Files
- New: `django_res/core/seed_data/villa_images/manifest.yaml`
- New: `django_res/core/seed_data/villa_images/villa_NN_<slug>/{hero,interior,exterior,gallery}.jpg` (~80 files)
- New: `django_res/core/seed_data/villa_images/README.md`
- New: `django_res/core/management/commands/generate_seed_images.py`
- Edit: `django_res/properties/factories.py` — pool loader replaces `_tiny_png()` HERO write
- Maybe edit: `pyproject.toml` (PyYAML, confirm `requests`)

## Verification
1. Generate one villa with `--only villa_01_amalfi`; inspect the 4 outputs visually.
2. Full pass; confirm ~80 files, repo diff ≤ 25 MB.
3. Re-run; expect "skipped: 80, generated: 0" with no API calls (idempotency).
4. `uv run pytest properties/tests/test_factories.py` — adjust any assertion that pins exactly-one-image-per-property.
5. Drop dev DB, migrate, `seed_dev --scale small`; spot-check 4 PropertyImage rows per Property.
6. Boot frontend, confirm real villa imagery in property list + detail.

## Out of scope
Production media (S3/CDN), upload UI, floor plans (SD3 does them poorly), alt-text generation.

## Cost
~80 images × $0.04–$0.08 = $3–$7 for the one-off run. Stability API key in `STABILITY_API_KEY` env var.