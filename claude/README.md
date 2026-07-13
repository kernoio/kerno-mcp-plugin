# Claude Code — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

Install from the Kerno marketplace, then run the setup skill:

```
/plugin marketplace add kernoio/kerno-mcp-plugin
/plugin install kerno@kerno
/install-kerno
```

**Developing on the plugin?** Point Claude at a local checkout instead (restart Claude after updating it):

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

`/install-kerno` installs `@kerno/cli`, logs in, starts the agent, and registers MCP. MCP registration details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Claude Code** row). Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
