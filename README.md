# Kerno MCP (Claude Code + Cursor + Codex plugin)

**Kerno** is a runtime QA engine for backend coding agents: it generates and runs integration tests against your real stack, so your agent catches its own regressions before they reach a PR.

This repo is the **plugin** that connects Kerno to your coding tool (Claude Code, Cursor, or Codex): it adds the slash commands and skills that teach the agent how to work with Kerno.

## Install

Install the **kerno** plugin, then paste the setup prompt into your agent to configure Kerno for your project.

Prerequisites: Node.js ≥ 18, npm, Docker running, a git repository, and a Kerno account.

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
