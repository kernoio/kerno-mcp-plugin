---
description: Show Kerno MCP setup pointers, job semantics, and reference links
---

Summarize for the user:

0. **First-time setup** — run `/install-kerno` or `${CLAUDE_PLUGIN_ROOT}/skills/install-kerno/SKILL.md`; host registration details in `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (**Install (CLI)**). Docs: https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp
1. **MCP connection** — `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (URL, env vars, timeouts).
2. **Tool ordering** — `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`.
3. **Async jobs** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-background-job/SKILL.md` for `kerno_start_environment` + `kerno_job`.
4. **Scenario validation** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-validate/SKILL.md` for `kerno_validate` (after code changes, before hand-editing `.kerno/scenarios/`).
5. **Scenario capture** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-capture-baseline/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/references/capture-baseline.md` for `kerno_capture_baseline` (after environment is healthy).
6. **Further detail** — `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`, `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md`, and the MCP server’s own `tools/list` output for live tool schemas.
