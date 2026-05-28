# Kerno MCP — recommended tool order

Use this as a **default** sequence when the user does not specify otherwise. Details: `agent/apps/agent/docs/mcp.md` in the aicore repo.

1. **`kerno_healthcheck`** — Docker, git, auth (optional `workspace_path`). Intentionally waits **120 seconds** (SSE timeout testing).
2. **`kerno_get_applications`** — Analyze workspace; note `workspace_id` if you will pass it to later tools.
3. Optionally **`kerno_list_endpoints`** — **requires `scope`** (`all`, `changed`, `file:…`, `endpoint:…`); routes + **`existingTests`** per endpoint.
4. **Bring the stack up** for one `app`:
   - Prefer **`kerno_compose_up`** when compose files already exist (synchronous).
   - First-time setup: **`kerno_compose_plan`** → if `no_plan_yet`, **`kerno_compose_plan_generate`** → show plan → **`kerno_compose_plan_feedback`** loop → **user approval** → **`kerno_start_environment`** (optional `regenerate=true`). See [compose-plan.md](compose-plan.md).
   - **`kerno_job`** only when step 4 used an async launch (`start_environment`, compose plan jobs). Terminals for `start_environment`: **`healthy`**, **`needs_user_feedback`**, **`failed`**, **`cancelled`**. On **`needs_user_feedback`**, stop and ask the user.
   - Confirm **`ready_for_validation`** via **`kerno_compose_status`** before validate or implement (`status: Up` ≠ ready).
5. Optionally **`kerno_plan_baseline`** — async: pass **`scope`** (not `changed`); optional **`plan_review_instructions`**. Sync single endpoint: **`method`** + **`path`**, omit **`scope`**. Async returns **`job_id`** / **`kind`**: `plan_baseline`; complete with **`kerno_job`**. See [plan-implement-baseline.md](plan-implement-baseline.md).
6. Optionally **`kerno_implement_baseline`** — requires prior plan for endpoints in scope and **`ready_for_validation`**. Same **`scope`** / **`app`** model. **`kind`**: `implement_baseline`; complete with **`kerno_job`**.
7. Optionally **`kerno_validate`** — run scenarios against the live stack (`kind`: `validate`). **After handler or API changes, prefer this before editing anything under `.kerno/scenarios/`** (`scope: changed` or `endpoint:…`). Requires **`ready_for_validation`**. Complete with **`kerno_job`**.
8. Optionally **`kerno_approve`** / **`kerno_reject`** — after reviewing validate output; synchronous acknowledgements (optional **`reason`**).
9. **`kerno_compose_status`**, **`kerno_environments_status`**, **`kerno_compose_logs`** as needed.
10. **`kerno_cancel`** — stop an in-flight async job when the user asks or the result is no longer needed (fire-and-forget).

## Anti-patterns

- Hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase API changes; run **`kerno_validate`** first, then **`kerno_plan_baseline`** / **`kerno_implement_baseline`** with the same scope if Kerno should rewrite scenarios.
- Call **`kerno_compose_up`** / **`kerno_compose_down`** while **`kerno_start_environment`** is still running for that app; wait for **`kerno_job`** first.
- Launch a second **`plan_baseline`** or **`implement_baseline`** while one is already running for the same workspace + scope + app selection (deduped; see `mcp.md`).
- Call **`kerno_start_environment`** without user-approved compose plan on first setup.
- Treat compose **`status: Up`** or **`healthy`** job status as ready for validate/implement without checking **`ready_for_validation`**.
- Treating “setup the env” / “bootstrap” / “start the stack” as approval of the compose plan or its open questions.
- Calling **`kerno_start_environment`** without pasting **Open Questions** to the user (verbatim or faithfully extracted).
- Continuing **`kerno_job`** polling when status is **`needs_user_feedback`**.
