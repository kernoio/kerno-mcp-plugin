---
name: kerno-mcp-validate
description: This skill should be used when the user asks to run Kerno HTTP scenario tests, fix failing tests after API changes, or wants validation (kerno_validate) after editing handlers. Prevents hand-editing .kerno scenario files before calling MCP validate and capture_baseline.
version: 0.1.0
---

# Kerno MCP — run scenario validation (`kerno_validate`)

## When to use this skill

Use **`kerno_validate`** when the goal is to **execute** TypeScript HTTP scenarios against the running stack (including baseline checks when baselines exist), not to rewrite scenario source by hand.

Typical situations:

- After **`kerno_start_environment`** is **healthy** (via **`kerno_job`**), you want to know whether existing scenarios still pass.
- The user **changed handlers or API responses** and wants to confirm tests; you should **`kerno_validate`** with **`scope: changed`** or **`endpoint:METHOD /path`** before doing anything else to **`.kerno/scenarios/`**.

## Must not (critical)

- **Do not** open **`.kerno/scenarios/**/*.scenario.ts`** and edit **`baseline`**, assertions, or steps to match a new response shape **before** calling **`kerno_validate`** and reading the job result.
- **Do not** treat “fix the tests” as a reason to patch scenario files manually. Those updates belong to **`kerno_capture_baseline`** (plan → implement → run) after validation shows what is stale or missing.

## Correct flow

1. **`kerno_healthcheck`**, **`kerno_get_applications`** as needed.
2. **`kerno_start_environment`** → **`kerno_job`** until **healthy** (if the stack is not already up).
3. **`kerno_list_endpoints`** with the **same** **`scope`** string you will use for validate (optional but useful for **`existingTests`**).
4. **`kerno_validate`** with **`scope`** (`all`, `changed`, `file:…`, or `endpoint:…`) → **`kerno_job`** until terminal (sparse **`wait=false`** or **`log_path`**; see **`skills/kerno-mcp-background-job/SKILL.md`**).
5. If validation fails and scenarios need regeneration, **`kerno_capture_baseline`** with the **same** **`scope`**, then **`kerno_job`** again — not ad-hoc edits under **`.kerno/scenarios/`**.

## See also

- **`${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`** — full tool order, including **`kerno_validate`**.
- **`${CLAUDE_PLUGIN_ROOT}/references/capture-baseline.md`** — **`kerno_capture_baseline`** when scenarios must be regenerated after validate.
- **`${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md`** — MCP URL, **`WORKSPACE`**, and client setup.
