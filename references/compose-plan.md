# Docker Compose plan workflow

Before the first **`kerno_start_environment`** for an app, the user must review and approve a compose plan. Prefer **`kerno_compose_up`** when Kerno-generated compose files already exist on disk.

## Tools

| Tool | Sync/async | Role |
| --- | --- | --- |
| **`kerno_compose_plan`** | sync | Read existing **`.kerno/analysis/docker-compose-plan.md`** for one app |
| **`kerno_compose_plan_generate`** | async | Run analyzers + plan formatter; persist plan markdown |
| **`kerno_compose_plan_feedback`** | async | Apply user free-text feedback to the plan |
| **`kerno_start_environment`** | async | Build and bring up services after plan approval |
| **`kerno_compose_up`** | sync | Start/restart stack from existing files (cheap; no LLM) |

Complete async tools with **`kerno_job`**. Job kinds: **`compose_plan_generate`**, **`compose_plan_feedback`**, **`start_environment`**.

## Recommended first-time flow

1. **`kerno_compose_plan`** with **`workspace_path`** and **`app`**.
2. If the response is **`no_plan_yet`**, call **`kerno_compose_plan_generate`** → **`kerno_job`** until terminal.
3. Show **`compose_plan.plan_markdown`** (from job terminal JSON or read tool) to the user.
4. If the user wants changes, call **`kerno_compose_plan_feedback`** with required **`feedback`** → **`kerno_job`** → show updated plan. Repeat as needed.
5. Only after **explicit user approval**, call **`kerno_start_environment`** (optional **`regenerate=true`** to bust compose-guidance cache).
6. **`kerno_job`** until terminal. For **`start_environment`**, terminals include **`healthy`**, **`needs_user_feedback`**, **`failed`**, or **`cancelled`**.
7. On **`needs_user_feedback`**, stop and relay **`result.question`** to the user. Call **`kerno_compose_plan_feedback`** with their answer — not only regenerate — so **`.kerno/analysis/orchestration-run-summary.md`** is incorporated when present.
8. Confirm **`ready_for_validation`** via **`kerno_compose_status`** before validate or implement.

## When compose files already exist

Use **`kerno_compose_up`** instead of **`kerno_start_environment`**. Then check **`ready_for_validation`** — do **not** treat **`status: Up`** as sufficient.

## Parameters

All compose-plan read/generate/feedback tools require **`workspace_path`** and **`app`**.

**`kerno_compose_plan_feedback`** additionally requires **`feedback`** — free-text user instructions (service versions, secrets, build steps, answers to orchestrator questions).

## Latency (typical)

- **`kerno_compose_plan_generate`**: ~70–130s uncached; near-instant on cache hit for same source commit.
- **`kerno_compose_plan_feedback`**: ~75–150s per round (always runs an LLM pass).

MCP hosts cap a single tool call around **~60s**; use sparse **`kerno_job`** polling with **`wait=false`** or read **`log_path`**.

## Anti-patterns

- Call **`kerno_start_environment`** without showing the plan and receiving user approval.
- Treat **`needs_user_feedback`** as success or generic failure.
- Call **`kerno_compose_up`** / **`kerno_compose_down`** while **`kerno_start_environment`** is still running for the same app — wait for **`kerno_job`** first.
- Use **`kerno_start_environment`** when compose files exist and **`kerno_compose_up`** would suffice.
