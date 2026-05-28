---
description: Show Kerno MCP setup pointers, job semantics, and reference links
---

Summarize for the user:

0. **First-time setup** — run `/install-kerno` or `${CLAUDE_PLUGIN_ROOT}/skills/install-kerno/SKILL.md`; host registration details in `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (**Install (CLI)**). Docs: https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp
1. **MCP connection** — `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (URL, env vars, timeouts).
2. **Tool ordering** — `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`.
3. **Compose plan** — `${CLAUDE_PLUGIN_ROOT}/references/compose-plan.md` before first **`kerno_start_environment`**.
4. **Async jobs** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-background-job/SKILL.md` for launch tools + **`kerno_job`** + **`kerno_cancel`**.
5. **Scenario validation** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-validate/SKILL.md` for **`kerno_validate`** (after code changes, before hand-editing `.kerno/scenarios/`).
6. **Scenario plan + implement** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-plan-implement-baseline/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/references/plan-implement-baseline.md` for **`kerno_plan_baseline`** and **`kerno_implement_baseline`**.
7. **Further detail** — the MCP server’s own `tools/list` output for live tool schemas.
