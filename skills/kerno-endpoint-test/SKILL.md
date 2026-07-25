---
name: kerno-endpoint-test
description: This skill should be used when the user asks to generate, validate, or update endpoint tests, run scenarios, test an API route, run security tests, or run /kerno-endpoint-test. Guides kerno_list_endpoints, kerno_endpoint_test (generate vs validate vs update, plus effort/box_testing_strategy/tags), kerno_job, and plan-review feedback gates.
version: 0.3.0
---

# Kerno MCP — endpoint test workflow

Use when the user wants to **generate** scenarios, **validate** existing scenarios, or test a specific HTTP endpoint.

**References (read before acting):**

- `references/endpoint-test-types.md` — **`type`**, **`effort`**, **`box_testing_strategy`**, **`tags`**, feedback gates, verdicts, after code changes
- `references/state-and-jobs.md` — read plane and **`kerno_job`** when jobs stall
- `references/changes-detected.md` — optional post-edit hook
- `references/unified-flow.md` — anti-patterns

## Preconditions

1. **`kerno_environment_status`** reports **`ready_for_endpoint_test: true`** for the **`app`**
2. If not ready, load `skills/kerno-environment-setup/SKILL.md` first

## Step 1: Discover endpoints

Call **`kerno_list_endpoints`** with **`workspace_path`**, required **`scope`**, and optional **`app`**. Inspect **`existingTests`** per route — see **`endpoint-test-types.md`**.

## Step 2: Choose type

Follow **`endpoint-test-types.md`**: **`generate`** when no scenarios exist or coverage should restart, **`validate`** to re-run existing scenarios after a code change, **`update`** when the endpoint changed intentionally and scenarios should follow. Do not hand-edit `.kerno/scenarios/**/*.scenario.ts`.

## Step 3: Resolve testing intent

Before the first **`kerno_endpoint_test`** call for an app/endpoint, check the user's **own** rules files (`CLAUDE.md`, `.cursor/rules`, `AGENTS.md`) for a recorded kerno preference covering **`effort`**, **`box_testing_strategy`** and **`tags`**.

- Preference recorded → use it and say so.
- Nothing recorded → **ask the user** rather than silently taking defaults. Defaults are `effort: high`, `box_testing_strategy: white_box`, `tags: ["validation"]`.

Kerno stores no preferences. After launch, read **`resolved_intent`** in the response — if it lists anything under `defaulted` and the user has a standing preference, offer to save it to their own rules file. See **`kerno_guide`** (`topic="rules_template"`).

## Step 4: kerno_endpoint_test

Call with `workspace_path`, `app`, `endpoint_method`, `endpoint_path`, `type`, plus any of `effort`, `box_testing_strategy`, `tags`, `test_generation_context`, `scenario_ids`, `interactive`. Returns **`job_id`**, **`log_path`**, **`kind`**: `endpoint_test`, and **`resolved_intent`**.

For security coverage, pass `tags: ["validation","security"]` — **`security`** on its own replaces functional coverage rather than adding to it.

## Step 5: kerno_job and feedback gates

Poll with sparse **`wait=false`** or read **`log_path`** — load `skills/kerno-background-job/SKILL.md`. Don't tight-loop.

A **generate** run always parks on a plan-approval gate while **`kerno_job`** still shows `running` — the gate is not visible there. An **update** run does the same when `interactive: true`. When the job stays `running`:

1. **Detect** — **`kerno_feedback_pending`**, or **`kerno_get_state`** on the endpoint-test resource with **`until_status: ["awaiting_approval","awaiting_answer","ready","failed"]`**.
2. **Answer** — plan approval → `{"approved": true}` (or `{"approved": false, "reason": "..."}` to replan); free-text question → `{"answer": "..."}`. Submit with **`kerno_feedback_answer`**.
3. **Re-poll** — a run can hit several gates in sequence; re-check after each answer.

Full detail and the resource-scoped path (**`answer_feedback_request`**): **`state-and-jobs.md`** § Feedback. Blocked scenarios and generate-vs-validate: **`endpoint-test-types.md`**.

## User-facing messaging

Describe progress in plain language (planning coverage, running scenarios, pass/fail). Avoid MCP wiring jargon unless the user is debugging integration.

Report verdicts honestly — they are not all pass/fail:

- **`blocked`** — did not run, usually missing DB access. Neither pass nor fail; say so rather than implying coverage.
- **`not_implemented`** — Kerno could not write a working scenario. Do not count it as a pass.
- A **potential bug** on a *passing* scenario means Kerno documented real behaviour the plan did not expect. Surface it to the user; if they confirm it's intended, call **`kerno_ignore_potential_bug`** with the reported `fingerprint`.
