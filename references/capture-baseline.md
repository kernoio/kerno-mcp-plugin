# `kerno_capture_baseline` reference

Async tool: returns **`job_id`**, **`log_path`**, **`status`**: `running`, **`kind`**: `capture_baseline`. Finish with **`kerno_job`** (see [tool-ordering.md](tool-ordering.md) and [mcp-client-config.md](mcp-client-config.md)).

## Prerequisites

- **`kerno_get_applications`** has been run for this **`workspace_path`**.
- Environment is up: **`kerno_start_environment`** completed **`healthy`** via **`kerno_job`** for the relevant **`app`** (when using a single app).

## Parameters

| Field | Required | Notes |
| --- | --- | --- |
| **`workspace_path`** | yes | Absolute path; must match agent `WORKSPACE`. |
| **`scope`** | yes | `all`, `file:<workspace-relative path>`, or `endpoint:METHOD /path`. Not `changed` (use **`kerno_validate`**). |
| **`app`** | no | For `all`, omit to include all HTTP apps. For `endpoint:` / `file:` when ambiguous, set module id from **`kerno_get_applications`**. |
| **`workspace_id`** | no | If set, must match analyzed workspace. |
| **`user_message`** | no | Extra context for planning (passed to plan). |

## Terminal payload (`kerno_job`)

When `kind` is `capture_baseline` and the job is finished, the JSON may include:

- **`capture_baseline`** — Object with **`summary`** and **`endpoints`**: list of `{ app, method, path, success, error?, run? }` where **`run`** mirrors validate’s structured scenario run when present.

Only one **`capture_baseline`** job may run at a time per workspace **+** normalized scope **+** app selection. A second launch fails until the first finishes.
