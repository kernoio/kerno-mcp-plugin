# Kerno MCP (Claude Code + Cursor + Codex plugin)

Markdown-only plugin: slash commands, skills, and rules that guide use of the **Kerno MCP** tools. The agent runtime is **not** included here — install and start it with **`@kerno/cli`**.

**Source:** [github.com/kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

## Give this repo to your coding tool

### Quick install (Skills CLI)

From your project root (or use `-g` for a user-wide install), install the plugin skills into the agents the CLI detects (Cursor, Claude Code, Codex, and others):

```bash
npx skills add kernoio/kerno-mcp-plugin
```

Then run **`/install-kerno`** (or **`@install-kerno`** in Codex) in that workspace to install `@kerno/cli`, start the agent with `kerno mcp -w`, and register MCP.

To refresh after upstream changes:

```bash
npx skills update kernoio/kerno-mcp-plugin
```

Useful flags: `-g` / `--global`, `-a cursor` (or `claude-code`, `codex`, …), `-y` to skip prompts. See [vercel-labs/skills](https://github.com/vercel-labs/skills).

**Marketplace install is not available yet** — use the GitHub repo directly (`npx skills add` or clone). This path installs **skills** (procedures). Slash commands, Cursor rules, and full plugin manifests still use the [per-client install](#install--claude-code) steps below if you need them.

### Or: paste a prompt into your assistant

Paste **one** prompt below into your assistant (Agent chat, Claude Code, Codex, etc.). It installs skills from the GitHub repo, then runs **install-kerno** to install the CLI, start the agent, and connect MCP for your workspace. Do **not** use plugin marketplaces.

| Tool | Copy-paste prompt |
|------|-------------------|
| Claude Code | [prompts/install-claude.md](prompts/install-claude.md) |
| Cursor | [prompts/install-cursor.md](prompts/install-cursor.md) |
| Codex | [prompts/install-codex.md](prompts/install-codex.md) |

### Claude Code

```
Install and set up Kerno MCP for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Run `npx skills add kernoio/kerno-mcp-plugin -y` from the project root to install Kerno skills on this machine.
   For slash commands too: clone the repo to ~/.kerno/mcp-plugin and restart Claude with `claude --plugin-dir ~/.kerno/mcp-plugin` (see claude/README.md). Do not use `/plugin marketplace`.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
```

### Cursor

**Open in Cursor:** use the link under the prompt block, or copy the text below.

```
Install and set up Kerno MCP for this project using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Run `npx skills add kernoio/kerno-mcp-plugin -y` from the project root to install Kerno skills.
   For slash commands, rules, and full plugin: clone to ~/.kerno/mcp-plugin and symlink into ~/.cursor/plugins/local/kerno, then reload Cursor (see cursor/README.md).
2. Run /install-kerno to install @kerno/cli, bind the agent to this workspace with kerno mcp -w, and register MCP with the URL from CLI output.
3. Confirm Kerno MCP tools are available in this project folder.

Work in this repository root unless I specify another path.
```

**Open in Cursor:** [Open in Cursor](https://cursor.com/link/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0ADo%20not%20use%20any%20plugin%20marketplace%20%E2%80%94%20Kerno%20is%20not%20published%20to%20marketplaces%20yet.%0A%0A1.%20Run%20%60npx%20skills%20add%20kernoio%2Fkerno-mcp-plugin%20-y%60%20from%20the%20project%20root%20to%20install%20Kerno%20skills.%0A%20%20%20For%20slash%20commands%2C%20rules%2C%20and%20full%20plugin%3A%20clone%20to%20~%2F.kerno%2Fmcp-plugin%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno%2C%20then%20reload%20Cursor%20%28see%20cursor%2FREADME.md%29.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) · [cursor://](cursor://anysphere.cursor-deeplink/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0ADo%20not%20use%20any%20plugin%20marketplace%20%E2%80%94%20Kerno%20is%20not%20published%20to%20marketplaces%20yet.%0A%0A1.%20Run%20%60npx%20skills%20add%20kernoio%2Fkerno-mcp-plugin%20-y%60%20from%20the%20project%20root%20to%20install%20Kerno%20skills.%0A%20%20%20For%20slash%20commands%2C%20rules%2C%20and%20full%20plugin%3A%20clone%20to%20~%2F.kerno%2Fmcp-plugin%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno%2C%20then%20reload%20Cursor%20%28see%20cursor%2FREADME.md%29.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) — opens the IDE with the install prompt above pre-filled (review and send; does not run automatically). [Link details](references/cursor-install-deeplink.md).


### Codex

```
Set up Kerno for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Run `npx skills add kernoio/kerno-mcp-plugin -y` from the project root to install Kerno skills on this machine.
2. Run the install-kerno skill (@install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP in Codex.
3. Verify Kerno MCP tools work in this workspace.

Work in this repository root unless I specify another path.
```

## Where to start

1. **Install the plugin** — [`npx skills add`](#quick-install-skills-cli) (fastest), a [prompt](#or-paste-a-prompt-into-your-assistant), or the minimal steps under [Install](#install--claude-code) ([Claude](#install--claude-code) · [Cursor](#install--cursor) · [Codex](#install--codex)).
2. **First thing after the plugin is installed:** run **install-kerno** (`/install-kerno` or `@install-kerno`).
3. **Open your assistant in the same workspace** you bound with `kerno mcp -w <path>`.

After MCP is connected, use `/kerno-bootstrap` to verify connectivity, then `/kerno-env` for environment setup, or other skills for endpoints and validation.

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
npx skills add kernoio/kerno-mcp-plugin
```

For slash commands too, clone and use `--plugin-dir`:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

Then run **`/install-kerno`**. Details: [claude/README.md](claude/README.md).

## Install — Cursor

```bash
npx skills add kernoio/kerno-mcp-plugin
```

For slash commands, rules, and full plugin, symlink a checkout into Cursor’s local plugins folder, then reload the window:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno
```

Then run **`/install-kerno`**. Details: [cursor/README.md](cursor/README.md) · deeplinks in [references/cursor-install-deeplink.md](references/cursor-install-deeplink.md) (regenerate after prompt edits).

## Install — Codex

```bash
npx skills add kernoio/kerno-mcp-plugin
```

Then run **`@install-kerno`**. Details: [codex/README.md](codex/README.md).

## Commands

| Command | Purpose |
|---------|---------|
| `/install-kerno` | First-time setup: CLI, agent, MCP registration, verification, next steps |
| `/kerno-bootstrap` | Verify MCP connectivity (healthcheck → get_applications → optional endpoints) |
| `/kerno-env` | Environment setup with compose plan approval gate → start environment |
| `/kerno-plan-implement-baseline` | Plan and implement scenario tests via **`kerno_plan_baseline`** + **`kerno_implement_baseline`** |
| `/kerno-capture-baseline` | Deprecated alias — use **`/kerno-plan-implement-baseline`** |
| `/kerno-help` | Pointers to MCP setup, job semantics, and references |

## Skills

- **install-kerno** — Step-by-step install and MCP connection for a workspace ([GitBook guide](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)). **Run this first** after adding the plugin.
- **kerno-bootstrap** — Connectivity/bootstrap checks (no environment bring-up).
- **kerno-environment-setup** — Compose plan approval gate + start environment (recommended for “setup the env” requests).
- **kerno-background-job** — How to use `kerno_start_environment` + `kerno_job` (wait, timeouts, logs).
- **kerno-validate** — Run **`kerno_validate`** after code changes; do not patch **`.kerno/scenarios/`** before validate / plan-implement.
- **kerno-plan-implement-baseline** — When and how to use **`kerno_plan_baseline`** and **`kerno_implement_baseline`** (two-stage scenario authoring).
- **kerno-capture-baseline** — Deprecated; redirects to plan-implement-baseline.

## Rules (Cursor)

- [rules/kerno.mdc](rules/kerno.mdc) — Tool ordering and async-job constraints (`alwaysApply: true`).

Canonical operator details (ports, env, workspace invariant) remain in **`agent/apps/agent/docs/mcp.md`** in the main repo.

## References

- **[references/mcp-client-config.md](references/mcp-client-config.md)** — CLI install, host registration, operator env, timeouts (single connection reference).
- **[references/tool-ordering.md](references/tool-ordering.md)** — Recommended tool order aligned with shipped MCP tools.
- **[references/compose-plan.md](references/compose-plan.md)** — Compose plan generate/feedback workflow before **`kerno_start_environment`**.
- **[references/plan-implement-baseline.md](references/plan-implement-baseline.md)** — **`kerno_plan_baseline`** and **`kerno_implement_baseline`** parameters, scopes, and job response fields.
- **[references/capture-baseline.md](references/capture-baseline.md)** — Deprecated redirect to plan-implement-baseline.
- **[references/cursor-install-deeplink.md](references/cursor-install-deeplink.md)** — Cursor “Open in Cursor” prompt deeplinks (regenerate with `scripts/generate-cursor-install-deeplink.py`).
