---
name: kerno-mcp-bootstrap
description: This skill should be used when the user asks to bootstrap Kerno MCP, verify connectivity, or runs /kerno-bootstrap. Guides healthcheck, get_applications, and optional endpoint discovery. For environment bring-up use kerno-mcp-environment-setup.
version: 0.1.0
---

# Kerno MCP bootstrap

Bootstrap Kerno MCP connectivity for aicore-agent. Use the MCP tools exposed by the connected server (names may be prefixed by the client; match tool definitions to `kerno_*`).

**References:**

- `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md` — ordered steps and anti-patterns
- `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` — URL and timeouts
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-environment-setup/SKILL.md` — compose plan approval gate + start environment

## Preconditions

1. Confirm the agent is running with MCP enabled and the client can list tools.
2. Obtain **workspace_path**: absolute path to the workspace root. It must match the agent’s configured `WORKSPACE` (expected root).

## Step 1: kerno_healthcheck

Call `kerno_healthcheck` with `workspace_path` if required, or omit if the tool defaults to the agent workspace.

The tool intentionally waits **120 seconds** (SSE timeout testing). If the result indicates failure, stop and report remediation (Docker, git, auth).

## Step 2: kerno_get_applications

Call `kerno_get_applications` with the same `workspace_path`. Parse supported applications and choose **app** for subsequent steps. Note **workspace_id** if you will pass it to later tools.

## Step 3 (optional): kerno_list_endpoints

If the task needs HTTP route discovery, call `kerno_list_endpoints` with `workspace_path`, **required `scope`** (e.g. `all`), and optional `app`.

## See also

- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-environment-setup/SKILL.md` — compose plan + approval gate + start environment
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-plan-implement-baseline/SKILL.md` — scenario authoring after env is ready
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-validate/SKILL.md` — run tests after code changes
