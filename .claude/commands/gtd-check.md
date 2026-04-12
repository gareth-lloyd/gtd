# GTD Dev Check

Run the full validation pipeline before committing code changes.

## Steps

Run these in sequence, stopping at the first failure:

1. **Lint**: `uv run ruff check .`
2. **Tests**: `uv run pytest`
3. **Frontend build**: `cd frontend && npm run build`

Report pass/fail for each step. If all pass, say "All clear — safe to commit."

If any step fails, show the error output and suggest a fix.
