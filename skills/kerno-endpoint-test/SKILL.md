---
name: kerno-endpoint-test
description: This skill should be used when the user asks to generate or validate endpoint tests, run scenarios, test an API route, or run /kerno-endpoint-test. Guides kerno_list_endpoints, kerno_endpoint_test (generate vs validate), kerno_job, and plan-review feedback gates.
version: 0.1.0
---

# Kerno MCP — endpoint test workflow

Use when the user wants to **generate** scenarios, **validate** existing scenarios, or test a specific HTTP endpoint.

## Preconditions

1. **`kerno_environment_status`** reports **`ready_for_endpoint_test: true`** for the **`app`**
2. If not ready, run **`skills/kerno-environment-setup/SKILL.md`** first

## Step 1: Discover endpoints

Call **`kerno_list_endpoints`** with:

- **`workspace_path`**
- **`scope`** (required): `all`, `changed`, `file:<path>`, or `endpoint:METHOD /path`
- optional **`app`**

Inspect **`existingTests`** per route. See `${CLAUDE_PLUGIN_ROOT}/references/endpoint-test-types.md`.

## Step 2: Choose type

| Situation | `type` |
|-----------|--------|
| No scenarios / first time | `generate` |
| Scenarios on disk; verify after code change | `validate` |
| Validate failed; scenarios stale vs API | `generate` |

**Never** hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase API changes.

## Step 3: kerno_endpoint_test

Call with:

- `workspace_path`, `app`
- `endpoint_method`, `endpoint_path`
- `type`: `generate` | `validate`
- optional `implementation`: `reflective` (default) or `standard`

Returns **`job_id`**, **`log_path`**, **`kind`**: `endpoint_test`.

## Step 4: kerno_job

Poll with sparse **`wait=false`** checks or read **`log_path`**. See `${CLAUDE_PLUGIN_ROOT}/skills/kerno-background-job/SKILL.md`.

## Plan-review feedback (generate only)

GOAP **`reviewPlan`** may park the run on **`awaiting_approval`** or **`awaiting_answer`**. These are **gates**, not failures — **`kerno_job`** alone may show the job as still running.

When stalled:

1. **`kerno_feedback_pending`** with `workspace_path` and `app`, **or**
2. **`kerno_get_state`** on `workspace/<ws>/app/<app>/endpoint/<METHOD>/<path>/endpointtest` with optional **`until_status`**: `["awaiting_approval","awaiting_answer","ready","failed"]`

Show the pending prompt to the user. Answer with:

- **`kerno_feedback_answer`** (app-scoped), **or**
- **`answer_feedback_request`** (resource-scoped on `.../feedback`)

Payload shapes:

- Free-text: `{"answer": "..."}`
- Approval: `{"approved": true}` or `{"approved": false, "reason": "..."}`

After answering, poll **`kerno_get_state`** or resume **`kerno_job`** until terminal.

Rejection on plan review triggers replan — the run continues automatically.

## After code changes

1. **`kerno_list_endpoints`** with `scope: changed` (optional hook: `${CLAUDE_PLUGIN_ROOT}/references/changes-detected.md`)
2. **`kerno_endpoint_test`** **`type=validate`** per impacted endpoint
3. If stale, **`type=generate`** — do not patch scenario files manually

## User-facing messaging

Describe progress in plain language (planning coverage, running scenarios, pass/fail). Avoid MCP wiring jargon unless the user is debugging integration.

## See also

- `${CLAUDE_PLUGIN_ROOT}/references/endpoint-test-types.md`
- `${CLAUDE_PLUGIN_ROOT}/references/state-and-jobs.md`
- `${CLAUDE_PLUGIN_ROOT}/references/unified-flow.md`
