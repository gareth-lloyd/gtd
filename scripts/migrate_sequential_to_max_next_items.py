"""One-off migration: Project.sequential (bool) → Project.max_next_items (int|None).

Walks every project YAML under data/<env>/projects/ and rewrites the
frontmatter:
  - sequential: true  → max_next_items: 1
  - sequential: false → (drop both keys — default None = no cap)

After running, commit via `uv run manage.py snapshot`.

Usage:
    uv run python scripts/migrate_sequential_to_max_next_items.py
"""

from pathlib import Path

import frontmatter


def migrate_file(path: Path) -> bool:
    """Return True if the file was modified."""
    post = frontmatter.load(str(path))
    md = post.metadata
    if "sequential" not in md:
        return False
    sequential = bool(md.pop("sequential"))
    if sequential:
        md["max_next_items"] = 1
    with path.open("wb") as f:
        frontmatter.dump(post, f)
    return True


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    data_root = repo_root / "data"
    changed = 0
    checked = 0
    for project_file in sorted(data_root.glob("*/projects/*.md")):
        checked += 1
        if migrate_file(project_file):
            print(f"migrated: {project_file.relative_to(repo_root)}")
            changed += 1
    print(f"\n{changed} of {checked} project files migrated.")


if __name__ == "__main__":
    main()
