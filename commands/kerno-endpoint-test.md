---
description: Generate or validate endpoint tests (kerno_endpoint_test workflow)
argument-hint: "[generate|validate] [app] [METHOD /path]"
---

Run the **kerno-endpoint-test** skill from `${CLAUDE_PLUGIN_ROOT}/skills/kerno-endpoint-test/SKILL.md`.

Parse `$ARGUMENTS` if present:

- First token: `generate` or `validate` (default from context — validate after code changes, generate when no scenarios)
- Optional `app`, HTTP method, and path (e.g. `GET /api/users`)

If missing, derive from context or ask once. Confirm **`ready_for_endpoint_test`** before launching.
