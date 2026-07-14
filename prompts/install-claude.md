Install and set up the Kerno MCP plugin from https://github.com/kernoio/kerno-mcp-plugin for this workspace.

1. Install from the Kerno marketplace: run `claude plugin marketplace add kernoio/kerno-mcp-plugin` then `claude plugin install kerno@kerno` (see claude/README.md), then restart Claude Code so the plugin loads.
2. Run the install-kerno skill (/install-kerno) to install @kerno/cli, log in, start the agent with kerno init -w on this project, and register MCP.
3. Verify kerno_get_applications works for this workspace path.

Work in this repository root unless I specify another path.
