# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **Kerno MCP** tools. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

**Source:** [github.com/kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

## Give this repo to your coding tool

Paste **one** prompt below into your assistant (Agent chat, Claude Code, Codex, etc.). It should clone or register this plugin, then run **install-kerno** to install the CLI, start the agent, and connect MCP for your workspace.

| Tool | Copy-paste prompt |
|------|-------------------|
| Claude Code | [prompts/install-claude.md](prompts/install-claude.md) |
| Cursor | [prompts/install-cursor.md](prompts/install-cursor.md) |
| Codex | [prompts/install-codex.md](prompts/install-codex.md) |

### Claude Code

```
Install and set up the Kerno MCP plugin from https://github.com/kernoio/kerno-mcp-plugin for this workspace.

1. Clone https://github.com/kernoio/kerno-mcp-plugin and load it as a Claude Code plugin (see claude/README.md in the repo).
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Cursor

```
Install and set up Kerno MCP for this project using https://github.com/kernoio/kerno-mcp-plugin.

1. Follow cursor/README.md in that repo: clone it and symlink into ~/.cursor/plugins/local/kerno-mcp, then reload Cursor.
2. Run /install-kerno to install @kerno/cli, bind the agent to this workspace with kerno mcp -w, and register MCP with the URL from CLI output.
3. Confirm Kerno MCP tools are available in this project folder.

Work in this repository root unless I specify another path.
```

**Cursor MCP deeplink (optional):** [Add Kerno MCP server in Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=kerno&config=eyJ1cmwiOiJodHRwOi8vMTI3LjAuMC4xOjgwODYvbWNwIn0=) — registers a Kerno MCP entry with a placeholder URL. Still run **`/install-kerno`** so the port matches your `kerno mcp -w` session. This link does not install plugin skills or rules; use the prompt above for full setup.

### Codex

```
Set up Kerno for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

1. Run: codex plugin marketplace add kernoio/kerno-mcp-plugin
2. Install plugin kerno-mcp from /plugins (Kerno MCP marketplace).
3. Run the install-kerno skill (@install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP in Codex.
4. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```

## Where to start

1. **Install the plugin** — use a [prompt above](#give-this-repo-to-your-coding-tool), or the minimal steps under [Install](#install--claude-code) ([Claude](#install--claude-code) · [Cursor](#install--cursor) · [Codex](#install--codex)).
2. **First thing after the plugin is installed:** run **install-kerno** (`/install-kerno` or `@install-kerno`).
3. **Open your assistant in the same workspace** you bound with `kerno mcp -w <path>`.

After MCP is connected, use `/kerno-bootstrap` or other skills for environment setup, endpoints, and validation.

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)

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

## Install — Claude Code

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

Then run **`/install-kerno`**. Details: [claude/README.md](claude/README.md).

## Install — Cursor

Symlink or copy the repo into Cursor’s local plugins folder, then reload the window:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno-mcp
```

Then run **`/install-kerno`**. Details: [cursor/README.md](cursor/README.md) · [MCP deeplink](cursor://anysphere.cursor-deeplink/mcp/install?name=kerno&config=eyJ1cmwiOiJodHRwOi8vMTI3LjAuMC4xOjgwODYvbWNwIn0=) (optional).

## Install — Codex

```bash
codex plugin marketplace add kernoio/kerno-mcp-plugin
# In Codex CLI: /plugins → Kerno MCP → Install kerno-mcp
```

Then run **`@install-kerno`**. Details: [codex/README.md](codex/README.md).

## Commands

| Command | Purpose |
|---------|---------|
| `/install-kerno` | First-time setup: CLI, agent, MCP registration, verification, next steps |
| `/kerno-bootstrap` | Run the recommended Kerno MCP workflow (healthcheck → get_applications → environment → job) |
| `/kerno-mcp-capture-baseline` | Point the agent at **`kerno_capture_baseline`** (scopes, async job, prerequisites) |
| `/kerno-mcp-help` | Pointers to MCP setup, job semantics, and references |

## Skills

- **install-kerno** — Step-by-step install and MCP connection for a workspace ([GitBook guide](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)). **Run this first** after adding the plugin.
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
