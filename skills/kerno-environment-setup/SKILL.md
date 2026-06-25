---
name: kerno-environment-setup
description: This skill should be used when the user asks to set up the environment, start the stack, bring up services, or run /kerno-env. Prefers local dev flow when the repo has docker-compose or scripts; orchestrate only on user request or when no easy startup exists.
version: 0.2.0
---

# Kerno MCP — environment setup (unified)

Use this workflow when the user asks to “set up the env”, “start the stack”, “bring up services”, or similar.

**Default:** prefer **`local`** when the repository already has a routine way to start the full stack (`docker compose`, `npm run dev`, `make run`, README quickstart). The MCP client starts that flow **before** **`kerno_save_config`**. Use **`orchestrate`** only when the user explicitly asks Kerno to orchestrate the environment, **or** when the repo has no such startup path. See `${CLAUDE_PLUGIN_ROOT}/references/target-environment.md`.

## Preconditions

1. **`kerno_healthcheck`**
2. If you changed code since Kerno last analyzed/snapshotted the workspace (or results look stale), call **`kerno_sync_workspace`** first (optionally inspect snapshot state via **`kerno_list_workspaces`**).
3. **`kerno_get_applications`** → pick **`app`**

## Step 1: Choose target_environment

Inspect the repository for an **easy full-stack startup** — for example `docker-compose.yml`, `compose.yaml`, `package.json` scripts, a `Makefile`, or documented dev commands in the README.

| Situation | `target_environment` | Before `save_config` | `sut_url` |
|-----------|---------------------|----------------------|-----------|
| Repo has easy startup **and** user did not ask Kerno to orchestrate | **`local`** | **Start the stack** with the repo's dev flow (`docker compose up`, `npm run dev`, etc.) | Required once SUT is up (e.g. `http://localhost:8080`) |
| SUT already runs on staging / a remote host | **`remote`** | None — user or CI already started it | Required |
| User **explicitly** asks Kerno to orchestrate / bootstrap the environment | **`orchestrate`** | None — Kerno owns bootstrap | Omit |
| No easy full-stack startup in the repo | **`orchestrate`** | None — Kerno owns bootstrap | Omit |

**User override:** phrases like “orchestrate”, “bootstrap with Kerno”, or “have Kerno bring up the stack” → **`orchestrate`** even when `docker-compose.yml` or dev scripts exist.

**Do not** pick **`orchestrate`** only because the SUT is not running yet — on the local path, **start it with the repo's own tooling first**, then save config.

## Step 2: kerno_save_config

Call **`kerno_save_config`** with `workspace_path` and `applications: [{ app, target_environment, sut_url?, ...db env blocks }]`.

Include dependency connection env vars (postgres, redis, etc.) when the local stack exposes them. Details: `${CLAUDE_PLUGIN_ROOT}/references/workspace-config.md`.

## Step 3: environment_setup

Call **`kerno_environment_setup`** with `workspace_path` and `app`.

- **local / remote:** synchronous SUT probe; fix config if `missing_config`
- **orchestrate:** may return **`job_id`** for compose-plan + start-environment background work

Optional:

- **`regenerate_instructions`** — user guidance for docker orchestrator after failure or to steer provisioning
- **`sut_url`** — persist before probing for local/remote

## Step 4: Orchestrate feedback (when needed)

On the orchestrate path, compose-plan may open questions or require approval. Use the read plane:

1. **`kerno_get_state`** on composeplan resource_id `workspace/<ws>/module/<app>/composeplan`
2. When state carries **`open_feedback`**, read `.../feedback` or call **`kerno_feedback_pending`**
3. Answer with **`kerno_feedback_answer`** or **`answer_feedback_request`**
4. Re-run **`kerno_environment_setup`** if the flow requires it after answers

Show plan summaries and **open questions** to the user before proceeding. User phrases like “setup the env” are **not** implicit approval — ask explicitly when the plan has open questions.

### During start_environment job

Poll with **`kerno_job`** (`wait=false` every few minutes) or read **`log_path`**.

If terminal **`needs_user_feedback`**: **stop immediately**, paste **`result.question`** to the user, answer via feedback tools, then retry setup as appropriate.

## Step 5: environment_status

Call **`kerno_environment_status`** until **`ready_for_endpoint_test: true`**.

Do not treat **`status: Up`** alone as sufficient. Check **`next_action`** when not ready.

## After environment is ready

Proceed to **`kerno_list_endpoints`** then **`kerno_endpoint_test`** — see `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md`.

## Anti-patterns

- Picking **`orchestrate`** when the repo has `docker-compose.yml`, dev scripts, or a documented quickstart — start the stack locally first unless the user asked Kerno to orchestrate
- Calling **`kerno_save_config`** with **`local`** before starting the stack when the repo has easy startup
- Skipping **`kerno_save_config`** before **`kerno_environment_setup`**
- Calling **`kerno_endpoint_test`** before **`ready_for_endpoint_test`**
- Continuing **`kerno_job`** polling when status is **`needs_user_feedback`**
- Tight-loop **`kerno_job`** polling
