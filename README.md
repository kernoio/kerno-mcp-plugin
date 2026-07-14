# Kerno MCP (Claude Code + Cursor + Codex plugin)

**Kerno** is a runtime QA engine for backend coding agents: it generates and runs integration tests against your real stack, so your agent catches its own regressions before they reach a PR.

This repo is the **plugin** that connects Kerno to your coding tool (Claude Code, Cursor, or Codex): it adds the slash commands and skills that teach the agent how to work with Kerno. The engine itself runs locally via **`@kerno/cli`**; the `/install-kerno` step below sets it up.

## Install

Pick your tool. Two steps each: install the **kerno** plugin, then paste the setup prompt into your agent to configure Kerno for your project.

Prerequisites: Node.js ≥ 18, npm, Docker running, a git repository, and a Kerno account.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart). For self-hosted or dev agent setups, see [references/mcp-client-config.md](references/mcp-client-config.md).

### Claude Code

**1. Install the plugin**
```
/plugin marketplace add kernoio/kerno-mcp-plugin
/plugin install kerno@kerno
```

**2. Paste this into your agent**
```
Set up Kerno for this workspace.

1. Confirm the kerno plugin is installed and its skills are available (e.g. /install-kerno resolves). If not, diagnose what's wrong and help me troubleshoot it before continuing.
2. Run /install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

Details: [claude/README.md](claude/README.md).

### Cursor

**1. Install the plugin**
Settings → Plugins → **Add marketplace → Import from repo**, enter `kernoio/kerno-mcp-plugin`, install **kerno**, then reload the window (**Developer: Reload Window**).

**2. Paste this into your agent**
```
Set up Kerno for this workspace.

1. Confirm the kerno plugin is installed and its skills are available (e.g. /install-kerno resolves). If not, diagnose what's wrong and help me troubleshoot it before continuing.
2. Run /install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

Details: [cursor/README.md](cursor/README.md).

### Codex

**1. Install the plugin**
```
codex plugin marketplace add kernoio/kerno-mcp-plugin
```
Then open **`/plugins`**, install **kerno**, and start a new session.

**2. Paste this into your agent**
```
Set up Kerno for this workspace.

1. Confirm the kerno plugin is installed and its skills are available (e.g. @install-kerno resolves). If not, diagnose what's wrong and help me troubleshoot it before continuing.
2. Run @install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP in Codex.
3. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```

Details: [codex/README.md](codex/README.md).

## Layout (one repo, three clients)

| Client | Install guide | Plugin manifest |
|--------|---------------|-----------------|
| Claude Code | [claude/README.md](claude/README.md) | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) |
| Cursor | [cursor/README.md](cursor/README.md) | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) |
| Codex | [codex/README.md](codex/README.md) | [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) |

Shared content: `skills/`, `commands/`, `references/`.
