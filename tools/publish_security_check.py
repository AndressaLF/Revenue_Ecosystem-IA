#!/usr/bin/env python3
"""CLI — audit staged/tracked files before push to public GitHub."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python tools/publish_security_check.py` without installing the package.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.publish_security import audit_public_push, format_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bloqueia push se houver secrets ou PII em arquivos Git."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Raiz do repositório (default: cwd)",
    )
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="Auditar só arquivos no index (git add)",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Sempre exit 0 (só imprime relatório; usado no pre-push não-estrito)",
    )
    args = parser.parse_args()

    findings = audit_public_push(
        args.repo.resolve(),
        scan_tracked=not args.staged_only,
        scan_staged=True,
    )
    errors = [f for f in findings if f.severity == "error"]
    print(format_report(findings))
    if args.warn_only:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
