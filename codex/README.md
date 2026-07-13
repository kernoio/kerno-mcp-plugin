# Codex — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

[Codex plugin](https://developers.openai.com/codex/plugins/) manifest: [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json). **Fastest:** paste [prompts/install-codex.md](../prompts/install-codex.md) into Codex.

Public marketplace install is **not** available yet — do not use `codex plugin marketplace add`. Clone and register as a **local** plugin source:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
mkdir -p ~/.agents/plugins
```

Merge into `~/.agents/plugins/marketplace.json` (create if needed):

```json
{
  "name": "kerno-local",
  "interface": { "displayName": "Kerno (local)" },
  "plugins": [
    {
      "name": "kerno",
      "source": { "source": "local", "path": "../../.kerno/mcp-plugin" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Developer Tools"
    }
  ]
}
```

Adjust `source.path` so it resolves from `~/.agents/plugins/` to your clone. Restart Codex, open `/plugins`, install **kerno**, then run **`@install-kerno`**.

**Developing in this repo:** use [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) (local `./` checkout). Trust the project in `~/.codex/config.toml` — see **`mcp-client-config.md`** § Codex.

Installing the plugin does **not** start the Kerno agent. **`@install-kerno`** installs `@kerno/cli`, runs `kerno init -w <workspace>`, and registers the session MCP URL. Full steps: [references/mcp-client-config.md](../references/mcp-client-config.md). Bundled MCP template: [`.mcp.json`](../.mcp.json) (replace URL after each `kerno init -w`).

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart) · [Build plugins (Codex)](https://developers.openai.com/codex/plugins/build)
