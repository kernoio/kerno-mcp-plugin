Install and set up Kerno MCP for this project using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Follow cursor/README.md: clone https://github.com/kernoio/kerno-mcp-plugin to ~/.kerno/mcp-plugin and symlink into ~/.cursor/plugins/local/kerno, then reload Cursor.
2. Run /install-kerno to install @kerno/cli, bind the agent to this workspace with kerno mcp -w, and register MCP with the URL from CLI output.
3. Confirm Kerno MCP tools are available in this project folder.

Work in this repository root unless I specify another path.
