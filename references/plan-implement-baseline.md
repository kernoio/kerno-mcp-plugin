# `kerno_plan_baseline` and `kerno_implement_baseline` reference

Scenario authoring is a **two-stage** async workflow (plus an optional **sync** planning mode). There is **no** `kerno_capture_baseline` tool in the shipped MCP surface.

## Overview

| Tool | When | Requires env |
| --- | --- | --- |
| **`kerno_plan_baseline`** | Produce a plan payload (**`plan_json`** / **`plan_sync`**) describing scenarios to keep/add/update/delete | No — uses workspace analysis only |
| **`kerno_implement_baseline`** | Generate **`.scenario.ts`** files and run them against the live stack | Yes — **`ready_for_validation`** must be true |

Complete each async launch with **`kerno_job`** (see [tool-ordering.md](tool-ordering.md) and [mcp-client-config.md](mcp-client-config.md)).

## `kerno_plan_baseline`

### Modes

**Async (batch):** pass **`scope`** (not **`changed`**). Returns **`job_id`**, **`log_path`**, **`kind`**: `plan_baseline`. Complete with **`kerno_job`**.

**Sync (single endpoint):** omit **`scope`**; pass **`method`** and **`path`** together. Returns **`job`** null and **`plan_sync`** (`plan`, `pending_scenario_ids`, `ok`, `message`). No **`kerno_job`** poll for that call. Optional **`plan_review_instructions`** on each round-trip.

Do **not** pass **`scope`** together with **`method`** + **`path`**.

### Parameters

| Field | Required | Notes |
| --- | --- | --- |
| **`workspace_path`** | yes | Absolute path; must match agent `WORKSPACE`. |
| **`scope`** | async only | `all`, `file:<workspace-relative path>`, or `endpoint:METHOD /path`. Not `changed`. |
| **`method`** / **`path`** | sync only | HTTP method and path for one endpoint. |
| **`app`** | no | Optional for `all` (omit = all HTTP apps). For `endpoint:` / `file:` when ambiguous, set module id from **`kerno_get_applications`**. |
| **`workspace_id`** | no | If set, must match analyzed workspace. |
| **`plan_review_instructions`** | no | Natural-language refinement; reference scenario ids from a prior **`plan_json`** to adjust guidance or coverage. |

### Terminal payload (`kerno_job`, async)

When **`kind`** is `plan_baseline` and the job is finished, the JSON may include:

- **`plan_baseline`** — Object with **`summary`** and **`endpoints`**: list of `{ app, method, path, success, error?, plan_json? }` where **`plan_json`** is a JSON document containing `scenarios` with **`id`**, **`guidance`**, and **`status`** (`keep`, `updated`, `added`, or `deleted`).

## `kerno_implement_baseline`

### Prerequisites

- **`kerno_plan_baseline`** has run at least once for each endpoint in scope — present **`plan_json`** or **`plan_sync`** to the user for review; optionally refine via sync **`kerno_plan_baseline`** before implementing.
- **`ready_for_validation`** is **`true`** for the relevant app(s) — confirm via **`kerno_compose_status`**. Status **`Up`** alone is insufficient.
- Prefer **`kerno_compose_up`** when compose files already exist before **`kerno_start_environment`**.

### Parameters

| Field | Required | Notes |
| --- | --- | --- |
| **`workspace_path`** | yes | Absolute path; must match agent `WORKSPACE`. |
| **`scope`** | yes | Same grammar as async **`kerno_plan_baseline`**: `all`, `file:…`, `endpoint:METHOD /path`. |
| **`app`** | no | Same rules as plan. |
| **`workspace_id`** | no | If set, must match analyzed workspace. |

Returns **`job_id`**, **`log_path`**, **`kind`**: `implement_baseline`. Complete with **`kerno_job`**.

### Terminal payload (`kerno_job`)

When **`kind`** is `implement_baseline` and the job is finished, the JSON may include:

- **`implement_baseline`** — Object with **`summary`** and **`endpoints`**: list of `{ app, method, path, success, error?, run? }` where **`run`** mirrors validate's structured scenario run when present.

## Deduping

**`plan_baseline`** and **`implement_baseline`** share one dedupe slot per workspace **+** normalized scope **+** app selection — only one may run at a time for that key. A second launch fails until the first finishes.

## Scopes (summary)

| Scope | Plan (async) | Implement | Validate |
| --- | --- | --- | --- |
| `all` | yes | yes | yes |
| `changed` | no | no | yes |
| `file:<path>` | yes | yes | yes |
| `endpoint:METHOD /path` | yes | yes | yes |

For **`changed`** or git-driven validation, use **`kerno_validate`** — not async plan.
