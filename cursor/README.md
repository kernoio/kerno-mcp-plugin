# Cursor — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

Install from the Kerno marketplace, then run the setup skill:

1. Open Cursor **Settings → Plugins** (or [cursor.com/dashboard](https://cursor.com/dashboard) → Plugins).
2. **Add marketplace → Import from repo**, and enter `kernoio/kerno-mcp-plugin`.
3. Install **kerno**, reload the window (**Developer: Reload Window**), then run **`/install-kerno`**.

`/install-kerno` installs `@kerno/cli`, logs in, binds the agent to this workspace with `kerno init -w`, and registers MCP with the URL from CLI output.

MCP config: `.cursor/mcp.json` or `~/.cursor/mcp.json`, same shape as [`mcp.json.example`](../mcp.json.example); replace the URL after `kerno init -w`. Details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Cursor** row). Example: [mcp.json.example](mcp.json.example). Rules: [rules/kerno.mdc](../rules/kerno.mdc).
