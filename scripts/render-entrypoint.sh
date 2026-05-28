#!/usr/bin/env bash
# Render container entrypoint. Configures git for push-back, aligns the working
# tree to the latest origin/main, then hands off to gunicorn.
#
# Required env (set in render.yaml / Render secrets):
#   GITHUB_TOKEN        PAT with contents:write on the repo
#   GTD_GIT_REMOTE      owner/repo (e.g. "garethlloyd/gtd")
#   GTD_GIT_USER_NAME   commit author/committer name
#   GTD_GIT_USER_EMAIL  commit author/committer email
set -euo pipefail

REPO_DIR=/app
BRANCH=main

git config --global --add safe.directory "$REPO_DIR"
git config --global user.name "${GTD_GIT_USER_NAME:-gtd-mobile}"
git config --global user.email "${GTD_GIT_USER_EMAIL:-gtd-mobile@users.noreply.github.com}"

if [[ -n "${GITHUB_TOKEN:-}" && -n "${GTD_GIT_REMOTE:-}" ]]; then
  git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GTD_GIT_REMOTE}.git"
  # Align to the latest remote state. The container filesystem is ephemeral, so
  # durability relies on captures having been pushed to origin — the capture
  # endpoint returns `synced:false` when a push fails so the client knows the
  # item isn't yet durable. This alignment is best-effort: a transient fetch
  # failure must not crash-loop the service, which already has a working tree
  # (and committed data/) baked into the image at build time.
  if git fetch origin "$BRANCH" && git checkout -B "$BRANCH" "origin/$BRANCH"; then
    git branch --set-upstream-to="origin/$BRANCH" "$BRANCH"
  else
    echo "WARNING: could not align to origin/$BRANCH — serving build-time data." >&2
  fi
else
  echo "WARNING: GITHUB_TOKEN/GTD_GIT_REMOTE unset — git push-back disabled." >&2
fi

# --no-sync: deps are already installed in the image; don't re-resolve against
# the network (or fail on a read-only fs) on every boot.
exec uv run --no-sync gunicorn gtd_site.wsgi:application \
  --config scripts/gunicorn_config.py \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 1 \
  --threads 4 \
  --timeout 60
