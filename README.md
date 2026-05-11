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

## Run as a background service (macOS)

Once GTD has earned a place in your daily workflow, install it as a
per-user `LaunchAgent` so it starts at login and auto-restarts on crash.

```sh
make install-service     # installs + starts + verifies via /api/health/
make service-status      # launchd status + health snapshot
make service-logs        # tail error + launchd stderr
make restart-service     # kick the service after manual config changes
make rebuild-frontend    # rebuild SPA and restart in one shot
make uninstall-service   # stop + remove
```

Internals: `scripts/serve.sh` runs gunicorn (1 worker, 4 threads) against
`gtd_site.wsgi`, with logging routed through Django's `LOGGING` to
`logs/{gtd,access,error}.log` (rotated, 10 MB × 5 each).
`scripts/gtd.plist.template` is rendered into
`~/Library/LaunchAgents/com.glloyd.gtd.plist` at install time with absolute
paths. The plist's `KeepAlive.Crashed=true` + `ThrottleInterval=10` give
crash recovery without restart-loop thrash.

Bind is `127.0.0.1:8765` only — service is reachable from this Mac alone.

The active dev workflow (`runserver` + `npm run dev`) is unchanged and still
recommended for code work; the service is for everyday usage.

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
