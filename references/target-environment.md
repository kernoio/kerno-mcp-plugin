# Target environment decision tree

Choose **`target_environment`** in **`kerno_save_config`** before **`kerno_environment_setup`**. Valid values only: **`local`**, **`remote`**, **`orchestrate`**.

## Decision flow

```
User wants endpoint tests
        │
        ▼
  SUT already running?
    │           │
   yes          no
    │           │
    ▼           ▼
local/remote   orchestrate
+ sut_url      (omit sut_url)
    │           │
    └─────┬─────┘
          ▼
  kerno_environment_setup
          │
    ┌─────┴─────┐
    ▼           ▼
sync probe   async start_environment job
(local/remote) (orchestrate)
    │           │
    └─────┬─────┘
          ▼
  kerno_environment_status
  until ready_for_endpoint_test
          ▼
  kerno_list_endpoints → kerno_endpoint_test
```

## Comparison

| Choice | When | `sut_url` | `environment_setup` behavior |
|--------|------|-----------|------------------------------|
| **`local`** | SUT on this machine (user started it) | Required — probed from ts-sandbox | Sync SUT probe |
| **`remote`** | SUT elsewhere (staging, teammate's machine) | Required — probed from ts-sandbox | Sync SUT probe |
| **`orchestrate`** | User wants full bootstrap / no SUT yet | Omit | Compose-plan + async `start_environment` job |

## Orchestrate flow

When **`target_environment`** is **`orchestrate`**:

1. **`kerno_environment_setup`** — may return **`job_id`** for background work
2. **`kerno_get_state`** on composeplan resource_id — track plan generation and open questions
3. **`answer_feedback_request`** or **`kerno_feedback_pending`** / **`kerno_feedback_answer`** when feedback is open
4. Re-run **`kerno_environment_setup`** if needed after answering compose-plan questions
5. Poll **`kerno_job`** and **`kerno_environment_status`** until **`ready_for_endpoint_test`**

Compose-plan open questions and plan approval are **not** separate MCP tools on the unified surface — handle them via the read plane and feedback tools. See [state-and-jobs.md](state-and-jobs.md).

## Hard stops

**`needs_user_feedback`** on a **`start_environment`** job terminal payload is a **hard stop** — relay **`result.question`** to the user; do not proceed to endpoint tests until resolved.

## See also

- [workspace-config.md](workspace-config.md) — save_config fields and host gateway
- [unified-flow.md](unified-flow.md) — full checklist
