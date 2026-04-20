#!/usr/bin/env bash
# Run backend + frontend test coverage and print a combined summary.
# Usage: ./scripts/coverage.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== backend coverage (pytest-cov) ==="
uv run pytest \
  --cov=gtd_core --cov=gtd_api \
  --cov-report=term \
  --no-header -q

echo
echo "=== frontend coverage (vitest v8) ==="
cd frontend
npm test -- --coverage --reporter=dot
