# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **Kerno MCP** tools. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

## Where to start

1. **Install this plugin** (Claude Code or Cursor) — see [Install](#install--claude-code) below.
2. **Run `/install-kerno`** in your IDE. The skill walks through CLI install, login, binding the agent to your workspace, and registering MCP with your editor.
3. **Open your assistant in the same workspace** you bound with `kerno mcp -w <path>`. Kerno MCP tools only work when the session matches that folder.

After MCP is connected, use `/kerno-bootstrap` or other skills for environment setup, endpoints, and validation.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)

## Layout (one repo, two manifests)

| Client | Manifest | Discovery |
|--------|----------|-----------|
| Claude Code | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | `commands/`, `skills/`, `references/` |
| Cursor | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) | `rules/`, `skills/`, `commands/`, root [`mcp.json`](mcp.json) |

Shared content: `skills/`, `commands/`, `references/`.

## Prerequisites

- Node.js ≥ 18, `npm`, Docker, and a git repository for the target project.
- **`@kerno/cli`** installed and logged in (`kerno login`).
- Agent running for your workspace: `kerno mcp -w /absolute/path/to/repo` — read the MCP URL from CLI output (port is not fixed).
- MCP registered in your editor — `/install-kerno` handles this step by step.

For self-hosted or dev agent setups, see [references/mcp-client-config.md](references/mcp-client-config.md) and aicore `agent/apps/agent/docs/mcp.md`.

## Install — Claude Code

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

## Install — Cursor

Symlink or copy this directory into Cursor’s local plugins folder, then reload the window:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno-mcp
```

See [cursor/README.md](cursor/README.md) for details and [Cursor marketplace publish](https://cursor.com/marketplace/publish) when ready.

## Commands

| Command | Purpose |
|---------|---------|
| `/install-kerno` | First-time setup: CLI, agent, MCP registration, verification, next steps |
| `/kerno-bootstrap` | Run the recommended Kerno MCP workflow (healthcheck → get_applications → environment → job) |
| `/kerno-mcp-capture-baseline` | Point the agent at **`kerno_capture_baseline`** (scopes, async job, prerequisites) |
| `/kerno-mcp-help` | Pointers to MCP setup, job semantics, and references |

## Skills

- **install-kerno** — Step-by-step install and MCP connection for a workspace ([GitBook guide](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)).
- **kerno-mcp-bootstrap** — Full bootstrap procedure aligned with `mcp.md`.
- **kerno-mcp-background-job** — How to use `kerno_start_environment` + `kerno_job` (wait, timeouts, logs).
- **kerno-mcp-validate** — Run **`kerno_validate`** after code changes; do not patch **`.kerno/scenarios/`** before validate / **`kerno_capture_baseline`**.
- **kerno-mcp-capture-baseline** — When and how to use **`kerno_capture_baseline`** (plan+implement+run scenarios).

## Rules (Cursor)

- [rules/kerno-mcp.mdc](rules/kerno-mcp.mdc) — Tool ordering and async-job constraints (`alwaysApply: true`).

Canonical operator details (ports, env, workspace invariant) remain in **`agent/apps/agent/docs/mcp.md`** in the main repo.

## References

- **[references/mcp-client-config.md](references/mcp-client-config.md)** — CLI install, host registration, operator env, timeouts (single connection reference).
- **[references/tool-ordering.md](references/tool-ordering.md)** — Recommended tool order including optional scenario capture.
- **[references/capture-baseline.md](references/capture-baseline.md)** — `kerno_capture_baseline` parameters, scopes, and job response fields.
- **[references/changes-detected.md](references/changes-detected.md)** — Optional `.kerno/CHANGES_DETECTED.md` marker + hook pattern to trigger `kerno_validate`.
