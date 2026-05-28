---
name: kerno-mcp-bootstrap
description: This skill should be used when the user asks to bootstrap Kerno MCP, run the full environment setup flow, or runs /kerno-bootstrap. Guides healthcheck, get_applications, optional endpoints, compose plan gate, compose_up or start_environment, and kerno_job until terminal with client-aware polling.
version: 0.1.0
---

# Kerno MCP bootstrap

Execute the recommended MCP workflow for aicore-agent. Use the MCP tools exposed by the connected server (names may be prefixed by the client; match tool definitions to `kerno_*`).

**References:**

- `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md` — ordered steps and anti-patterns
- `${CLAUDE_PLUGIN_ROOT}/references/compose-plan.md` — compose plan before first start_environment
- `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` — URL and timeouts

## Preconditions

1. Confirm the agent is running with MCP enabled and the client can list tools.
2. Obtain **workspace_path**: absolute path to the workspace root. It must match the agent’s configured `WORKSPACE` (expected root).
3. Obtain **app**: module id or name from the next step (`kerno_get_applications`).

## Step 1: kerno_healthcheck

Call `kerno_healthcheck` with `workspace_path` if required, or omit if the tool defaults to the agent workspace.

The tool intentionally waits **120 seconds** (SSE timeout testing). If the result indicates failure, stop and report remediation (Docker, git, auth).

## Step 2: kerno_get_applications

Call `kerno_get_applications` with the same `workspace_path`. Parse supported applications and choose **app** for subsequent steps. Note **workspace_id** if you will pass it to later tools.

## Step 3 (optional): kerno_list_endpoints

If the task needs HTTP route discovery, call `kerno_list_endpoints` with `workspace_path`, **required `scope`** (e.g. `all`), and optional `app`.

## Step 4: Bring the stack up

**Prefer `kerno_compose_up`** when Kerno-generated compose files already exist (synchronous, cheap).

**First-time setup** for an app — follow `${CLAUDE_PLUGIN_ROOT}/references/compose-plan.md`:

1. `kerno_compose_plan` → if `no_plan_yet`, `kerno_compose_plan_generate` → `kerno_job`
2. Show plan markdown to the user; loop `kerno_compose_plan_feedback` if they want changes
3. Only after **explicit user approval**, `kerno_start_environment` (optional `regenerate=true`)
4. `kerno_job` until terminal (`healthy`, `needs_user_feedback`, `failed`, or `cancelled`)

On **`needs_user_feedback`**, stop and ask the user — call `kerno_compose_plan_feedback` with their answer before retrying start.

Expect **long** wall-clock time for async steps (often **many minutes**, sometimes **past 15 minutes**).

## Step 5: kerno_job (async launches only)

When step 4 used `kerno_start_environment` or compose plan async tools, call `kerno_job` with **job_id** and **workspace_path**.

MCP hosts typically cap **one tool call** around **~60s**. Use **`wait=false`** and check again **every few minutes**, or read **log_path**. **Do not** spam **`kerno_job`** in a tight loop.

Do not call `kerno_compose_up` or `kerno_compose_down` for this app until any in-flight `kerno_start_environment` job finishes.

## Step 6: Confirm readiness

Call `kerno_compose_status` and verify **`ready_for_validation`** is true before validate or implement. **Do not** treat `status: Up` alone as sufficient.

Use `kerno_environments_status`, `kerno_list_endpoints`, or `kerno_compose_logs` as needed. Do not treat `kerno_environments_status` “Not Started” during an in-flight start as a reason to call `kerno_compose_up` manually.

## See also

- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-plan-implement-baseline/SKILL.md` — scenario authoring after env is ready
- `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-validate/SKILL.md` — run tests after code changes
