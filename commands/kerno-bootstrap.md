---
description: Run the recommended Kerno MCP workflow (healthcheck, get_applications, start environment, wait for job)
argument-hint: "[workspace_path] [app]"
---

Run the **kerno-mcp-bootstrap** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-bootstrap/SKILL.md`.

Parse `$ARGUMENTS` if present: optional `workspace_path` and `app` for the user’s target workspace and application module. If missing, derive from context or ask once.
