# gtd

Local GTD (Getting Things Done) system backed by markdown + YAML frontmatter
files. Two interfaces on top of a single service layer: a Django + DRF API
with a React frontend, and direct file access for Claude Code CLI sessions.

## Setup

Requires Python 3.13 (managed by [uv](https://docs.astral.sh/uv/)) and Node 20+.

```sh
# Python
uv sync

# Frontend
cd frontend && npm install && cd ..
```

## Run locally

```sh
# Build frontend once
cd frontend && npm run build && cd ..

# Start the Django server (serves API + built frontend)
uv run manage.py runserver 8765
```

For frontend hot-reload during development, run Vite dev server alongside:

```sh
# Terminal 1
uv run manage.py runserver 8765

# Terminal 2
cd frontend && npm run dev
```

## Snapshot (commit data changes)

```sh
uv run manage.py snapshot                  # auto-generated message
uv run manage.py snapshot -m "weekly review"
uv run manage.py snapshot --push           # also push to origin
```

## Tests

```sh
uv run pytest
```

## Data layout

All GTD data lives under `data/`:

```
data/
├── work/
│   ├── config.yml
│   ├── inbox/
│   ├── next/
│   ├── waiting/
│   ├── someday/
│   ├── reference/
│   ├── archive/
│   ├── trash/
│   ├── projects/      # not a bucket — projects live here
│   └── templates/     # not a bucket — recurring templates
└── home/
    └── ...
```

Each item is one markdown file. See `gtd_core/models.py` for the full schema.

## Features

- **Capture**: quick text capture (`C`) or AI capture (`A`) — AI mode shells
  out to the `claude` CLI to extract title, contexts, project, etc. from
  unstructured text.
- **Inline editing**: items expand into live editors that auto-save via
  debounced PATCH. No Save button.
- **Full-text search**: client-side MiniSearch index over the whole corpus
  including archive and trash.
- **Recurring templates**: files in `data/<env>/templates/` spawn inbox
  items on a schedule (daily / weekly / monthly / …). Triggered on every
  snapshot.
- **Per-project next-action cap** (`max_next_items`): `1` = classic
  sequential (one step at a time), `N` = surface N steps, `null` = no cap.
  Drag-and-drop reorders.
- **Project priority + due date** (priority 1 = most urgent … 5 =
  aspirational). The projects tab sorts by priority, then due date.
- **Natural-language dates** on item `due` / `defer_until` (e.g. "next
  friday", "2w", "end of month", "in 2 hours").

## Architecture

- `gtd_core/` — self-contained Python library: models, storage, repository,
  service, snapshot. No Django/HTTP knowledge. Usable directly from scripts
  and CLI sessions.
- `gtd_api/` — thin DRF layer: serializers + views that call `gtd_core`.
- `frontend/` — Vite + React + TypeScript SPA.
- `gtd_site/` — Django project glue.

Each layer has its own `CLAUDE.md` with deeper conventions.
