# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **unified Kerno MCP** tool surface. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

**Source:** [github.com/kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

## Give this repo to your coding tool

**Claude Code, Cursor, and Codex** all install Kerno from the Kerno marketplace: add `kernoio/kerno-mcp-plugin` as a marketplace, install the **kerno** plugin, then run **install-kerno**. Jump to your tool below, or paste a [one-shot prompt](#paste-a-prompt-into-your-assistant) for Claude Code or Codex.

### Paste a prompt into your assistant

Paste **one** prompt below into **Claude Code or Codex**. It installs the Kerno plugin from the marketplace, then runs **install-kerno** to install the CLI, start the agent, and connect MCP for your workspace. Cursor installs from its Plugins dashboard, see [Cursor](#cursor) below.

| Tool | Copy-paste prompt |
|------|-------------------|
| Claude Code | [prompts/install-claude.md](prompts/install-claude.md) |
| Codex | [prompts/install-codex.md](prompts/install-codex.md) |

### Claude Code

Install from the Kerno marketplace, then run the setup skill:

```
/plugin marketplace add kernoio/kerno-mcp-plugin
/plugin install kerno@kerno
/install-kerno
```

`/install-kerno` installs `@kerno/cli`, logs in, starts the agent with `kerno init -w`, and registers MCP.

**Or paste a prompt** (agent-driven — it clones and loads the plugin for you):

```
Install and set up the Kerno MCP plugin from https://github.com/kernoio/kerno-mcp-plugin for this workspace.

1. Install from the Kerno marketplace: run `claude plugin marketplace add kernoio/kerno-mcp-plugin` then `claude plugin install kerno@kerno` (see claude/README.md), then restart Claude Code so the plugin loads.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Cursor

Install from the Kerno marketplace, then run the setup skill:

1. Open Cursor **Settings → Plugins** (or [cursor.com/dashboard](https://cursor.com/dashboard) → Plugins).
2. **Add marketplace → Import from repo**, and enter `kernoio/kerno-mcp-plugin`.
3. Install **kerno**, reload the window (**Developer: Reload Window**), then run **`/install-kerno`**.

`/install-kerno` installs `@kerno/cli`, logs in, binds the agent to this workspace with `kerno init -w`, and registers MCP with the URL from CLI output.

### Codex

```
Set up Kerno for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

1. Install from the Kerno marketplace: run `codex plugin marketplace add kernoio/kerno-mcp-plugin`, then open /plugins and install kerno (see codex/README.md).
2. Run the install-kerno skill (@install-kerno) to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP in Codex.
3. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```

## Where to start

1. **Install the plugin** — use a [prompt](#paste-a-prompt-into-your-assistant) or a client install guide ([Claude](claude/README.md) · [Cursor](cursor/README.md) · [Codex](codex/README.md)).
2. **First thing after the plugin is installed:** run **install-kerno** (`/install-kerno` or `@install-kerno`).
3. **Open your assistant in the same workspace** you bound with `kerno init -w <path>`.

After MCP is connected, use `/kerno-bootstrap` to verify connectivity, then `/kerno-env` for environment setup or `/kerno-endpoint-test` for endpoint tests.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)

## Unified MCP flow (summary)

```
healthcheck → get_applications → [local: start repo dev flow] → save_config
  → environment_setup → environment_status (until ready_for_endpoint_test)
  → list_endpoints → endpoint_test → job
```

Prefer **greybox** (local + DB access, so DB-backed scenarios run); fall back to **black box** (HTTP-only) when DB access isn't possible, telling the user that scenarios requiring direct DB access will be reported **`[BLOCKED]`**. Full checklist: [references/unified-flow.md](references/unified-flow.md).

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
- Agent running for your workspace: `kerno init -w /absolute/path/to/repo` — read the MCP URL from CLI output (port is not fixed).
- MCP registered in your editor — **install-kerno** handles this step by step.

For self-hosted or dev agent setups, see [references/mcp-client-config.md](references/mcp-client-config.md).

## Plugin contents

**Slash commands** (`/install-kerno`, `/kerno-bootstrap`, `/kerno-env`, `/kerno-endpoint-test`, `/kerno-help`) delegate to matching skills under `skills/`. **Cursor rules:** [rules/kerno.mdc](rules/kerno.mdc). **Canonical MCP workflow:** [references/unified-flow.md](references/unified-flow.md). Other references: [workspace-config](references/workspace-config.md), [target-environment](references/target-environment.md), [endpoint-test-types](references/endpoint-test-types.md), [state-and-jobs](references/state-and-jobs.md), [mcp-client-config](references/mcp-client-config.md), [changes-detected](references/changes-detected.md). Operator details: `agent/apps/agent/docs/mcp.md` in the main repo.

## Drift prevention

Run **`scripts/check-unified-drift.py`** locally or in CI to ensure plugin docs match the unified tool surface.
