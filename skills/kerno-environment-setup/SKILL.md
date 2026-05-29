---
name: kerno-environment-setup
description: This skill should be used when the user asks to set up the environment, start the stack, bring up services, bootstrap the env, or run /kerno-env. Enforces the compose-plan user approval gate and handles needs_user_feedback as a hard stop before calling kerno_start_environment.
version: 0.1.0
---

# Kerno MCP — environment setup (compose plan approval gate)

Use this workflow whenever the user asks to “set up the env”, “bootstrap”, “start the stack”, or similar. Those phrases are **not** approval of a compose plan.

## Preconditions

1. `kerno_healthcheck`
2. If you changed code since Kerno last analyzed/snapshotted the workspace (or results look stale), call **`kerno_sync_workspace`** first (optionally inspect snapshot state via **`kerno_list_workspaces`**).
3. `kerno_get_applications` → pick **`app`**

## Plan gate (mandatory — do not skip)

1. Call **`kerno_compose_plan`** with `workspace_path` and `app`.
2. If it returns `no_plan_yet`, call **`kerno_compose_plan_generate`** → complete with **`kerno_job`**.
3. Show the plan to the user and stop for approval.
   - Include a short summary (services, ports, test user if present).
   - Include the plan’s **Open Questions** section verbatim when it exists (or a faithful bullet list extracted from it).
   - Ask for explicit approval or requested changes.
4. If the user wants changes, call **`kerno_compose_plan_feedback`** with their free-text instruction → **`kerno_job`** → show updated plan → ask again.
5. **Only after explicit user approval** (e.g. “approved”, “looks good”, “use defaults”, or they answer each open question), call **`kerno_start_environment`**.

### Required approval message template

```markdown
### Compose plan review

**Summary:** <1–3 sentences>

**Open questions** (answer these or say “use Kerno defaults”):

1. <question 1>
2. <question 2>

**Planned services:** <postgres, redis, ...>

**Waiting for:** your approval before starting the build.
```

## Start environment

1. Call **`kerno_start_environment`** with `workspace_path` and `app` (optional `regenerate=true` when explicitly requested).
2. Poll with **`kerno_job`** using sparse checks (`wait=false` every few minutes) or read `log_path`. Do not loop tightly.

### During `kerno_job` (start_environment)

- If `status === needs_user_feedback`: **stop immediately**.
  - Paste `result.question` (and options if present) to the user.
  - Do not keep polling.
  - Call **`kerno_compose_plan_feedback`** with their answer, show the updated plan again, then re-run the approval gate before retrying `kerno_start_environment`.

## After environment is up

1. Call **`kerno_compose_status`** and confirm **`ready_for_validation: true`**. Do not treat `status: Up` as sufficient.
2. Proceed to validation (`kerno_validate`) or scenario authoring (plan/implement baseline) as needed.

## Anti-patterns

- Treating “setup the env” / “bootstrap” as approval of the compose plan or open questions.
- Calling `kerno_start_environment` without pasting **Open Questions** to the user.
- Continuing `kerno_job` polling when status is `needs_user_feedback`.

