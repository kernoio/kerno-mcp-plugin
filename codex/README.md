# Codex — install and plugin management

This package is a [Codex plugin](https://developers.openai.com/codex/plugins/): manifest at [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json), skills under `skills/`, and an optional bundled MCP template at [`.mcp.json`](../.mcp.json).

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-codex.md](../prompts/install-codex.md) into Codex.

## First step after installing the plugin

Installing **kerno** only adds skills and references. The **first thing to do next** is run the **install-kerno** skill in the workspace you want to validate:

- Type `@` and choose **install-kerno**, or ask Codex to “set up Kerno MCP”.

That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers the session MCP URL in Codex. See [Connect Kerno MCP](#connect-kerno-mcp) below.

## Prerequisites

- [Codex CLI](https://developers.openai.com/codex/cli/) installed and signed in (`codex login`)
- Node.js ≥ 18, Docker, and a git repo for the target project
- **`@kerno/cli`** for the Kerno agent — installed by the **install-kerno** skill (see [README.md](../README.md))

## Install the plugin

Pick one path. After any install, **start a new Codex thread** or restart Codex so skills load. Then run **`@install-kerno`** (see above).

### Option A — Plugin directory (recommended)

From Codex CLI, open the plugin browser and install from a marketplace:

```text
codex
/plugins
```

1. Add the [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) repo as a marketplace source (once per machine):

   ```bash
   codex plugin marketplace add kernoio/kerno-mcp-plugin
   ```

   To pin a branch: `codex plugin marketplace add kernoio/kerno-mcp-plugin --ref main`

2. In `/plugins`, select the **Kerno MCP** marketplace, open **kerno**, and choose **Install plugin**.

3. Run **`@install-kerno`** in your project ([First step after installing the plugin](#first-step-after-installing-the-plugin)).

Manage marketplaces from the CLI:

```bash
codex plugin marketplace list
codex plugin marketplace upgrade
codex plugin marketplace remove kerno
```

### Option B — Clone + personal marketplace

For local development or offline use:

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

Adjust `source.path` so it resolves from `~/.agents/plugins/` to your clone. Restart Codex, install **kerno** from `/plugins`, then run **`@install-kerno`**.

### Option C — Repo marketplace (monorepo / this checkout)

When this repository is your project root, Codex can read [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json). The entry points at `./` (this repo). Trust the project (see below), restart Codex, open `/plugins`, select the **Kerno MCP** marketplace, install **kerno**, then run **`@install-kerno`**.

## Enable, disable, or remove

| Goal | Action |
|------|--------|
| Turn off without uninstalling | In `~/.codex/config.toml`: `[plugins."kerno@kerno"]` → `enabled = false`, then restart Codex |
| Uninstall | `/plugins` → open **kerno** → **Uninstall plugin** |
| Refresh after git pull | Update your clone or run `codex plugin marketplace upgrade`, then restart Codex |

Exact plugin keys in `config.toml` may include the marketplace name; check `~/.codex/config.toml` after install.

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
| **kerno-mcp-bootstrap** | Recommended bootstrap workflow |
| **kerno-mcp-background-job** | `kerno_start_environment` + `kerno_job` |
| **kerno-mcp-validate** | After code changes |
| **kerno-mcp-capture-baseline** | Scenario capture workflow |

Codex discovers skills from `skills/*/SKILL.md` via the manifest `skills` field.

## Further reading

- [Setup Kerno MCP](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)
- [Build plugins (Codex)](https://developers.openai.com/codex/plugins/build)
- [Plugin root README](../README.md)
