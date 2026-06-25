---
name: kerno-environment-setup
description: This skill should be used when the user asks to set up the environment, start the stack, bring up services, bootstrap the env, configure target environment, or run /kerno-env. Guides save_config, environment_setup, environment_status, and orchestrate feedback via the read plane.
version: 0.2.0
---

# Kerno MCP — environment setup (unified)

Use this workflow when the user asks to “set up the env”, “bootstrap”, “start the stack”, “orchestrate”, or similar.

## Preconditions

1. **`kerno_healthcheck`**
2. If you changed code since Kerno last analyzed/snapshotted the workspace (or results look stale), call **`kerno_sync_workspace`** first (optionally inspect snapshot state via **`kerno_list_workspaces`**).
3. **`kerno_get_applications`** → pick **`app`**

## Step 1: Choose and save config

Decide **`target_environment`** — see `${CLAUDE_PLUGIN_ROOT}/references/target-environment.md`:

| User situation | `target_environment` | `sut_url` |
|----------------|---------------------|-----------|
| SUT already running locally | `local` | Required (e.g. `http://localhost:8080`) |
| SUT on staging / remote host | `remote` | Required |
| No SUT yet / full bootstrap | `orchestrate` | Omit |

Call **`kerno_save_config`** with `workspace_path` and `applications: [{ app, target_environment, sut_url?, ...db env blocks }]`.

Details: `${CLAUDE_PLUGIN_ROOT}/references/workspace-config.md`.

## Step 2: environment_setup

Call **`kerno_environment_setup`** with `workspace_path` and `app`.

- **local / remote:** synchronous SUT probe; fix config if `missing_config`
- **orchestrate:** may return **`job_id`** for compose-plan + start-environment background work

Optional:

- **`regenerate_instructions`** — user guidance for docker orchestrator after failure or to steer provisioning
- **`sut_url`** — persist before probing for local/remote

## Step 3: Orchestrate feedback (when needed)

On the orchestrate path, compose-plan may open questions or require approval. Use the read plane:

1. **`kerno_get_state`** on composeplan resource_id `workspace/<ws>/module/<app>/composeplan`
2. When state carries **`open_feedback`**, read `.../feedback` or call **`kerno_feedback_pending`**
3. Answer with **`kerno_feedback_answer`** or **`answer_feedback_request`**
4. Re-run **`kerno_environment_setup`** if the flow requires it after answers

Show plan summaries and **open questions** to the user before proceeding. User phrases like “setup the env” are **not** implicit approval — ask explicitly when the plan has open questions.

### During start_environment job

Poll with **`kerno_job`** (`wait=false` every few minutes) or read **`log_path`**.

If terminal **`needs_user_feedback`**: **stop immediately**, paste **`result.question`** to the user, answer via feedback tools, then retry setup as appropriate.

## Step 4: environment_status

Call **`kerno_environment_status`** until **`ready_for_endpoint_test: true`**.

Do not treat **`status: Up`** alone as sufficient. Check **`next_action`** when not ready.

## After environment is ready

Proceed to **`kerno_list_endpoints`** then **`kerno_endpoint_test`** — see `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md`.

## Anti-patterns

- Skipping **`kerno_save_config`** before **`kerno_environment_setup`**
- Calling **`kerno_endpoint_test`** before **`ready_for_endpoint_test`**
- Continuing **`kerno_job`** polling when status is **`needs_user_feedback`**
- Tight-loop **`kerno_job`** polling
