# Codex — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

[Codex plugin](https://developers.openai.com/codex/plugins/) manifest: [`.codex-plugin/plugin.json`](../.codex-plugin/plugin.json).

Install from the Kerno marketplace, then run the setup skill:

```bash
codex plugin marketplace add kernoio/kerno-mcp-plugin
```

Open **`/plugins`**, install **kerno**, start a new session, then run **`@install-kerno`**.

Installing the plugin does **not** start the Kerno agent. **`@install-kerno`** installs `@kerno/cli`, runs `kerno init -w <workspace>`, and registers the session MCP URL. Full steps: [references/mcp-client-config.md](../references/mcp-client-config.md). Bundled MCP template: [`mcp.json.example`](../mcp.json.example) (replace URL after each `kerno init -w`).

Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart) · [Build plugins (Codex)](https://developers.openai.com/codex/plugins/build)
