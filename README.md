# Kerno MCP (Claude Code + Cursor + Codex plugin)

**Kerno** is a runtime QA engine for backend coding agents: it generates and runs integration tests against your real stack, so your agent catches its own regressions before they reach a PR.

This repo is the **plugin** that connects Kerno to your coding tool (Claude Code, Cursor, or Codex): it adds the slash commands and skills that teach the agent how to work with Kerno.

## Install

Paste the setup prompt into your agent to configure Kerno for your project.

Prerequisites: Node.js ≥ 18, npm, Docker running, a git repository, and a Kerno account.

### Claude Code

Paste this into your agent:
```
Set up Kerno for this workspace.

1. Run /install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
2. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Cursor

Paste this into your agent:
```
Set up Kerno for this workspace.

1. Run /install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
2. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Codex

Paste this into your agent:
```
Set up Kerno for this workspace.

1. Run @install-kerno to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP in Codex.
2. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```
