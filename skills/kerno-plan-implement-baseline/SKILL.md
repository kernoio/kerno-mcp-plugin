---
name: kerno-plan-implement-baseline
description: This skill should be used when the user wants to author or refresh Kerno HTTP scenario tests via MCP (kerno_plan_baseline and kerno_implement_baseline), or asks about scopes, plan_review_instructions, workspace_id, or async completion. Planning does not require a running stack; implement requires ready_for_validation.
version: 0.1.0
---

# Kerno MCP — plan and implement scenario baselines

## When to use this skill

Use **`kerno_plan_baseline`** and **`kerno_implement_baseline`** when the goal is to **create or update `.scenario.ts` files** and **confirm they pass** end-to-end.

Typical situations:

- Scenarios are **missing** for routes (check **`existingTests`** via **`kerno_list_endpoints`** with the same **`scope`**).
- **`kerno_validate`** failed and scenarios need Kerno-driven regeneration — do **not** hand-edit **`.kerno/scenarios/`**.
- The user wants a **batch** pass (`scope: all`) or a **single route** (`scope: endpoint:…` or sync **`method`** + **`path`**).

**Do not** use this skill as the primary guide for:

- **`kerno_validate`** alone — use **`skills/kerno-validate/SKILL.md`**. Run validate **before** deciding scenarios need regeneration when the API changed.

## Prerequisites

1. **`kerno_healthcheck`** and **`kerno_get_applications`** (note **`workspace_id`** if you will pass it).
2. Optional **`kerno_list_endpoints`** with the **same `scope`** you will use for plan/implement — requires **`scope`** (e.g. `all`).
3. **`kerno_implement_baseline`** only: stack up with **`ready_for_validation: true`** (via **`kerno_compose_up`** or **`kerno_start_environment`** + **`kerno_job`**). Planning (**`kerno_plan_baseline`**) does **not** require a running environment.

Use the **same** **`workspace_path`** and **`app`** conventions as compose and start-environment tools.

## Stage 1 — Plan (`kerno_plan_baseline`)

**Async (many endpoints):** call with **`scope`** (not **`changed`**). Optional **`plan_review_instructions`**. Returns **`job_id`**, **`log_path`**, **`kind`**: `plan_baseline`. Complete with **`kerno_job`**.

**Sync (one endpoint in the MCP loop):** omit **`scope`**; pass **`method`** and **`path`** together. Optional **`plan_review_instructions`** on each round. Response has **`plan_sync`** — no **`kerno_job`** for that call.

Present the plan to the user (scenario names, coverage, open decisions). Refine with another sync call or async job + **`plan_review_instructions`** before implement.

## Stage 2 — Implement (`kerno_implement_baseline`)

Only after planning for every endpoint in scope and **`ready_for_validation`** is true:

1. Call **`kerno_implement_baseline`** with **`scope`** (and optional **`app`**, **`workspace_id`**).
2. Complete with **`kerno_job`** (**`kind`**: `implement_baseline`).

Long-running LLM work — use sparse **`wait=false`** polling or **`log_path`**. See **`skills/kerno-background-job/SKILL.md`**.

## Scopes

| Scope                   | Plan (async)                  | Implement |
| ----------------------- | ----------------------------- | --------- |
| `all`                   | yes                           | yes       |
| `file:<path>`           | yes                           | yes       |
| `endpoint:METHOD /path` | yes                           | yes       |
| `changed`               | no — use **`kerno_validate`** | no        |

Parameter details and terminal JSON: **`${CLAUDE_PLUGIN_ROOT}/references/plan-implement-baseline.md`**.

## Deduping

**`plan_baseline`** and **`implement_baseline`** share one slot per workspace **+** scope **+** app selection. Do not launch a second job in that family while one is running.

## See also

- **`${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`** — full tool order.
- **`${CLAUDE_PLUGIN_ROOT}/skills/kerno-validate/SKILL.md`** — validate before regenerating when the API changed.
- **`${CLAUDE_PLUGIN_ROOT}/references/compose-plan.md`** — environment setup before implement.
