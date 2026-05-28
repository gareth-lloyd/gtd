"""Gunicorn configuration for the GTD service.

Reuses Django's ``LOGGING`` dict so gunicorn's access/error logs land in the
same rotating files as the rest of the app, and runs a startup self-check
that refuses to boot against a missing/empty GTD_DATA_ROOT.
"""

from __future__ import annotations

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gtd_site.settings")
django.setup()

from django.conf import settings  # noqa: E402

from gtd_core.healthcheck import verify_data_root  # noqa: E402

logconfig_dict = settings.LOGGING


def on_starting(server) -> None:  # pyright: ignore[reportMissingParameterType]
    info = verify_data_root()
    server.log.info(
        "GTD service starting — data_root=%s envs=%s",
        info.data_root,
        ",".join(info.envs),
    )
    # cloud_sync serializes git ops with an in-process lock, which only works
    # with a single worker. More than one worker means separate processes
    # racing on the same .git index — surface that misconfiguration loudly.
    if settings.GTD_CLOUD_SYNC and server.cfg.workers > 1:
        server.log.error(
            "GTD_CLOUD_SYNC=1 requires --workers 1 (got %s); concurrent git ops "
            "across processes will corrupt the working tree.",
            server.cfg.workers,
        )
