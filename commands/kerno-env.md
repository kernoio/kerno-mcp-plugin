---
description: Set up the environment (compose plan approval gate, then start_environment; handles needs_user_feedback)
argument-hint: "[workspace_path] [app]"
---

Run the **kerno-mcp-environment-setup** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-environment-setup/SKILL.md`.

Parse `$ARGUMENTS` if present: optional `workspace_path` and `app`. If missing, derive from context or ask once.

