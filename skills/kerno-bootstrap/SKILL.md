---
name: kerno-bootstrap
description: This skill should be used when the user asks to bootstrap Kerno MCP, verify connectivity, or runs /kerno-bootstrap. Guides healthcheck, get_applications, and optional endpoint discovery. For environment bring-up use kerno-environment-setup.
version: 0.3.0
---

# Kerno MCP bootstrap

Bootstrap Kerno MCP connectivity for the Kerno agent. Match connected tools to **`kerno_*`** names (clients may prefix them).

**References:**

- `references/unified-flow.md` — canonical tool order and anti-patterns
- `references/mcp-client-config.md` — URL and timeouts

## Preconditions

1. Agent running with MCP enabled; client can list tools.
2. **workspace_path** — absolute path matching the agent **`WORKSPACE`**.

## Step 1: kerno_healthcheck

Call with `workspace_path` if required. Waits **120 seconds** intentionally. On failure, stop (Docker, git, auth).

## Step 2: kerno_get_applications

Parse supported apps; choose **`app`**. Note **`workspace_id`** and per-app config summary.

## Step 3 (optional): kerno_list_endpoints

Only if route discovery is needed **before** environment setup — requires **`scope`**. Normally runs **after** **`ready_for_endpoint_test`** — see **`unified-flow.md`**.

## Next steps

Load `skills/kerno-environment-setup/SKILL.md` for environment bring-up, or `skills/kerno-endpoint-test/SKILL.md` when the environment is already ready.
