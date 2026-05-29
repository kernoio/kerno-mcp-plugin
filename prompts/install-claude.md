Install and set up Kerno MCP for this workspace using https://github.com/kernoio/kerno-mcp-plugin.

Do not use any plugin marketplace — Kerno is not published to marketplaces yet.

1. Run `npx skills add kernoio/kerno-mcp-plugin -y` from the project root to install Kerno skills on this machine.
   For slash commands too: clone the repo to ~/.kerno/mcp-plugin and restart Claude with `claude --plugin-dir ~/.kerno/mcp-plugin` (see claude/README.md). Do not use `/plugin marketplace`.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno mcp -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
