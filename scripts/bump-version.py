#!/usr/bin/env python3
"""Bump the plugin version across all client manifests, in lockstep.

Usage:
    python3 scripts/bump-version.py <new-version>   # e.g. 0.2.0

Keeps .claude-plugin, .cursor-plugin, and .codex-plugin plugin.json in sync so
marketplace installs (Claude/Cursor/Codex) see the same version and can offer an
update. After bumping, commit, then run `claude plugin tag --push` to tag the
release and create a GitHub Release.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".codex-plugin/plugin.json",
]
VERSION_RE = re.compile(r'("version":\s*")([^"]+)(")')


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: bump-version.py <new-version>   e.g. 0.2.0")
    new = sys.argv[1].lstrip("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", new):
        sys.exit(f"not a semver X.Y.Z: {new}")

    changes = []
    for rel in MANIFESTS:
        path = ROOT / rel
        text = path.read_text()
        match = VERSION_RE.search(text)
        if not match:
            sys.exit(f"no top-level \"version\" field in {rel}")
        old = match.group(2)
        path.write_text(VERSION_RE.sub(rf"\g<1>{new}\g<3>", text, count=1))
        changes.append(f"  {rel}: {old} -> {new}")

    print("bumped:")
    print("\n".join(changes))
    print(
        f"\nnext: commit these, then `claude plugin tag --push` "
        f"(tags kerno--v{new}), then draft a GitHub Release for v{new}."
    )


if __name__ == "__main__":
    main()
