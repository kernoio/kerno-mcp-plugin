---
name: kerno-environment-setup
description: This skill should be used when the user asks to set up the environment, start the stack, bring up services, or run /kerno-env. Prefers local dev flow when the repo has docker-compose or scripts; orchestrate only on user request or when no easy startup exists.
version: 0.3.0
---

# Kerno MCP — environment setup (unified)

Use this workflow when the user asks to “set up the env”, “start the stack”, “bring up services”, or similar.

**References (read before acting):**

- `references/target-environment.md` — choose **`local`**, **`remote`**, or **`orchestrate`**
- `references/workspace-config.md` — **`kerno_save_config`** fields
- `references/state-and-jobs.md` — orchestrate feedback and **`kerno_job`** polling
- `references/unified-flow.md` — anti-patterns

## Preconditions

1. **`kerno_healthcheck`**
2. If results look stale, call **`kerno_sync_workspace`** first (optionally **`kerno_list_workspaces`**).
3. **`kerno_get_applications`** → pick **`app`**

## Step 1: Choose target_environment

Follow the decision flow in **`target-environment.md`**. Default **`local`**: start the repo's dev flow **before** **`kerno_save_config`** when easy startup exists. Use **`orchestrate`** only on explicit user request or when the repo has no easy full-stack startup.

## Step 2: kerno_save_config

Call **`kerno_save_config`** with `workspace_path` and `applications: [{ app, target_environment, sut_url?, ...db env blocks }]`.

Field details: **`workspace-config.md`**.

## Step 3: environment_setup

Call **`kerno_environment_setup`** with `workspace_path` and `app`.

- **local / remote:** synchronous SUT probe; fix config if `missing_config`
- **orchestrate:** may return **`job_id`** for compose-plan + start-environment background work

Optional: **`regenerate_instructions`**, **`sut_url`** (persist before probing for local/remote).

## Step 4: Orchestrate feedback (when needed)

On the orchestrate path, use the read plane per **`state-and-jobs.md`** (composeplan resource, **`kerno_feedback_pending`**, **`kerno_feedback_answer`** / **`answer_feedback_request`**).

Show plan summaries and **open questions** to the user before proceeding. User phrases like “setup the env” are **not** implicit approval — ask explicitly when the plan has open questions.

Poll **`kerno_job`** with **`wait=false`** every few minutes or read **`log_path`**. On terminal **`needs_user_feedback`**, stop and relay **`result.question`**.

## Step 5: environment_status

Call **`kerno_environment_status`** until **`ready_for_endpoint_test: true`**. Check **`next_action`** when not ready.

## After environment is ready

Proceed to **`kerno_list_endpoints`** then **`kerno_endpoint_test`** — load `skills/kerno-endpoint-test/SKILL.md`.
