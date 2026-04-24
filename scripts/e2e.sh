#!/usr/bin/env bash
# Run the Playwright e2e suite against a throwaway Django env.
# Usage: ./scripts/e2e.sh            # headless
#        ./scripts/e2e.sh --ui       # Playwright UI mode
#        ./scripts/e2e.sh --debug    # Playwright inspector
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/frontend"

echo "=== building frontend ==="
npm run build

echo "=== running Playwright ==="
npx playwright test "$@"
