# Codex — install

This package is a [Codex plugin](https://developers.openai.com/codex/plugins/): manifest at [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json), skills under `skills/`, and an optional bundled MCP template at [`.mcp.json`](../.mcp.json).

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-codex.md](../prompts/install-codex.md) into Codex.

## Install the plugin

Public marketplace install is **not** available yet — do not use `codex plugin marketplace add`. Clone the repo and register it as a **local** plugin source.

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
mkdir -p ~/.agents/plugins
```

Merge into `~/.agents/plugins/marketplace.json` (create the file if needed):

```json
{
  "name": "kerno-local",
  "interface": { "displayName": "Kerno (local)" },
  "plugins": [
    {
      "name": "kerno",
      "source": {
        "source": "local",
        "path": "../../.kerno/mcp-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

Adjust `source.path` so it resolves from `~/.agents/plugins/` to your clone. Restart Codex, open `/plugins`, select **Kerno (local)**, install **kerno**, then run **`@install-kerno`**.

### Developing in this repo

When this repository is your project root, Codex can read [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) (local `./` checkout). Trust the project (see below), restart Codex, install **kerno** from `/plugins`, then run **`@install-kerno`**.

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

Installing the plugin does **not** start the Kerno agent. Use the **install-kerno** skill first. The bundled [`.mcp.json`](../.mcp.json) is a template; the MCP port is **session-specific**.

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
| **kerno-bootstrap** | Connectivity checks |
| **kerno-environment-setup** | save_config → environment_setup → environment_status |
| **kerno-endpoint-test** | Generate or validate endpoint tests |
| **kerno-background-job** | Async job polling (`kerno_job`, `kerno_cancel`) |

Codex discovers skills from `skills/*/SKILL.md` via the manifest `skills` field.

## Further reading

- [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
- [Build plugins (Codex)](https://developers.openai.com/codex/plugins/build)
- [Plugin root README](../README.md)
