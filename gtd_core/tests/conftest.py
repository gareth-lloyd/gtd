from pathlib import Path

import pytest


ALL_BUCKETS = [
    "inbox", "next", "waiting", "someday", "reference",
    "projects", "archive", "trash", "templates",
]

DEFAULT_CONFIG = (
    "contexts: [calls, computer, errands, office]\n"
    "areas: [engineering, health]\n"
    "default_energy: medium\n"
)


def make_env(
    root: Path,
    name: str,
    config_yaml: str = DEFAULT_CONFIG,
) -> Path:
    env_dir = root / name
    for bucket in ALL_BUCKETS:
        (env_dir / bucket).mkdir(parents=True, exist_ok=True)
    (env_dir / "config.yml").write_text(f"name: {name}\n{config_yaml}")
    return env_dir


@pytest.fixture
def data_root(tmp_path):
    make_env(tmp_path, "work")
    make_env(tmp_path, "home")
    return tmp_path
