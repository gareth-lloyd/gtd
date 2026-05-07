"""Append-only log of irreversible actions (purge, project delete).

Records land at `<root>/.audit/purges.ndjson`, one JSON object per line.
The directory is intentionally tracked by git so a snapshot picks it up
and the record survives a synced device wipe.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

PurgeKind = Literal["item", "project"]


def log_purge(root: Path, *, env: str, kind: PurgeKind, target_id: str) -> None:
    path = root / ".audit" / "purges.ndjson"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "env": env,
        "kind": kind,
        "id": target_id,
    }
    with path.open("a") as f:
        f.write(json.dumps(record) + "\n")
