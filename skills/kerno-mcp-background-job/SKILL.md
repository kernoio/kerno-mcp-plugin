---
name: kerno-mcp-background-job
description: This skill should be used when the user asks about Kerno async jobs, kerno_job wait semantics, or debugging long-running start_environment. Explains launch plus kerno_job, client-side per-tool-call limits, and sparse polling to avoid token spam.
version: 0.1.0
---

# Kerno MCP background jobs

Long-running work uses a **launch** tool (e.g. `kerno_start_environment`, `kerno_capture_baseline`, `kerno_validate`) plus **`kerno_job`**. Streamable HTTP clients should not rely on MCP progress notifications alone.

## Launch

`kerno_start_environment` (and similarly `kerno_capture_baseline`, `kerno_validate`) returns immediately with:

- **job_id**
- **log_path** (file under `<workspace>/.kerno/mcp-jobs/<job_id>.log`)
- **status** `running`, **kind** (e.g. `start_environment`)

Wall-clock time is often **many minutes** and can **exceed 15 minutes**. There is no reliable upper bound from the tool response alone.

## Complete with kerno_job

Call **`kerno_job`** with `job_id`, `workspace_path`, and:

- **wait** (default **true**): the server blocks until the job is `healthy` or `failed`, or until the **server wait budget** elapses while still running.

**Effective limit:** MCP **hosts** (Claude Code, Cursor, etc.) usually enforce a **per-tool-call** duration on the order of **~60 seconds** on the HTTP request, **independent** of server behavior. The agent does not expose a parameter to extend that client-side cap. **`wait=true` does not mean** the model can hold one call open until a 15+ minute job finishes—the client may cut the call first.

**Recommended pattern:**

- Prefer **`wait=false`** and call again **every few minutes** (not every 30 seconds), **or** tail/read **`log_path`** for progress.
- **Do not** call **`kerno_job`** in a **tight loop**; each call consumes model context and tokens.

If the response has **wait_timed_out** true and status **running**:

- Call **`kerno_job`** again **after several minutes** with **`wait=false`** (or **`wait=true`** knowing the same client limits apply), **or**
- Read **`log_path`** for live output.

## Anti-patterns

- Calling **`kerno_compose_up`** while **`kerno_start_environment`** is still running for the same app.
- Assuming **`kerno_environments_status`** “Not Started” during an in-flight start means you should call **`kerno_compose_up`** manually.
- **Rapid repeated `kerno_job`** calls to “watch” progress (high token use).

## Proxies and clients

The MCP **host** timeout is usually the binding constraint for a single tool invocation. Server-side SDK timeouts do not override the host’s per-tool-call limit.

See `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md`.
