# Cursor — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-cursor.md](../prompts/install-cursor.md) into Cursor Agent.

Manifest: [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json). Shared skills, commands, and rules live at the [plugin root](../README.md).

Regenerate **Open in Cursor** deeplinks after editing the prompt: `python3 scripts/generate-cursor-install-deeplink.py` — then copy from [references/cursor-install-deeplink.md](../references/cursor-install-deeplink.md).

## Install skills (recommended)

From your project root:

```bash
npx skills add kernoio/kerno-mcp-plugin
```

Use `-g` for a user-wide install. Refresh after upstream changes: `npx skills update kernoio/kerno-mcp-plugin`.

## Full plugin (slash commands + rules)

Symlink or copy a checkout into Cursor’s local plugins folder, then reload the window:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno
```

Restart Cursor or run **Developer: Reload Window**.

Components are discovered from `rules/`, `skills/`, and `commands/` at the plugin root.

## First step after installing

Run **`/install-kerno`**. That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers MCP for Cursor.

## MCP

Point Kerno at your workspace using `.cursor/mcp.json` or `~/.cursor/mcp.json` (same JSON shape as root [`.mcp.json`](../.mcp.json); replace the URL after `kerno mcp -w`). Details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Cursor** row).

Example shape: [mcp.json.example](mcp.json.example).

## Rules

Canonical rule content: [rules/kerno.mdc](../rules/kerno.mdc).

## Further reading

- [Plugin root README](../README.md)
- [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
