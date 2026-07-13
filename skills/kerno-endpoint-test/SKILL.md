---
name: kerno-endpoint-test
description: This skill should be used when the user asks to generate or validate endpoint tests, run scenarios, test an API route, or run /kerno-endpoint-test. Guides kerno_list_endpoints, kerno_endpoint_test (generate vs validate), kerno_job, and plan-review feedback gates.
version: 0.2.1
---

# Kerno MCP — endpoint test workflow

Use when the user wants to **generate** scenarios, **validate** existing scenarios, or test a specific HTTP endpoint.

**References (read before acting):**

- `references/endpoint-test-types.md` — **`type`**, **`implementation`**, feedback gates, after code changes
- `references/state-and-jobs.md` — read plane and **`kerno_job`** when jobs stall
- `references/changes-detected.md` — optional post-edit hook
- `references/unified-flow.md` — anti-patterns

## Preconditions

1. **`kerno_environment_status`** reports **`ready_for_endpoint_test: true`** for the **`app`**
2. If not ready, load `skills/kerno-environment-setup/SKILL.md` first

## Step 1: Discover endpoints

Call **`kerno_list_endpoints`** with **`workspace_path`**, required **`scope`**, and optional **`app`**. Inspect **`existingTests`** per route — see **`endpoint-test-types.md`**.

## Step 2: Choose type

Follow **`endpoint-test-types.md`** (generate vs validate from **`existingTests`** and task). Do not hand-edit `.kerno/scenarios/**/*.scenario.ts`.

## Step 3: kerno_endpoint_test

Call with `workspace_path`, `app`, `endpoint_method`, `endpoint_path`, `type`, and optional `implementation`. Returns **`job_id`**, **`log_path`**, **`kind`**: `endpoint_test`.

## Step 4: kerno_job and feedback gates

Poll with sparse **`wait=false`** or read **`log_path`** — load `skills/kerno-background-job/SKILL.md`.

If a **generate** job stalls while still `running`, check plan-review gates via **`endpoint-test-types.md`** and **`state-and-jobs.md`** (not visible on **`kerno_job`** alone).

## User-facing messaging

Describe progress in plain language (planning coverage, running scenarios, pass/fail). Flag any **`[BLOCKED]`** scenarios — they need DB access (greybox) and did not run; see **`endpoint-test-types.md`**. Avoid MCP wiring jargon unless the user is debugging integration.
