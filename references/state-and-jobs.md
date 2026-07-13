# State plane, job registry, and feedback

Three cooperating observability mechanisms on the unified MCP surface (ADR-0016).

## Job registry (`kerno_job`)

### Launch tools that return `job_id`

| Launch tool | `kind` | When |
|-------------|--------|------|
| **`kerno_endpoint_test`** | `endpoint_test` | Always async |

Each returns **`job_id`**, **`log_path`** (`<workspace>/.kerno/mcp-jobs/<job_id>.log`), **`status`**: `running`.

### Polling semantics

- **`wait`** default **true** — blocks until terminal or server wait budget (~60s); MCP hosts usually cap the HTTP round-trip anyway
- Prefer **`wait=false`** every few minutes or read **`log_path`**
- **Do not** tight-loop **`kerno_job`**
- First **terminal** response retires **`job_id`** and deletes the log file
- **`kerno_cancel`** is fire-and-forget; next **`kerno_job`** returns **`cancelled`** once

## Read plane (FSM state)

| Tool | Role |
|------|------|
| **`kerno_get_state(resource_id)`** | Snapshot; optional **`until_status`** long-poll (default timeout ~45s) |
| **`kerno_list_state(prefix)`** | Discover resources under a prefix |
| **`kerno_poll_events(prefix, cursor)`** | Event replay; handle **`gap=true`** by re-reading state |

### Resource IDs (examples)

- Endpoint test: `workspace/<ws>/app/<app>/endpoint/<METHOD>/<path>/endpointtest`
- Feedback subresources: `.../feedback`

### Endpoint-test status set

`working` | `awaiting_approval` | `awaiting_answer` | `ready` | `failed`

Long-poll with **`until_status`**: `["awaiting_approval","awaiting_answer","ready","failed"]`.

## Feedback (human gates)

Two equivalent paths — prefer **Family A** for app-scoped UX:

### Family A (app-scoped)

1. **`kerno_feedback_pending`** — `{request_id, prompt, schema, resource_id}` or `{status: none}`
2. **`kerno_feedback_answer`** — submit structured **`payload`** matching schema

### Generic (resource-scoped)

1. **`kerno_get_state`** on `<resource_id>/feedback` — find open **`request_id`**
2. **`answer_feedback_request`** — same payload shapes: `{"answer":"..."}` or `{"approved":true}` / `{"approved":false,"reason":"..."}`

### Gate contexts

| Context | Trigger | Action |
|---------|---------|--------|
| Endpoint-test plan review | GOAP `reviewPlan` parks on **`awaiting_approval`** | Answer via feedback tools → run resumes; rejection replans |

## When to use which

| Need | Use |
|------|-----|
| Job progress / terminal result | **`kerno_job`** or **`log_path`** |
| Endpoint-test plan gate | **`kerno_feedback_pending`** or **`kerno_get_state`** on endpoint-test resource |
| Event-driven client | **`kerno_poll_events`** with cursor protocol |

See [unified-flow.md](unified-flow.md) for the canonical sequence.
