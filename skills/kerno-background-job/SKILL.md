---
name: kerno-background-job
description: This skill should be used when the user asks about Kerno async jobs, kerno_job wait semantics, kerno_cancel, or debugging long-running MCP work on the unified surface. Explains launch plus kerno_job, client-side per-tool-call limits, and sparse polling.
version: 0.3.0
---

# Kerno MCP background jobs (unified surface)

Long-running work uses a **launch** tool plus **`kerno_job`**. Jobs often run **many minutes** and can **exceed 15 minutes**.

**References (read before acting):**

- `references/state-and-jobs.md` — launch tools, terminal statuses, feedback gates, read plane
- `references/mcp-client-config.md` — host per-tool-call limits (~60s) and timeout pattern
- `references/unified-flow.md` — anti-patterns

## Recommended pattern

1. Launch with **`kerno_environment_setup`** (orchestrate only) or **`kerno_endpoint_test`** — note **`job_id`** and **`log_path`**.
2. Poll **`kerno_job`** with **`wait=false`** every few minutes, **or** read **`log_path`**. Do not tight-loop.
3. On first terminal response, the **`job_id`** is retired — do not poll again.
4. Stop with **`kerno_cancel(job_id, workspace_path)`** when the user asks to abort.

If **`wait_timed_out`** is true and status is still **`running`**, wait several minutes and poll again with **`wait=false`**.

**Hard stops:** **`needs_user_feedback`** on start_environment — relay **`result.question`**. Endpoint-test plan gates — see **`state-and-jobs.md`**, not **`kerno_job`** alone.
