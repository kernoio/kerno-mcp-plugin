# Kerno MCP — unified flow (canonical checklist)

The MCP surface is the unified tool set documented here. Use this sequence when the user does not specify otherwise.

**Default `target_environment`:** **`local`** — start the stack with the repository's own tooling (`docker-compose`, dev scripts, quickstart), then point Kerno at it. Use **`remote`** when the env runs somewhere other than this machine (e.g. cloud). Wire DB access where possible so DB-backed scenarios can run; HTTP-only is the fallback. See [target-environment.md](target-environment.md).

## Primary sequence

1. **`kerno_healthcheck`** — Docker, git, auth (optional `workspace_path`). Intentionally waits **120 seconds** (SSE timeout testing).
2. **`kerno_get_applications`** — Analyze workspace; pick **`app`**; note **`workspace_id`** and per-app config summary (`target_environment`, recommended next action).
   - If you changed code since Kerno last analyzed/snapshotted the workspace (or results look stale), call **`kerno_sync_workspace`** first (optionally inspect snapshot state via **`kerno_list_workspaces`**).
3. **Choose environment** — default **`local`**. See [target-environment.md](target-environment.md). Start the stack with the repo's dev flow (`docker-compose`, dev scripts, quickstart), then **`kerno_save_config`** (`local` + `sut_url` + dependencies). Use **`remote`** when the env runs somewhere other than this machine (e.g. cloud). Wire DB env blocks where possible so DB-backed scenarios run; HTTP-only is the fallback.
4. **`kerno_environment_setup`** — Sync SUT probe. Fix config if `missing_config`.
5. **`kerno_environment_status`** — Poll until **`ready_for_endpoint_test: true`**. Do not treat compose **`status: Up`** alone as sufficient.
6. **`kerno_list_endpoints`** — **Requires `scope`** (`all`, `changed`, `file:…`, `endpoint:…`); note **`existingTests`** per route. See [endpoint-test-types.md](endpoint-test-types.md) to choose generate, validate, or update.
7. **`kerno_endpoint_test`** — Async job for one endpoint (`type`: `generate` | `validate` | `update`). Requires **`ready_for_endpoint_test`**. Optional `effort`, `box_testing_strategy`, `tags`, `test_generation_context`, `scenario_ids`, `interactive` — see [endpoint-test-types.md](endpoint-test-types.md); resolve testing intent from the user's own rules files before the first call. Returns **`job_id`**, **`log_path`**, **`kind`**: `endpoint_test`, and **`resolved_intent`**.
8. **`kerno_job`** — Sparse poll until terminal (`wait=false` every few minutes) or read **`log_path`**. Use **`kerno_cancel`** if the user stops the job.

## Parallel observability (not sequential steps)

During long endpoint-test work:

- **Job registry:** **`kerno_job`** with **`wait=false`** every few minutes, or tail `<workspace>/.kerno/mcp-jobs/<job_id>.log`.
- **Read plane:** **`kerno_get_state`** on resource IDs (endpoint-test during GOAP), **`kerno_list_state`**, **`kerno_poll_events`** for event replay.
- **Feedback:** **`kerno_feedback_pending`** / **`kerno_feedback_answer`** (app-scoped) or **`kerno_get_state`** on `.../feedback` + **`answer_feedback_request`**. See [state-and-jobs.md](state-and-jobs.md).

## Workspace snapshot tools

- **`kerno_list_workspaces`** — Inspect snapshot state when results look stale.
- **`kerno_sync_workspace`** — Re-analyze after code changes.
- **`kerno_clear_cache`** — Clear cached analysis when explicitly needed.

## Anti-patterns

- Hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase API changes; run **`kerno_endpoint_test`** with **`type=validate`** first, then **`type=update`** when the endpoint changed intentionally (**`type=generate`** only to restart coverage).
- Pass **`tags: ["security"]`** alone when the user wanted security *in addition to* functional coverage — it narrows the run. Pass both tags.
- Silently accept `effort` / `box_testing_strategy` / `tags` defaults on a first run without checking the user's own rules files or asking.
- Call **`kerno_endpoint_test`** before **`ready_for_endpoint_test`** is true.
- Omit **`scope`** on **`kerno_list_endpoints`** (required).
- Spam **`kerno_job`** in a tight loop (high token use).
- Assume a gated endpoint-test job is stuck on **`kerno_job`** alone; check feedback via read plane or **`kerno_feedback_pending`**.
- Fall back to **black box** (HTTP-only) without telling the user that scenarios requiring direct DB access will be reported **`[BLOCKED]`**.

## See also

- [target-environment.md](target-environment.md) — local / remote and DB-access decisions
- [endpoint-test-types.md](endpoint-test-types.md) — generate / validate / update, effort, box strategy, tags, verdicts
- [state-and-jobs.md](state-and-jobs.md) — job registry, read plane, feedback
- [workspace-config.md](workspace-config.md) — `.kerno/config.yaml` and save_config params
- [mcp-client-config.md](mcp-client-config.md) — connection, timeouts
