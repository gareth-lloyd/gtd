#!/usr/bin/env bash
# Production-style entry point for the GTD service. Used by the LaunchAgent
# and by `make serve` for foreground debugging.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p logs

# Build the frontend if dist/ is missing (fresh checkout / after a clean).
if [ ! -d frontend/dist ]; then
  echo "frontend/dist missing — building..."
  (cd frontend && npm install && npm run build)
fi

HOST="${GTD_HOST:-127.0.0.1}"
PORT="${GTD_PORT:-8765}"

exec uv run gunicorn gtd_site.wsgi:application \
  --config scripts/gunicorn_config.py \
  --bind "${HOST}:${PORT}" \
  --workers 1 \
  --threads 4 \
  --timeout 60 \
  --graceful-timeout 30 \
  --max-requests 1000 \
  --max-requests-jitter 100
