"""Initialize SQLite schema."""

from __future__ import annotations

import argparse
from pathlib import Path

from shared_components.database.schema import init_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize RE-IA SQLite database")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("storage/local_cache.db"),
        help="Database file path",
    )
    args = parser.parse_args()
    path = init_db(args.db)
    print(f"Database ready: {path}")


if __name__ == "__main__":
    main()
