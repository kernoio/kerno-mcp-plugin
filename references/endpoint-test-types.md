# Endpoint test types (`kerno_endpoint_test`)

**`kerno_endpoint_test`** runs an async job for **one endpoint**. Requires **`ready_for_endpoint_test`** from **`kerno_environment_status`**. Complete with **`kerno_job`** (`kind`: `endpoint_test`).

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workspace_path` | yes | Absolute workspace root |
| `app` | yes | Module id from **`kerno_get_applications`** |
| `endpoint_method` | yes | e.g. `GET` |
| `endpoint_path` | yes | e.g. `/api/users` |
| `type` | yes | `generate` or `validate` |
| `implementation` | no | `reflective` (default) or `standard` |

## type: generate vs validate

| `type` | When to use |
|--------|-------------|
| **`generate`** | No scenarios yet, or API changed and Kerno should rewrite scenarios (GOAP: analyze → plan → reviewPlan → implement → run) |
| **`validate`** | Scenarios exist on disk; run against live SUT only |

Use **`kerno_list_endpoints`** with matching **`scope`** to inspect **`existingTests`** per route before choosing:

- Empty **`existingTests`** → usually **`generate`**
- Scenarios on disk → **`validate`** first after code changes

## implementation strategies

| Value | Behavior |
|-------|----------|
| **`reflective`** (default) | Writes and runs the scenario, then adversarially reflects on correctness before looping to fix |
| **`standard`** | Skips the reflection step |

## After code changes

1. **`kerno_endpoint_test`** with **`type=validate`**
2. If failures indicate stale scenarios, **`type=generate`** for that endpoint
3. **Never** hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase handler or API changes

## Scope grammar (for list_endpoints prefetch)

Same as endpoint discovery: **`all`**, **`changed`**, **`file:<path>`**, **`endpoint:METHOD /path`**.

**`kerno_list_endpoints`** requires **`scope`** — use **`all`** to list every route for the app selection.

## Feedback gates (generate only)

A **`type=generate`** run can pause for:

- **`awaiting_approval`** — plan review (GOAP `reviewPlan`)
- **`awaiting_answer`** — free-text planner question

These are **gate statuses**, not job failures. **`kerno_job`** shows job progress but **not** feedback gates — a gated job may look stuck there.

When stalled:

1. **`kerno_feedback_pending`** (workspace + app), **or**
2. **`kerno_get_state`** on endpoint-test resource id `workspace/<ws>/app/<app>/endpoint/<METHOD>/<path>/endpointtest`

Answer with **`kerno_feedback_answer`** or **`answer_feedback_request`**, then the run resumes.

Rejection on plan review triggers replan (GOAP replan loop).

See [state-and-jobs.md](state-and-jobs.md) and **`skills/kerno-endpoint-test/SKILL.md`**.

## Blocked scenarios (DB access)

A scenario that needs the database (**`requiredDependencies: [database]`**) is reported **`[BLOCKED]`** in a **black box** (HTTP-only) run — or in a greybox run where Kerno can't derive the DB schema. **Blocked is not failed:** the scenario didn't run, so it's neither pass nor fail. To unblock, provide DB access (greybox) — see [workspace-config.md](workspace-config.md#database-access-requires-a-derivable-schema). If DB access isn't possible, tell the user those scenarios can't run and only API-level validation is covered.
