#!/usr/bin/env bash
# Fresh-clone setup: install Python + frontend deps and the pre-commit hook.
# Usage: ./scripts/setup-dev.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== uv sync ==="
uv sync

echo
echo "=== npm install (frontend) ==="
(cd frontend && npm install)

echo
echo "=== pre-commit install ==="
uv run pre-commit install

echo
echo "Setup complete. Run ./scripts/lint.sh to verify."
