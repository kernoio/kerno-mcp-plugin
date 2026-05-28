# Claude Code — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

Manifest: [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json). Shared skills and commands live at the [plugin root](../README.md).

## Install the plugin

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

Or point `--plugin-dir` at any checkout of [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin).

## First step after installing the plugin

Run **`/install-kerno`**. That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers MCP for Claude Code.

## MCP registration

Host-specific steps and scopes: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Claude Code** row).

## Further reading

- [Plugin root README](../README.md)
- [Setup Kerno MCP](https://kerno.gitbook.io/docs/user-manual/setup-kerno-mcp)
