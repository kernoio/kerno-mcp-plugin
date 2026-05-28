# Cursor — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

Manifest: [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json). Shared skills, commands, and rules live at the [plugin root](../README.md).

## Install the plugin

Symlink or copy a checkout into Cursor’s local plugins folder, then reload the window:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno-mcp
```

Restart Cursor or run **Developer: Reload Window**.

Components are discovered from `rules/`, `skills/`, and `commands/` at the plugin root. See [Cursor plugin docs](https://cursor.com) for manifest details and [marketplace publish](https://cursor.com/marketplace/publish) when ready.

## First step after installing the plugin

Run **`/install-kerno`**. That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers MCP for Cursor.

## MCP

Point Kerno at your workspace using `.cursor/mcp.json` or `~/.cursor/mcp.json` (same JSON shape as root [`.mcp.json`](../.mcp.json); replace the URL after `kerno mcp -w`). Details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Cursor** row).

Example shape: [mcp.json.example](mcp.json.example).

## Rules

Canonical rule content: [rules/kerno-mcp.mdc](../rules/kerno-mcp.mdc).

## Further reading

- [Plugin root README](../README.md)
- [Setup Kerno MCP](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)
