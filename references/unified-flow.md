# Kerno MCP — unified flow (canonical checklist)

The MCP surface is the unified tool set documented here. Use this sequence when the user does not specify otherwise. Authoritative registration: `KernoMcpRegistration.kt` in aicore; operator details: `agent/apps/agent/docs/mcp.md`.

**Default `target_environment`:** **`local`**. Start the stack with the repository's own tooling when `docker-compose`, dev scripts, or a documented quickstart exists. Fall back to **`orchestrate`** only when the repo has **no** way to start the full stack and dependencies, **or** when the user explicitly asks Kerno to orchestrate. See [target-environment.md](target-environment.md).

## Primary sequence

1. **`kerno_healthcheck`** — Docker, git, auth (optional `workspace_path`). Intentionally waits **120 seconds** (SSE timeout testing).
2. **`kerno_get_applications`** — Analyze workspace; pick **`app`**; note **`workspace_id`** and per-app config summary (`target_environment`, recommended next action).
   - If you changed code since Kerno last analyzed/snapshotted the workspace (or results look stale), call **`kerno_sync_workspace`** first (optionally inspect snapshot state via **`kerno_list_workspaces`**).
3. **Choose target environment** — default **`local`**. See [target-environment.md](target-environment.md). **Local (default):** if the repo has `docker-compose`, dev scripts, or a quickstart — start the full stack with that flow, then **`kerno_save_config`** (`local` + `sut_url` + dependencies). **Orchestrate (fallback):** only when none of the above exists **or** the user asked Kerno to orchestrate — **`kerno_save_config`** with `orchestrate` (omit `sut_url`).
4. **`kerno_environment_setup`** — Sync SUT probe (local/remote) or compose-plan + async start-environment job (orchestrate). Optional **`regenerate_instructions`** to steer docker orchestration after failure.
5. **`kerno_environment_status`** — Poll until **`ready_for_endpoint_test: true`**. Do not treat compose **`status: Up`** alone as sufficient.
6. **`kerno_list_endpoints`** — **Requires `scope`** (`all`, `changed`, `file:…`, `endpoint:…`); note **`existingTests`** per route. See [endpoint-test-types.md](endpoint-test-types.md) to choose generate vs validate.
7. **`kerno_endpoint_test`** — Async job for one endpoint (`type`: `generate` | `validate`). Requires **`ready_for_endpoint_test`**. Returns **`job_id`**, **`log_path`**, **`kind`**: `endpoint_test`.
8. **`kerno_job`** — Sparse poll until terminal (`wait=false` every few minutes) or read **`log_path`**. Use **`kerno_cancel`** if the user stops the job.

## Parallel observability (not sequential steps)

During long orchestrate or endpoint-test work:

- **Job registry:** **`kerno_job`** with **`wait=false`** every few minutes, or tail `<workspace>/.kerno/mcp-jobs/<job_id>.log`.
- **Read plane:** **`kerno_get_state`** on resource IDs (composeplan during orchestrate; endpoint-test during GOAP), **`kerno_list_state`**, **`kerno_poll_events`** for event replay.
- **Feedback:** **`kerno_feedback_pending`** / **`kerno_feedback_answer`** (app-scoped) or **`kerno_get_state`** on `.../feedback` + **`answer_feedback_request`**. See [state-and-jobs.md](state-and-jobs.md).

## Workspace snapshot tools

- **`kerno_list_workspaces`** — Inspect snapshot state when results look stale.
- **`kerno_sync_workspace`** — Re-analyze after code changes.
- **`kerno_clear_cache`** — Clear cached analysis when explicitly needed.

## Anti-patterns

- Use **`orchestrate`** when the repo already has `docker-compose.yml`, dev scripts, or a quickstart — **`local`** is the default; start the stack with the repo's tooling first.
- Pick **`orchestrate`** only because the SUT is not running yet — on the local path, start it with the repo's dev flow, then **`kerno_save_config`**.
- Hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase API changes; run **`kerno_endpoint_test`** with **`type=validate`** first, then **`type=generate`** if scenarios are stale.
- Call **`kerno_endpoint_test`** before **`ready_for_endpoint_test`** is true.
- Omit **`scope`** on **`kerno_list_endpoints`** (required).
- Spam **`kerno_job`** in a tight loop (high token use).
- Continue when **`needs_user_feedback`** on a start_environment job — relay **`result.question`** and stop.
- Assume a gated endpoint-test job is stuck on **`kerno_job`** alone; check feedback via read plane or **`kerno_feedback_pending`**.

## See also

- [target-environment.md](target-environment.md) — local / remote / orchestrate decision tree
- [endpoint-test-types.md](endpoint-test-types.md) — generate vs validate
- [state-and-jobs.md](state-and-jobs.md) — job registry, read plane, feedback
- [workspace-config.md](workspace-config.md) — `.kerno/config.yaml` and save_config params
- [mcp-client-config.md](mcp-client-config.md) — connection, timeouts
