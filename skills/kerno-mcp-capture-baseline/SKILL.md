---
name: kerno-mcp-capture-baseline
description: This skill should be used when the user wants to author or refresh TypeScript HTTP scenario tests via MCP (kerno_capture_baseline), or asks about scopes, workspace_id, or async completion. The tool runs plan, implement, then a full scenario run against the stack.
version: 0.1.0
---

# Kerno MCP — capture baselines via scenarios (`kerno_capture_baseline`)

## When to use this skill

Use **`kerno_capture_baseline`** when the goal is to **create or update `.scenario.ts` files** and **confirm they pass** end-to-end (same **plan → implement → run** behavior as REST `/scenarios/plan`, `/scenarios/implement`, and a full run per endpoint).

Typical situations:

- After the repo’s HTTP app **environment is up** (`kerno_start_environment` completed **healthy** via `kerno_job`), you want **Kerno-authored tests** for some or all routes.
- You want a **batch** pass over **all endpoints** in one or all HTTP modules (`scope: all`).
- You want to target **one handler file** or **one route** (`scope: file:…` or `endpoint:…`).

**Do not** use this skill as the primary guide for:

- **`kerno_validate`** alone (run tests against the live stack without authoring) — use **`skills/kerno-mcp-validate/SKILL.md`**; run validate **before** deciding scenarios need regeneration when the API changed. Do not hand-edit **`.kerno/scenarios/`** instead of calling **`kerno_capture_baseline`** after validate shows failures.

## Prerequisites

1. **`kerno_healthcheck`** and **`kerno_get_applications`** (workspace analyzed; note **`workspace_id`** if you will pass it).
2. Optional **`kerno_list_endpoints`** to choose `app`, paths, and handler file paths.
3. **`kerno_start_environment`** for the relevant **`app`**, then **`kerno_job`** until **healthy** (or your policy allows generating against a stack that is already up).

Use the **same** **`workspace_path`** and **`app`** conventions as **`kerno_start_environment`** (REST `workspaceId` / `applicationId` alignment). Optional **`workspace_id`** must match **`kerno_get_applications`** when provided.

## Launch and complete

1. Call **`kerno_capture_baseline`** with **`scope`** (and optional **`app`**, **`user_message`**, **`workspace_id`**). It returns immediately with **`job_id`**, **`log_path`**, **`kind`: `capture_baseline`**.
2. Complete with **`kerno_job`** the same way as environment builds: **sparse** polling (`wait=false` every few minutes) or read **`log_path`**. Do not spam **`kerno_job`** in a tight loop.

Long-running **LLM** work means wall-clock time can be **large**; the MCP host **~60s** per call limit still applies. See `${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-background-job/SKILL.md` for wait semantics.

## Scopes (summary)

| Scope | Meaning |
|--------|---------|
| `all` | Every analyzed HTTP endpoint; optional **`app`** limits to one module; omit **`app`** for all HTTP apps. |
| `file:<path>` | Workspace-relative **handler source file** path as shown under **`kerno_list_endpoints`** (not a `.scenario.ts` path). |
| `endpoint:METHOD /path` | Single route; if it exists in multiple modules, pass **`app`**. |

`changed` is **not** supported — use **`kerno_validate`** for that.

Parameter details and terminal JSON fields: `${CLAUDE_PLUGIN_ROOT}/references/capture-baseline.md`.

## Deduping

Only one **`capture_baseline`** job may run at a time per workspace **+** normalized scope **+** app selection. A second launch fails until the first finishes.

## See also

- **`${CLAUDE_PLUGIN_ROOT}/references/tool-ordering.md`** — full tool order next to **`kerno_validate`**.
- **`${CLAUDE_PLUGIN_ROOT}/skills/kerno-mcp-validate/SKILL.md`** — run validate before regenerating scenarios when the API changed.
