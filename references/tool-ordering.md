# Kerno MCP — recommended tool order

Use this as a **default** sequence when the user does not specify otherwise. Details: `agent/apps/agent/docs/mcp.md` in the aicore repo.

1. **`kerno_healthcheck`** — Docker, git, auth (optional `workspace_path`).
2. **`kerno_get_applications`** — Analyze workspace; note `workspace_id` if you will pass it to later tools.
3. Optionally **`kerno_list_endpoints`** with **`scope`** (e.g. `all`) — routes + **`existingTests`** per endpoint.
4. **`kerno_start_environment`** — One `app`; get **`job_id`** / **`log_path`**.
5. **`kerno_job`** — Until **healthy** or **failed** (sparse **`wait=false`** or **`log_path`**; not a tight loop).
6. Optionally **`kerno_validate`** — Run scenarios against the live stack (`kind`: `validate`). **After handler or API changes, prefer this before editing anything under `.kerno/scenarios/`.** Then **`kerno_job`** until terminal.
7. (Optional) **`kerno_capture_baseline`** — author or regenerate scenario files and run them (`kind`: `capture_baseline`). Same `workspace_path` / `app` model as `kerno_start_environment`. Use when scenarios are missing or need Kerno-driven rewrites—not as a substitute for step 6 when you only need to run tests. Then **`kerno_job`** until terminal for that `job_id`. See [capture-baseline.md](capture-baseline.md).
8. Optionally **`kerno_approve`** / **`kerno_reject`** — after reviewing validate output; synchronous acknowledgements (optional **`reason`**).
9. **`kerno_compose_status`**, **`kerno_environments_status`**, **`kerno_compose_logs`** as needed.

## Anti-patterns

- Hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase API changes; run **`kerno_validate`** first, then **`kerno_capture_baseline`** with the same scope if Kerno should rewrite scenarios.
- Call **`kerno_compose_up`** / **`kerno_compose_down`** while **`kerno_start_environment`** is still running for that app; wait for **`kerno_job`** first.
- Launch a second **`kerno_capture_baseline`** while one is already running for the same workspace + scope + app selection (deduped; see `mcp.md`).
