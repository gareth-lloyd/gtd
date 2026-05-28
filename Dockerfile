# Cloud (mobile) image for Render. Runs the same Django code as local but with
# GTD_ROOT_URLCONF=gtd_site.urls_cloud so only the locked mobile API is mounted.
# The container is an ephemeral clone of this repo; captures are pushed back to
# GitHub (see scripts/render-entrypoint.sh) so data survives restarts.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    GTD_FRONTEND_DIR=/app/frontend-mobile/dist

# git: required for push-back. node: builds the mobile SPA.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# uv for Python dependency management (matches local workflow).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies BEFORE copying the source so a code-only change doesn't
# bust the (slow) dependency layers. Lockfiles change far less often than code.
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

COPY frontend-mobile/package.json frontend-mobile/package-lock.json frontend-mobile/
RUN cd frontend-mobile && npm ci

# Now the full repo, including .git — push-back needs a working tree + origin.
COPY . .

# Build the mobile SPA and collect static assets for WhiteNoise.
RUN cd frontend-mobile && npm run build
RUN uv run manage.py collectstatic --noinput

CMD ["./scripts/render-entrypoint.sh"]
