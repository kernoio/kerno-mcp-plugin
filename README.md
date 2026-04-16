# Kerno MCP (Claude Code + Cursor plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **Kerno MCP** tools exposed by **aicore-agent** (`POST /mcp`). The JVM agent is **not** included here—run the agent separately.

## Layout (one repo, two manifests)

| Client | Manifest | Discovery |
|--------|----------|-----------|
| Claude Code | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | `commands/`, `skills/`, `references/` |
| Cursor | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) | `rules/`, `skills/`, `commands/`, root [`mcp.json`](mcp.json) |

Shared content: `skills/`, `commands/`, `references/`.

## Prerequisites

- Running aicore-agent with MCP enabled (`ENABLE_MCP`), valid `WORKSPACE`, and reachable HTTP URL (see [agent/apps/agent/docs/mcp.md](../agent/apps/agent/docs/mcp.md)).
- Edit root [`mcp.json`](mcp.json) (or your project MCP settings) so the URL matches your `PORT` or `MCP_PORT`.

## Install — Claude Code

```bash
claude --plugin-dir /path/to/aicore/kerno-claude-plugin
```

## Install — Cursor

Symlink or copy this directory into Cursor’s local plugins folder, then reload the window:

```bash
ln -s /path/to/aicore/kerno-claude-plugin ~/.cursor/plugins/local/kerno-mcp
```

See [cursor/README.md](cursor/README.md) for details and [Cursor marketplace publish](https://cursor.com/marketplace/publish) when ready.

## Commands

| Command | Purpose |
|---------|---------|
| `/kerno-bootstrap` | Run the recommended Kerno MCP workflow (healthcheck → get_applications → environment → job) |
| `/kerno-mcp-capture-baseline` | Point the agent at **`kerno_capture_baseline`** (scopes, async job, prerequisites) |
| `/kerno-mcp-help` | Pointers to MCP setup, job semantics, and references |

## Skills

- **kerno-mcp-bootstrap** — Full bootstrap procedure aligned with `mcp.md`.
- **kerno-mcp-background-job** — How to use `kerno_start_environment` + `kerno_job` (wait, timeouts, logs).
- **kerno-mcp-validate** — Run **`kerno_validate`** after code changes; do not patch **`.kerno/scenarios/`** before validate / **`kerno_capture_baseline`**.
- **kerno-mcp-capture-baseline** — When and how to use **`kerno_capture_baseline`** (plan+implement+run scenarios).

## Rules (Cursor)

- [rules/kerno-mcp.mdc](rules/kerno-mcp.mdc) — Tool ordering and async-job constraints (`alwaysApply: true`).

Canonical operator details (ports, env, workspace invariant) remain in **`agent/apps/agent/docs/mcp.md`** in the main repo.

## References

- **[references/tool-ordering.md](references/tool-ordering.md)** — Recommended tool order including optional scenario capture.
- **[references/capture-baseline.md](references/capture-baseline.md)** — `kerno_capture_baseline` parameters, scopes, and job response fields.
- **[references/changes-detected.md](references/changes-detected.md)** — Optional `.kerno/CHANGES_DETECTED.md` marker + hook pattern to trigger `kerno_validate`.
- **[references/sentry-insights-mcp.md](references/sentry-insights-mcp.md)** — How Sentry’s MCP **Resources** table relates (and does not relate) to **`kerno_*` tools**.
