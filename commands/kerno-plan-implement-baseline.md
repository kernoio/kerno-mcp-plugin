---
description: Author or refresh Kerno HTTP scenario tests via kerno_plan_baseline and kerno_implement_baseline (async jobs + scopes)
argument-hint: "[workspace_path] [app] [scope]"
---

Run the **kerno-plan-implement-baseline** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-plan-implement-baseline/SKILL.md`.

Parse `$ARGUMENTS` if present: optional **`workspace_path`**, **`app`**, and **`scope`**. If missing, derive from context or ask once. Default scope is often `all` only after the user confirms which module(s) to target.

For scope details and parameters, use `${CLAUDE_PLUGIN_ROOT}/references/plan-implement-baseline.md`.
