---
name: kerno-mcp-bootstrap
description: This skill should be used when the user asks to bootstrap Kerno MCP, run the full environment setup flow, or runs /kerno-bootstrap. Guides healthcheck, get_applications, optional endpoints, start_environment, and kerno_job until terminal state with client-aware polling.
version: 0.1.0
---

# Kerno MCP bootstrap

Execute the recommended MCP workflow for aicore-agent. Use the MCP tools exposed by the connected server (names may be prefixed by the client; match tool definitions to `kerno_*`).

**References:**

- `${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md` — ordered steps and anti-patterns
- `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` — URL and timeouts

## Preconditions

1. Confirm the agent is running with MCP enabled and the client can list tools.
2. Obtain **workspace_path**: absolute path to the workspace root. It must match the agent’s configured `WORKSPACE` (expected root).
3. Obtain **app**: module id or name from the next step (`kerno_get_applications`).

## Step 1: kerno_healthcheck

Call `kerno_healthcheck` with `workspace_path` if required, or omit if the tool defaults to the agent workspace.

If the result indicates failure, stop and report remediation (Docker, git, auth).

## Step 2: kerno_get_applications

Call `kerno_get_applications` with the same `workspace_path`. Parse supported applications and choose **app** for subsequent steps.

## Step 3 (optional): kerno_list_endpoints

If the task needs HTTP route discovery, call `kerno_list_endpoints` with `workspace_path` and optional `app` to scope.

## Step 4: kerno_start_environment

Call `kerno_start_environment` with `workspace_path` and `app`. Record **job_id** and **log_path** from the response.

Expect **long** wall-clock time (often **many minutes**, sometimes **past 15 minutes**).

## Step 5: kerno_job

Call `kerno_job` with **job_id** and **workspace_path**.

MCP hosts typically cap **one tool call** around **~60s**; that limit is on the **client**, not something you can raise via the server. Use **`wait=false`** and check again **every few minutes**, or read **log_path** for progress. **Do not** spam **`kerno_job`** in a tight loop (token cost).

If the job is still running after a check, wait wall-clock time before calling again, or follow **log_path**.

Do not call `kerno_compose_up` or `kerno_compose_down` for this app until the job finishes successfully or fails.

## Step 6: After healthy

Use `kerno_compose_status`, `kerno_list_endpoints`, `kerno_environments_status`, or `kerno_compose_logs` as needed. Do not treat `kerno_environments_status` “Not Started” during an in-flight start as a reason to call `kerno_compose_up` manually.
