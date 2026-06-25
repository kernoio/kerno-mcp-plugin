---
description: Set up the environment (save_config, environment_setup, environment_status)
argument-hint: "[workspace_path] [app] [local|remote|orchestrate]"
---

Run the **kerno-environment-setup** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md`.

Parse `$ARGUMENTS` if present: optional `workspace_path`, `app`, and target environment hint. If missing, derive from context or ask once.
