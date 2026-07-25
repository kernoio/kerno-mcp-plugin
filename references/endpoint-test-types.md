# Endpoint test types (`kerno_endpoint_test`)

**`kerno_endpoint_test`** runs an async job for **one endpoint**. Requires **`ready_for_endpoint_test`** from **`kerno_environment_status`**. Complete with **`kerno_job`** (`kind`: `endpoint_test`).

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workspace_path` | yes | Absolute workspace root |
| `app` | yes | Module id from **`kerno_get_applications`** |
| `endpoint_method` | yes | e.g. `GET` |
| `endpoint_path` | yes | e.g. `/api/users` |
| `type` | yes | `generate`, `validate`, or `update` |
| `effort` | no | `low`, `medium`, or **`high`** (default) |
| `box_testing_strategy` | no | `black_box` or **`white_box`** (default) |
| `tags` | no | `validation` (default) and/or `security` |
| `test_generation_context` | no | Free-text guidance for this endpoint |
| `scenario_ids` | no | Target specific scenarios only |
| `interactive` | no | Boolean, default `false` |

## type: generate vs validate vs update

| `type` | When to use |
|--------|-------------|
| **`generate`** | No scenarios yet, or you want to restart coverage for the endpoint (GOAP: analyze → plan → reviewPlan → implement → run). **Always** pauses for plan approval. |
| **`validate`** | Scenarios exist on disk; run them against the live SUT only. No planning, no implementation. |
| **`update`** | Endpoint changed intentionally and scenarios should follow. Loads prior run diffs and impacted files, defaults every scenario to keep, makes surgical edits. Pauses for plan approval **only** if `interactive: true`. |

**`validate`** and **`update`** both terminate immediately with **`needs_generate`** when no scenarios exist on disk.

Use **`kerno_list_endpoints`** with matching **`scope`** to inspect **`existingTests`** per route before choosing:

- Empty **`existingTests`** → **`generate`**
- Scenarios on disk → **`validate`** first after code changes, then **`update`** if the change was intentional

## effort

| Value | Behavior |
|-------|----------|
| **`low`** | Writes the scenario and proves it passes once |
| **`medium`** | Additionally runs the scenario a second consecutive time to prove it is repeatable |
| **`high`** (default) | Everything `medium` does, plus an iterative implement-critique-repair loop before accepting the scenario |

A second-run failure is a real finding, not noise: either the scenario's own arrange/cleanUp is not isolated, or fresh random data hit an edge case the first sample missed.

Note: **`type=validate`** runs existing scenarios rather than implementing them, so it performs a single run regardless of `effort`.

## box_testing_strategy

| Value | Behavior |
|-------|----------|
| **`white_box`** (default) | Scenarios may read and write configured datastores directly when the API cannot establish or verify state |
| **`black_box`** | Scenarios exercise the HTTP API only — no direct store access, no source-derived schema in the planning prompt |

Boundaries worth knowing:

- **Preconditions are not governed by this dial.** A precondition may use direct datastore access even under `black_box`.
- Dependency env vars still reach the sandbox under `black_box`, because preconditions may need them.
- `black_box` does not hide SUT source from the planner or implementer.

"Greybox" is **not** a value of this parameter. It is informal wording for having wired DB env blocks into **`kerno_save_config`** — see [target-environment.md](target-environment.md). Configuring DB access enables white box; `box_testing_strategy: black_box` opts an individual run out of it.

## tags

| `tags` | Happy path | Functional coverage | Security scenarios |
|--------|-----------|---------------------|--------------------|
| omitted or `["validation"]` | yes | yes | no |
| `["security"]` | yes | **no** | yes |
| `["validation","security"]` | yes | yes | yes |

**`security` alone narrows the run** — it replaces the functional coverage matrix rather than adding to it. Pass both tags when the user wants functional coverage plus security scenarios.

With `security`, the planner assesses which OWASP API/Web Top-10 categories plausibly apply to the endpoint and authors scenarios for the applicable ones. Security scenarios ship in the same set with the same verdicts — there is no separate findings artifact.

The happy path is always planned, whatever tags are passed.

## test_generation_context

Meaning depends on `type`:

- **`generate`** — complete guidance for planning. A **different** value than last time discards on-disk scenarios and re-plans from scratch, so resend prior guidance in full when adding to it.
- **`update`** — change intent: what changed and how tests should adapt. Does **not** wipe existing scenarios.
- **`validate`** — ignored.

Durable rules belong in `.kerno/config.yaml` under `test-generation` — see [workspace-config.md](workspace-config.md). Config rules and this per-call argument are merged, with the per-call value taking precedence on conflict. Only the per-call value triggers a re-plan; editing config does not.

## resolved_intent and saving preferences

The launch response echoes **`resolved_intent`** with the `effort`, `box_testing_strategy` and `tags` actually used, plus a `defaulted` list naming which ones the caller omitted.

**Kerno stores no testing preferences.** Before the first `kerno_endpoint_test` call for an endpoint, check the caller's **own** rules files (`CLAUDE.md`, `.cursor/rules`, `AGENTS.md`) for a recorded preference. If none is recorded, ask the user rather than silently accepting defaults, and offer to save the answer to those same files.

Call **`kerno_guide`** with `topic="endpoint_test_intent"` for the full protocol, or `topic="rules_template"` for a ready-to-paste preference table.

## After code changes

1. **`kerno_endpoint_test`** with **`type=validate`**
2. If failures are a real bug → fix product code, validate again
3. If the endpoint changed intentionally → **`type=update`** with `test_generation_context` describing the change
4. **Never** hand-edit `.kerno/scenarios/**/*.scenario.ts` to chase handler or API changes

## Scope grammar (for list_endpoints prefetch)

Same as endpoint discovery: **`all`**, **`changed`**, **`file:<path>`**, **`endpoint:METHOD /path`**.

**`kerno_list_endpoints`** requires **`scope`** — use **`all`** to list every route for the app selection. **`kerno_endpoint_test`** takes no scope; it targets one endpoint by explicit method and path.

## Feedback gates

A **`type=generate`** run always pauses for plan review. A **`type=update`** run pauses only with `interactive: true`. Either can pause for:

- **`awaiting_approval`** — plan review (GOAP `reviewPlan`)
- **`awaiting_answer`** — free-text planner question, or a request for a DB schema path

These are **gate statuses**, not job failures. **`kerno_job`** shows job progress but **not** feedback gates — a gated job may look stuck there.

When stalled:

1. **`kerno_feedback_pending`** (workspace + app), **or**
2. **`kerno_get_state`** on endpoint-test resource id `workspace/<ws>/app/<app>/endpoint/<METHOD>/<path>/endpointtest`

Answer with **`kerno_feedback_answer`** or **`answer_feedback_request`**, then the run resumes.

Rejection on plan review triggers replan (GOAP replan loop).

See [state-and-jobs.md](state-and-jobs.md) and **`skills/kerno-endpoint-test/SKILL.md`**.

## Scenario verdicts

| Verdict | Meaning |
|---------|---------|
| **`passed`** | Ran and behaved as expected |
| **`failed`** | Ran and the endpoint did something the scenario did not expect |
| **`blocked`** | Did **not** run — neither pass nor fail |
| **`not_implemented`** | Kerno could not produce a working scenario for this case |

A **passing** scenario may carry a **potential bug**: Kerno found behaviour the plan did not expect, confirmed it against source, and documented the real behaviour. If the user confirms it is known or intended, call **`kerno_ignore_potential_bug`** with the `fingerprint` exactly as reported. There is no un-ignore path.

## Blocked scenarios (DB access)

A scenario that needs the database is reported **`[BLOCKED]`** in a **black box** (HTTP-only) run — or in a white-box run where Kerno can't derive the DB schema. **Blocked is not failed:** the scenario didn't run, so it's neither pass nor fail. To unblock, provide DB access — see [workspace-config.md](workspace-config.md#database-access-requires-a-derivable-schema). If DB access isn't possible, tell the user those scenarios can't run and only API-level validation is covered.
