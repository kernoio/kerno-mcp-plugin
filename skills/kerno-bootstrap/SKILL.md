---
name: kerno-bootstrap
description: This skill should be used when the user asks to bootstrap Kerno MCP, verify connectivity, or runs /kerno-bootstrap. Guides healthcheck, get_applications, and optional endpoint discovery. For environment bring-up use kerno-environment-setup.
version: 0.2.0
---

# Kerno MCP bootstrap

Bootstrap Kerno MCP connectivity for aicore-agent. Use the MCP tools exposed by the connected server (names may be prefixed by the client; match tool definitions to `kerno_*`).

**References:**

- `${CLAUDE_PLUGIN_ROOT}/references/unified-flow.md` — canonical tool order
- `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` — URL and timeouts
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md` — save_config → environment_setup → environment_status

## Preconditions

1. Confirm the agent is running with MCP enabled and the client can list tools.
2. Obtain **workspace_path**: absolute path to the workspace root. It must match the agent’s configured `WORKSPACE` (expected root).

## Step 1: kerno_healthcheck

Call `kerno_healthcheck` with `workspace_path` if required, or omit if the tool defaults to the agent workspace.

The tool intentionally waits **120 seconds** (SSE timeout testing). If the result indicates failure, stop and report remediation (Docker, git, auth).

## Step 2: kerno_get_applications

Call `kerno_get_applications` with the same `workspace_path`. Parse supported applications and choose **app** for subsequent steps. Note **workspace_id** and per-app config summary (`target_environment`, recommended next action).

## Step 3 (optional): kerno_list_endpoints

If the task needs HTTP route discovery before environment setup, call `kerno_list_endpoints` with `workspace_path`, **required `scope`** (e.g. `all`), and optional `app`.

For the full workflow, **`kerno_list_endpoints`** normally runs **after** **`ready_for_endpoint_test`** — see unified flow.

## Next steps after bootstrap

1. **Environment** — load `${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md`. Prefer **`local`**: start the repo's dev flow first if compose/scripts exist; use **`orchestrate`** only on explicit user request or when no easy startup exists.
2. **`kerno_save_config`** → **`kerno_environment_setup`** → **`kerno_environment_status`**
3. **`kerno_endpoint_test`** — see `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md`

## See also

- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md` — environment setup
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md` — endpoint tests
