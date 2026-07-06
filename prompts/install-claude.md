Install and set up the Kerno MCP plugin from https://github.com/kernoio/kerno-mcp-plugin for this workspace.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Clone https://github.com/kernoio/kerno-mcp-plugin to ~/.kerno/mcp-plugin and load it as a Claude Code plugin with `claude --plugin-dir ~/.kerno/mcp-plugin` (see claude/README.md). Do not use `/plugin marketplace`.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
