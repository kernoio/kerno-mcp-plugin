---
description: Verify Kerno MCP connectivity (healthcheck, get_applications, optional endpoint listing)
argument-hint: "[workspace_path] [app]"
---

Run the **kerno-bootstrap** skill from `skills/kerno-bootstrap/SKILL.md`.

Parse `$ARGUMENTS` if present: optional `workspace_path` and `app` for the user’s target workspace and application module. If missing, derive from context or ask once.
