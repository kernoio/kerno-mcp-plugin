---
description: Show Kerno MCP setup pointers, unified flow, and reference links
---

Summarize for the user:

0. **First-time setup** — run `/install-kerno` or `${CLAUDE_PLUGIN_ROOT}/skills/install-kerno/SKILL.md`; host registration details in `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (**Install (CLI)**). Docs: https://kerno.gitbook.io/docs/getting-started/quickstart
1. **MCP connection** — `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` (URL, env vars, timeouts).
2. **Unified flow** — `${CLAUDE_PLUGIN_ROOT}/references/unified-flow.md` (canonical checklist).
3. **Target environment** — `${CLAUDE_PLUGIN_ROOT}/references/target-environment.md` (local / remote / orchestrate).
4. **Workspace config** — `${CLAUDE_PLUGIN_ROOT}/references/workspace-config.md` (save_config, `.kerno/config.yaml`).
5. **Environment setup** — `/kerno-env` or `${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md`.
6. **Endpoint tests** — `/kerno-endpoint-test` or `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md`; types in `${CLAUDE_PLUGIN_ROOT}/references/endpoint-test-types.md`.
7. **Async jobs & feedback** — `${CLAUDE_PLUGIN_ROOT}/skills/kerno-background-job/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/references/state-and-jobs.md`.
8. **Sync after code changes** — **`kerno_sync_workspace`** (and optionally **`kerno_list_workspaces`**); optional hook pattern in `${CLAUDE_PLUGIN_ROOT}/references/changes-detected.md`.
9. **Further detail** — the MCP server’s `tools/list` output for live tool schemas.
