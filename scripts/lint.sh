#!/usr/bin/env bash
# Run lint + format + typecheck across backend and frontend.
# Usage: ./scripts/lint.sh
#
# Steps run in fail-fast order. Each step is fast (<5s after warmup).
# Frontend type-checking can be skipped with SKIP_TYPECHECK=1 if needed.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

step() {
  printf '\n=== %s ===\n' "$1"
}

step "ruff check"
uv run ruff check .

step "ruff format --check"
uv run ruff format --check .

if [[ "${SKIP_TYPECHECK:-0}" != "1" ]]; then
  step "pyright"
  uv run pyright
fi

step "frontend eslint"
(cd frontend && npm run --silent lint)

step "frontend prettier --check"
(cd frontend && npm run --silent format:check)

if [[ "${SKIP_TYPECHECK:-0}" != "1" ]]; then
  step "frontend tsc --noEmit"
  (cd frontend && npm run --silent typecheck)
fi

echo
echo "All clear."
