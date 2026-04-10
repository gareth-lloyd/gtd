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
uv run manage.py runserver
```

For frontend hot-reload during development, run Vite dev server alongside:

```sh
# Terminal 1
uv run manage.py runserver

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
│   ├── projects/
│   └── archive/
└── home/
    └── ...
```

Each item is one markdown file. See `gtd_core/models.py` for the full schema.

## Architecture

- `gtd_core/` — self-contained Python library: models, storage, repository,
  service, snapshot. No Django/HTTP knowledge. Usable directly from scripts
  and CLI sessions.
- `gtd_api/` — thin DRF layer: serializers + views that call `gtd_core`.
- `frontend/` — Vite + React + TypeScript SPA.
- `gtd_site/` — Django project glue.
