# Changes detected marker (`.kerno/CHANGES_DETECTED.md`)

Kerno MCP supports **`scope: "changed"`**, which maps the current git working tree diff vs `HEAD` (staged + unstaged)
to impacted HTTP endpoints.

This repo also includes an **optional, local marker file** convention that a hook can read at the end of a turn to
decide whether it should run **`kerno_validate`**.

## What creates the file

When the agent calls MCP tools with `scope: "changed"` (notably **`kerno_list_endpoints`** and **`kerno_validate`**),
the aicore-agent writes:

- `.kerno/CHANGES_DETECTED.md`

at the **workspace root** (`WORKSPACE/.kerno/CHANGES_DETECTED.md`).

## What creates the hook script

When the aicore-agent starts for a workspace (first snapshot creation), it ensures this file exists:

- `.kerno/hooks/check-changes-detected.sh`

If the file already exists, it is left unchanged.

## File format

The file is markdown with two key sections:

- **Impacted endpoints**: `- app=<moduleId> METHOD /path`
- **Touched files**: repo-relative paths from git diff vs `HEAD`

Empty/missing file means “no action”.

## Hook pattern (recommended)

Wire a hook to run at the end of an agent turn:

1. If the file is missing or empty: do nothing.
2. If the file has content: print it and instruct the LLM to:
   - run **`kerno_validate`** with `scope: "changed"`
   - wait for completion using **`kerno_job`**
   - clear the file afterward

### Repo-local bash script

Put this in your repo at `.kerno/hooks/check-changes-detected.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="${KERNO_WORKSPACE_ROOT:-$(pwd)}"
FILE="$ROOT/.kerno/CHANGES_DETECTED.md"

if [[ ! -f "$FILE" ]]; then exit 0; fi
if [[ ! -s "$FILE" ]]; then exit 0; fi

echo "=== .kerno/CHANGES_DETECTED.md ==="
cat "$FILE"
echo
echo "Run: kerno_validate(scope=\"changed\"), then kerno_job until terminal, then clear the file."
```

### Claude Code example

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.kerno/hooks/check-changes-detected.sh"
          }
        ]
      }
    ]
  }
}
```

### Cursor example

Create `.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "stop": [
      { "command": "bash .kerno/hooks/check-changes-detected.sh" }
    ]
  }
}
```

