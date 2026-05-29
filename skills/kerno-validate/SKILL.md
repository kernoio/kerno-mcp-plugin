---
name: kerno-validate
description: This skill should be used when the user asks to run Kerno HTTP scenario tests, fix failing tests after API changes, or wants validation (kerno_validate) after editing handlers. Prevents hand-editing .kerno scenario files before calling MCP validate and plan/implement baseline.
version: 0.1.0
---

# Kerno MCP — run scenario validation (`kerno_validate`)

## When to use this skill

Use **`kerno_validate`** when the goal is to **execute** Kerno HTTP scenarios against the running stack (including baseline checks when baselines exist), not to rewrite scenario source by hand.

Typical situations:

- After the stack has **`ready_for_validation: true`** (via **`kerno_compose_status`**), you want to know whether existing scenarios still pass.
- The user **changed handlers or API responses** and wants to confirm tests; you should **`kerno_validate`** with **`scope: changed`** or **`endpoint:METHOD /path`** before doing anything else to **`.kerno/scenarios/`**.

## Must not (critical)

- **Do not** open **`.kerno/scenarios/**/\*.scenario.ts`** and edit **`baseline`**, assertions, or steps to match a new response shape **before** calling **`kerno_validate`\*\* and reading the job result.
- **Do not** treat “fix the tests” as a reason to patch scenario files manually. Those updates belong to **`kerno_plan_baseline`** then **`kerno_implement_baseline`** after validation shows what is stale or missing.

## Correct flow

1. **`kerno_healthcheck`**, **`kerno_get_applications`** as needed.
2. Bring the stack up — prefer **`kerno_compose_up`** when compose files exist; else compose-plan workflow + **`kerno_start_environment`** → **`kerno_job`**. Confirm **`ready_for_validation`** via **`kerno_compose_status`**.
3. **`kerno_list_endpoints`** with the **same** **`scope`** string you will use for validate (optional but useful for **`existingTests`**). **`scope` is required** on list_endpoints.
4. **`kerno_validate`** with **`scope`** (`all`, `changed`, `file:…`, or `endpoint:…`) → **`kerno_job`** until terminal (sparse **`wait=false`** or **`log_path`**; see **`skills/kerno-background-job/SKILL.md`**).
5. If validation fails and scenarios need regeneration, **`kerno_plan_baseline`** then **`kerno_implement_baseline`** with the **same** **`scope`**, each followed by **`kerno_job`** — not ad-hoc edits under **`.kerno/scenarios/`**.

## See also

- **`${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`** — full tool order, including **`kerno_validate`**.
- **`${CLAUDE_PLUGIN_ROOT}/references/plan-implement-baseline.md`** — plan and implement when scenarios must be regenerated after validate.
- **`${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md`** — MCP URL, **`WORKSPACE`**, and client setup.
