# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **unified Kerno MCP** tool surface. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

**Source:** [github.com/kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

## Install

Two steps: install the **kerno** plugin in your tool, then run **`/install-kerno`**.

### 1. Install the plugin

**Claude Code**
```
/plugin marketplace add kernoio/kerno-mcp-plugin
/plugin install kerno@kerno
```

**Cursor**: Settings → Plugins → **Add marketplace → Import from repo**, enter `kernoio/kerno-mcp-plugin`, install **kerno**, then reload the window (**Developer: Reload Window**).

**Codex**
```
codex plugin marketplace add kernoio/kerno-mcp-plugin
```
Then open **`/plugins`**, install **kerno**, and start a new session.

Per-tool details: [Claude](claude/README.md) · [Cursor](cursor/README.md) · [Codex](codex/README.md).

### 2. Run install-kerno

Run **`/install-kerno`** (**`@install-kerno`** in Codex). It loads the install-kerno skill, and the agent does the rest: installs `@kerno/cli`, logs you in, starts the local agent bound to this workspace (`kerno init -w`), registers MCP, and verifies the connection. It pauses to ask you a few things (browser login, which host, MCP scope).

Or hand both steps to the agent: paste [prompts/install-claude.md](prompts/install-claude.md) (or [prompts/install-codex.md](prompts/install-codex.md) for Codex).

Prerequisites: Node.js ≥ 18, npm, Docker running, a git repository, and a Kerno account. For self-hosted or dev agent setups, see [references/mcp-client-config.md](references/mcp-client-config.md).

## After install

Open your assistant in the **same workspace** you bound with `kerno init -w <path>`. Then use `/kerno-bootstrap` to verify connectivity, `/kerno-env` for environment setup, or `/kerno-endpoint-test` for endpoint tests.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)

## Unified MCP flow (summary)

```
healthcheck → get_applications → [local: start repo dev flow] → save_config
  → environment_setup → environment_status (until ready_for_endpoint_test)
  → list_endpoints → endpoint_test → job
```

Prefer **greybox** (local + DB access, so DB-backed scenarios run); fall back to **black box** (HTTP-only) when DB access isn't possible, telling the user that scenarios requiring direct DB access will be reported **`[BLOCKED]`**. Full checklist: [references/unified-flow.md](references/unified-flow.md).

## Layout (one repo, three clients)

| Client | Install guide | Plugin manifest |
|--------|---------------|-----------------|
| Claude Code | [claude/README.md](claude/README.md) | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) |
| Cursor | [cursor/README.md](cursor/README.md) | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) |
| Codex | [codex/README.md](codex/README.md) | [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) |

Shared content: `skills/`, `commands/`, `references/`, [prompts/](prompts/).

## Plugin contents

**Slash commands** (`/install-kerno`, `/kerno-bootstrap`, `/kerno-env`, `/kerno-endpoint-test`, `/kerno-help`) delegate to matching skills under `skills/`. **Cursor rules:** [rules/kerno.mdc](rules/kerno.mdc). **Canonical MCP workflow:** [references/unified-flow.md](references/unified-flow.md). Other references: [workspace-config](references/workspace-config.md), [target-environment](references/target-environment.md), [endpoint-test-types](references/endpoint-test-types.md), [state-and-jobs](references/state-and-jobs.md), [mcp-client-config](references/mcp-client-config.md), [changes-detected](references/changes-detected.md). Operator details: `agent/apps/agent/docs/mcp.md` in the main repo.

## Drift prevention

Run **`scripts/check-unified-drift.py`** locally or in CI to ensure plugin docs match the unified tool surface.
