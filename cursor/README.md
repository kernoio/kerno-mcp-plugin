# Cursor — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

**Fastest:** paste [prompts/install-cursor.md](../prompts/install-cursor.md) into Cursor Agent, or use the [Open in Cursor](https://cursor.com/link/prompt?text=Install%20and%20set%20up%20Kerno%20MCP%20for%20this%20project%20using%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin.%0A%0ADo%20not%20use%20any%20plugin%20marketplace%20%E2%80%94%20Kerno%20is%20not%20published%20to%20marketplaces%20yet.%0A%0A1.%20Follow%20cursor%2FREADME.md%3A%20clone%20https%3A%2F%2Fgithub.com%2Fkernoio%2Fkerno-mcp-plugin%20to%20~%2F.kerno%2Fmcp-plugin%20and%20symlink%20into%20~%2F.cursor%2Fplugins%2Flocal%2Fkerno%2C%20then%20reload%20Cursor.%0A2.%20Run%20%2Finstall-kerno%20to%20install%20%40kerno%2Fcli%2C%20bind%20the%20agent%20to%20this%20workspace%20with%20kerno%20mcp%20-w%2C%20and%20register%20MCP%20with%20the%20URL%20from%20CLI%20output.%0A3.%20Confirm%20Kerno%20MCP%20tools%20are%20available%20in%20this%20project%20folder.%0A%0AWork%20in%20this%20repository%20root%20unless%20I%20specify%20another%20path.) deeplink ([regenerate](../references/cursor-install-deeplink.md) after prompt edits).

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
ln -s ~/.kerno/mcp-plugin ~/.cursor/plugins/local/kerno
```

Reload the window (**Developer: Reload Window**), then run **`/install-kerno`**.

MCP config: `.cursor/mcp.json` or `~/.cursor/mcp.json` — same shape as [`.mcp.json`](../.mcp.json); replace the URL after `kerno mcp -w`. Details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Cursor** row). Example: [mcp.json.example](mcp.json.example). Rules: [rules/kerno.mdc](../rules/kerno.mdc).
