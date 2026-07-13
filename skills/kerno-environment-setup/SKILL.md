---
name: kerno-environment-setup
description: This skill should be used when the user asks to set up the environment, start the stack, bring up services, or run /kerno-env. Starts the app locally (or points at a remote SUT), wires DB access for greybox testing, and falls back to HTTP-only black box when DB access isn't possible.
version: 0.4.0
---

# Kerno MCP — environment setup (unified)

Use this workflow when the user asks to “set up the env”, “start the stack”, “bring up services”, or similar.

**References (read before acting):**

- `references/target-environment.md` — choose **`local`** or **`remote`**; greybox vs black box (DB access)
- `references/workspace-config.md` — **`kerno_save_config`** fields and DB-access requirements
- `references/unified-flow.md` — anti-patterns

## Preconditions

1. **`kerno_healthcheck`**
2. If results look stale, call **`kerno_sync_workspace`** first (optionally **`kerno_list_workspaces`**).
3. **`kerno_get_applications`** → pick **`app`**

## Step 1: Choose environment

Follow the decision flow in **`target-environment.md`**. Two choices:

- **Where the SUT runs** — **`local`** (default: start the repo's dev flow **before** **`kerno_save_config`**) or **`remote`** (env runs somewhere other than this machine, e.g. cloud).
- **DB-access posture** — **greybox** (recommended): wire DB credentials so DB-backed scenarios run. **Black box** (fallback): HTTP-only when DB access isn't possible — **tell the user** that scenarios requiring direct DB access will be reported **`[BLOCKED]`**.

## Step 2: kerno_save_config

Call **`kerno_save_config`** with `workspace_path` and `applications: [{ app, target_environment, sut_url?, ...db env blocks }]`.

Field details: **`workspace-config.md`**.

## Step 3: environment_setup

Call **`kerno_environment_setup`** with `workspace_path` and `app`. This is a **synchronous SUT probe** for both `local` and `remote`; fix config if `missing_config`.

Optional: **`sut_url`** (persist before probing).

## Step 4: environment_status

Call **`kerno_environment_status`** until **`ready_for_endpoint_test: true`**. Check **`next_action`** when not ready.

## After environment is ready

Proceed to **`kerno_list_endpoints`** then **`kerno_endpoint_test`** — load `skills/kerno-endpoint-test/SKILL.md`.
