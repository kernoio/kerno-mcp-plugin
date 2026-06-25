#!/usr/bin/env python3
"""Verify kerno-mcp-plugin docs match the unified MCP tool surface."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = ("skills", "rules", "commands", "references")
SCAN_FILES = ("README.md", "CLAUDE.md")

FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("kerno_compose_", re.compile(r"kerno_compose_")),
    ("kerno_start_environment", re.compile(r"kerno_start_environment")),
    ("kerno_plan_baseline", re.compile(r"kerno_plan_baseline")),
    ("kerno_implement_baseline", re.compile(r"kerno_implement_baseline")),
    ("kerno_validate", re.compile(r"kerno_validate")),
    ("kerno_approve", re.compile(r"kerno_approve")),
    ("kerno_reject", re.compile(r"kerno_reject")),
    ("kerno_environments_status", re.compile(r"kerno_environments_status")),
    ("kerno_capture_baseline", re.compile(r"kerno_capture_baseline")),
    ("ready_for_validation", re.compile(r"ready_for_validation")),
    ("MCP_TOOL_SURFACE=legacy", re.compile(r"MCP_TOOL_SURFACE=legacy")),
    ("compose_plan_generate", re.compile(r"compose_plan_generate")),
    ("compose_plan_feedback", re.compile(r"compose_plan_feedback")),
    ("plan-implement-baseline", re.compile(r"plan-implement-baseline")),
    ("kerno-capture-baseline", re.compile(r"kerno-capture-baseline")),
)

UNIFIED_MCP_TOOL_NAMES: tuple[str, ...] = (
    "kerno_healthcheck",
    "kerno_get_applications",
    "kerno_list_endpoints",
    "kerno_save_config",
    "kerno_environment_setup",
    "kerno_environment_status",
    "kerno_endpoint_test",
    "kerno_job",
    "kerno_cancel",
    "kerno_get_state",
    "kerno_list_state",
    "kerno_poll_events",
    "answer_feedback_request",
    "kerno_feedback_pending",
    "kerno_feedback_answer",
    "kerno_list_workspaces",
    "kerno_sync_workspace",
    "kerno_clear_cache",
)


def iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for name in SCAN_FILES:
        path = ROOT / name
        if path.is_file():
            files.append(path)
    for dirname in SCAN_DIRS:
        base = ROOT / dirname
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in {".md", ".mdc"}:
                files.append(path)
    return files


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check_forbidden(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{relative(path)}:{line}: forbidden token {label!r}")
    return errors


def check_required_coverage(files: list[Path]) -> list[str]:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    missing = [name for name in UNIFIED_MCP_TOOL_NAMES if name not in combined]
    if not missing:
        return []
    return [f"missing unified tool documentation: {', '.join(missing)}"]


def main() -> int:
    files = iter_scan_files()
    if not files:
        sys.stderr.write("No files to scan\n")
        return 1

    errors = check_forbidden(files) + check_required_coverage(files)
    if errors:
        sys.stderr.write("check-unified-drift: FAILED\n")
        for error in errors:
            sys.stderr.write(f"  - {error}\n")
        return 1

    sys.stdout.write(
        f"check-unified-drift: OK ({len(files)} files, {len(UNIFIED_MCP_TOOL_NAMES)} tools)\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
