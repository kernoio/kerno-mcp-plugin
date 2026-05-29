---
name: kerno-background-job
description: This skill should be used when the user asks about Kerno async jobs, kerno_job wait semantics, kerno_cancel, or debugging long-running MCP work. Explains launch plus kerno_job, client-side per-tool-call limits, and sparse polling to avoid token spam.
version: 0.1.0
---

# Kerno MCP background jobs

Long-running work uses a **launch** tool plus **`kerno_job`**. Streamable HTTP clients should not rely on MCP progress notifications alone.

## Launch tools

| Tool | `kind` |
| --- | --- |
| **`kerno_start_environment`** | `start_environment` |
| **`kerno_compose_plan_generate`** | `compose_plan_generate` |
| **`kerno_compose_plan_feedback`** | `compose_plan_feedback` |
| **`kerno_plan_baseline`** (async) | `plan_baseline` |
| **`kerno_implement_baseline`** | `implement_baseline` |
| **`kerno_validate`** | `validate` |

Each returns immediately with **job_id**, **log_path** (under `<workspace>/.kerno/mcp-jobs/<job_id>.log`), **status** `running`, and **kind**.

**`kerno_plan_baseline`** sync mode (**`method`** + **`path`**, no **`scope`**) returns **`plan_sync`** with **`job`** null — no **`kerno_job`** for that call.

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
- Other kinds: typically `healthy` or `failed` in terminal JSON (plus kind-specific payloads: **`plan_baseline`**, **`implement_baseline`**, **`validate`**, **`compose_plan`**).

If the response has **wait_timed_out** true and status **running**, call **`kerno_job`** again after several minutes with **`wait=false`**, or read **`log_path`**.

After the **first terminal** response, the job is **retired** — do not call **`kerno_job`** again with the same **`job_id`**.

## Cancel with kerno_cancel

**`kerno_cancel(job_id, workspace_path)`** is fire-and-forget. The next **`kerno_job`** for that id returns **`status: cancelled`** once, then retires the id. Use when the user asks to stop a job or the result is no longer needed.

## Anti-patterns

- Calling **`kerno_compose_up`** while **`kerno_start_environment`** is still running for the same app.
- Assuming **`kerno_environments_status`** “Not Started” during an in-flight start means you should call **`kerno_compose_up`** manually.
- **Rapid repeated `kerno_job`** calls to “watch” progress (high token use).
- Treating **`healthy`** or **`status: Up`** as ready for validate/implement without **`ready_for_validation`**.

See `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md`.
