---
name: kerno-background-job
description: This skill should be used when the user asks about Kerno async jobs, kerno_job wait semantics, kerno_cancel, or debugging long-running MCP work on the unified surface. Explains launch plus kerno_job, client-side per-tool-call limits, and sparse polling.
version: 0.2.0
---

# Kerno MCP background jobs (unified surface)

Long-running work uses a **launch** tool plus **`kerno_job`**. Streamable HTTP clients should not rely on MCP progress notifications alone.

## Launch tools (unified surface)

| Tool | `kind` | Notes |
| --- | --- | --- |
| **`kerno_environment_setup`** | `start_environment` | **Orchestrate path only** — local/remote are sync probe, no job |
| **`kerno_endpoint_test`** | `endpoint_test` | Always async |

Each async launch returns immediately with **job_id**, **log_path** (under `<workspace>/.kerno/mcp-jobs/<job_id>.log`), **status** `running`, and **kind**.

Wall-clock time is often **many minutes** and can **exceed 15 minutes**.

## Complete with kerno_job

Call **`kerno_job`** with `job_id`, `workspace_path`, and:

- **wait** (default **true**): the server blocks until a terminal status or until the **server wait budget** elapses while still running.

**Effective limit:** MCP **hosts** usually enforce a **per-tool-call** duration on the order of **~60 seconds** on the HTTP request, **independent** of server behavior. **`wait=true` does not mean** the model can hold one call open until a 15+ minute job finishes.

**Recommended pattern:**

- Prefer **`wait=false`** and call again **every few minutes** (not every 30 seconds), **or** tail/read **`log_path`**.
- **Do not** call **`kerno_job`** in a **tight loop**.

### Terminal statuses

- **`start_environment`**: `healthy`, `needs_user_feedback`, `failed`, `cancelled`. **`needs_user_feedback` is a hard stop** — relay **`result.question`** to the user.
- **`endpoint_test`**: terminal JSON includes run outcome; job-level status follows registry semantics.

**Feedback gates on endpoint_test:** **`kerno_job`** shows job progress but **not** plan-review or planner-question gates. When a generate job looks stuck while still `running`, use **`kerno_feedback_pending`** or **`kerno_get_state`** on the endpoint-test resource — see `${CLAUDE_PLUGIN_ROOT}/references/state-and-jobs.md`.

If the response has **wait_timed_out** true and status **running**, call **`kerno_job`** again after several minutes with **`wait=false`**, or read **`log_path`**.

After the **first terminal** response, the job is **retired** — do not call **`kerno_job`** again with the same **`job_id`**.

## Cancel with kerno_cancel

**`kerno_cancel(job_id, workspace_path)`** is fire-and-forget. The next **`kerno_job`** for that id returns **`status: cancelled`** once, then retires the id. Use when the user asks to stop a job or the result is no longer needed.

## Anti-patterns

- **Rapid repeated `kerno_job`** calls to “watch” progress (high token use).
- Treating **`healthy`** or **`status: Up`** as ready for endpoint tests without **`ready_for_endpoint_test`**.
- Assuming endpoint-test feedback gates appear on **`kerno_job`** responses.

See `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` and `${CLAUDE_PLUGIN_ROOT}/references/state-and-jobs.md`.
