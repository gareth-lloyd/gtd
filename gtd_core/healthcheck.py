"""Runtime health and startup self-check for the GTD service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class HealthInfo:
    data_root: Path
    envs: list[str]


def collect_health() -> HealthInfo:
    """Snapshot GTD_DATA_ROOT and enumerate available envs.

    An env is any directory under the data root containing a ``config.yml``.
    Safe to call regardless of whether the data root exists — missing roots
    return an empty env list rather than raising.
    """
    from django.conf import settings

    root = Path(settings.GTD_DATA_ROOT)
    envs: list[str] = []
    if root.exists():
        for child in sorted(root.iterdir()):
            if child.is_dir() and (child / "config.yml").exists():
                envs.append(child.name)
    return HealthInfo(data_root=root, envs=envs)


def verify_data_root() -> HealthInfo:
    """Refuse to start if the data root is missing or empty.

    Called from ``scripts/gunicorn_config.py`` on the master process before
    workers fork, so a wrong/stale ``GTD_DATA_ROOT`` surfaces immediately
    instead of silently writing to the wrong filesystem location.
    """
    info = collect_health()
    if not info.data_root.exists():
        raise RuntimeError(
            f"GTD_DATA_ROOT does not exist: {info.data_root}. "
            "Refusing to start — check the LaunchAgent plist or your env."
        )
    if not info.envs:
        raise RuntimeError(
            f"GTD_DATA_ROOT exists but has no env configs: {info.data_root}. "
            "Expected at least one subdirectory containing config.yml."
        )
    return info
