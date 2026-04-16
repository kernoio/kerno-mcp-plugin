---
description: Author or refresh TypeScript HTTP scenario tests via kerno_capture_baseline (async job + scopes)
argument-hint: "[workspace_path] [app] [scope]"
---

Run the **kerno-mcp-capture-baseline** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-capture-baseline/SKILL.md`.

Parse `$ARGUMENTS` if present: optional **`workspace_path`**, **`app`**, and **`scope`**. If missing, derive from context or ask once. Default scope is often `all` only after the user confirms environment is up and which module(s) to target.

For scope details and parameters, use `${CLAUDE_PLUGIN_ROOT}/references/capture-baseline.md`.
