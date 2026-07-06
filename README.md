# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **unified Kerno MCP** tool surface. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

**Source:** [github.com/kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

## Give this repo to your coding tool

Clone [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) and install the **full plugin** (skills, commands, references, and Cursor rules) using a [paste prompt](#paste-a-prompt-into-your-assistant) or a [client install guide](#layout-one-repo-three-manifests) below. Public marketplace install is **not** available yet.

### Paste a prompt into your assistant

Paste **one** prompt below into your assistant (Agent chat, Claude Code, Codex, etc.). It clones the repo, loads the full plugin, then runs **install-kerno** to install the CLI, start the agent, and connect MCP for your workspace.

| Tool | Copy-paste prompt |
|------|-------------------|
| Claude Code | [prompts/install-claude.md](prompts/install-claude.md) |
| Cursor | [prompts/install-cursor.md](prompts/install-cursor.md) |
| Codex | [prompts/install-codex.md](prompts/install-codex.md) |

### Claude Code

```
Install and set up the Kerno MCP plugin from https://github.com/kernoio/kerno-mcp-plugin for this workspace.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Clone https://github.com/kernoio/kerno-mcp-plugin to ~/.kerno/mcp-plugin and load it as a Claude Code plugin with `claude --plugin-dir ~/.kerno/mcp-plugin` (see claude/README.md). Do not use `/plugin marketplace`.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Cursor

**Open in Cursor:** use the link under the prompt block, or copy the text below.

```
Install and set up Kerno MCP for this project using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Follow cursor/README.md: clone https://github.com/kernoio/kerno-mcp-plugin to ~/.kerno/mcp-plugin and symlink into ~/.cursor/plugins/local/kerno, then reload Cursor.
2. Run /install-kerno to install @kerno/cli, bind the agent to this workspace with kerno mcp -w, and register MCP with the URL from CLI output.
3. Confirm Kerno MCP tools are available in this project folder.

Work in this repository root unless I specify another path.
```

**Open in Cursor:** [Open in Cursor](https://cursor.com/link/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0ADo%20not%20use%20any%20plugin%20marketplace%20%E2%80%94%20Kerno%20is%20not%20published%20to%20marketplaces%20yet.%0A%0A1.%20Follow%20cursor%2FREADME.md%3A%20clone%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin%20to%20~%2F.kerno%2Fmcp-plugin%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno%2C%20then%20reload%20Cursor.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) · [cursor://](cursor://anysphere.cursor-deeplink/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0ADo%20not%20use%20any%20plugin%20marketplace%20%E2%80%94%20Kerno%20is%20not%20published%20to%20marketplaces%20yet.%0A%0A1.%20Follow%20cursor%2FREADME.md%3A%20clone%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin%20to%20~%2F.kerno%2Fmcp-plugin%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno%2C%20then%20reload%20Cursor.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) — opens the IDE with the install prompt above pre-filled (review and send; does not run automatically). [Link details](references/cursor-install-deeplink.md).


### Codex

```
Set up Kerno for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Clone https://github.com/kernoio/kerno-mcp-plugin to ~/.kerno/mcp-plugin and register it as a local Codex plugin (see codex/README.md). Do not use `codex plugin marketplace add`.
2. Run the install-kerno skill (@install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP in Codex.
3. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```

## Where to start

1. **Install the plugin** — use a [prompt](#paste-a-prompt-into-your-assistant) or a client install guide ([Claude](claude/README.md) · [Cursor](cursor/README.md) · [Codex](codex/README.md)).
2. **First thing after the plugin is installed:** run **install-kerno** (`/install-kerno` or `@install-kerno`).
3. **Open your assistant in the same workspace** you bound with `kerno mcp -w <path>`.

After MCP is connected, use `/kerno-bootstrap` to verify connectivity, then `/kerno-env` for environment setup or `/kerno-endpoint-test` for endpoint tests.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)

## Unified MCP flow (summary)

```
healthcheck → get_applications → [local: start repo dev flow] → save_config
  → environment_setup → environment_status (until ready_for_endpoint_test)
  → list_endpoints → endpoint_test → job
```

Use **`orchestrate`** only when the user asks Kerno to orchestrate **or** the repo has no easy startup (`docker-compose`, dev scripts, etc.). Full checklist: [references/unified-flow.md](references/unified-flow.md).

## Layout (one repo, three manifests)

| Client | Install guide | Manifest |
|--------|---------------|----------|
| Claude Code | [claude/README.md](claude/README.md) | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) |
| Cursor | [cursor/README.md](cursor/README.md) | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) |
| Codex | [codex/README.md](codex/README.md) | [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) |

Shared content: `skills/`, `commands/`, `references/`, [prompts/](prompts/).

## Prerequisites

- Node.js ≥ 18, `npm`, Docker, and a git repository for the target project.
- **`@kerno/cli`** installed and logged in (`kerno login`) — **install-kerno** handles this after you add the plugin.
- Agent running for your workspace: `kerno mcp -w /absolute/path/to/repo` — read the MCP URL from CLI output (port is not fixed).
- MCP registered in your editor — **install-kerno** handles this step by step.

For self-hosted or dev agent setups, see [references/mcp-client-config.md](references/mcp-client-config.md) and aicore `agent/apps/agent/docs/mcp.md`.

## Plugin contents

**Slash commands** (`/install-kerno`, `/kerno-bootstrap`, `/kerno-env`, `/kerno-endpoint-test`, `/kerno-help`) delegate to matching skills under `skills/`. **Cursor rules:** [rules/kerno.mdc](rules/kerno.mdc). **Canonical MCP workflow:** [references/unified-flow.md](references/unified-flow.md). Other references: [workspace-config](references/workspace-config.md), [target-environment](references/target-environment.md), [endpoint-test-types](references/endpoint-test-types.md), [state-and-jobs](references/state-and-jobs.md), [mcp-client-config](references/mcp-client-config.md), [changes-detected](references/changes-detected.md), [cursor-install-deeplink](references/cursor-install-deeplink.md). Operator details: `agent/apps/agent/docs/mcp.md` in the main repo.

## Drift prevention

Run **`scripts/check-unified-drift.py`** locally or in CI to ensure plugin docs match the unified tool surface.
