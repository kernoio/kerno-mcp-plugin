# Cursor — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-cursor.md](../prompts/install-cursor.md) into Cursor Agent.

**Open in Cursor:** [Open in Cursor](https://cursor.com/link/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0A1.%20Follow%20cursor%2FREADME.md%20in%20that%20repo%3A%20clone%20it%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno-mcp%2C%20then%20reload%20Cursor.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) · [cursor://](cursor://anysphere.cursor-deeplink/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0A1.%20Follow%20cursor%2FREADME.md%20in%20that%20repo%3A%20clone%20it%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno-mcp%2C%20then%20reload%20Cursor.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) — opens the IDE with the install prompt above pre-filled (review and send; does not run automatically). [Link details](references/cursor-install-deeplink.md).

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
