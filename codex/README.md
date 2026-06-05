# Codex — install

This package is a [Codex plugin](https://developers.openai.com/codex/plugins/): manifest at [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json), skills under `skills/`, and an optional bundled MCP template at [`.mcp.json`](../.mcp.json).

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-codex.md](../prompts/install-codex.md) into Codex.

## Install skills (recommended)

From your project root:

```bash
npx skills add kernoio/kerno-mcp-plugin
```

Use `-a codex` to target Codex explicitly, or `-g` for a user-wide install. Refresh after upstream changes: `npx skills update kernoio/kerno-mcp-plugin`.

Marketplace install is **not** available yet — do not use `codex plugin marketplace add`.

After installing skills, **start a new Codex thread** or restart Codex so skills load.

## First step after installing

Run **`@install-kerno`**. That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers the session MCP URL in Codex. See [Connect Kerno MCP](#connect-kerno-mcp) below.

## Prerequisites

- [Codex CLI](https://developers.openai.com/codex/cli/) installed and signed in (`codex login`)
- Node.js ≥ 18, Docker, and a git repo for the target project
- **`@kerno/cli`** for the Kerno agent — installed by the **install-kerno** skill (see [README.md](../README.md))

## Trust project config (project-scoped MCP)

Codex loads `.codex/config.toml` in a repo only when the project is **trusted**. Add to `~/.codex/config.toml` (replace with your absolute workspace path):

```toml
[projects."/absolute/path/to/your/repo"]
trust_level = "trusted"
```

## Connect Kerno MCP

Installing skills does **not** start the Kerno agent. Use the **install-kerno** skill first. The bundled [`.mcp.json`](../.mcp.json) is a template; the MCP port is **session-specific**.

1. In Codex, invoke **install-kerno** (`@install-kerno` or “set up Kerno MCP”).
2. Follow the skill: install `@kerno/cli`, run `kerno mcp -w <workspace>`, parse `MCP_URL` from CLI output.
3. Register that URL in Codex — see [references/mcp-client-config.md](../references/mcp-client-config.md) (**Codex** row).

Example project-scoped MCP (after you know `MCP_URL`):

```toml
# .codex/config.toml in your application repo
[mcp_servers.kerno]
url = "http://127.0.0.1:<port>/mcp"
enabled = true
```

User-scoped alternative: same `[mcp_servers.kerno]` block in `~/.codex/config.toml`.

## Bundled skills

| Skill | Use when |
|-------|----------|
| **install-kerno** | **First** — CLI, agent, and MCP registration |
| **kerno-bootstrap** | Recommended bootstrap workflow |
| **kerno-background-job** | `kerno_start_environment` + `kerno_job` |
| **kerno-validate** | After code changes |
| **kerno-capture-baseline** | Scenario capture workflow |

Codex discovers skills from `skills/*/SKILL.md` via the manifest `skills` field.

## Further reading

- [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
- [Build plugins (Codex)](https://developers.openai.com/codex/plugins/build)
- [Plugin root README](../README.md)
