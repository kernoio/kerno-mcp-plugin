# Claude Code — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin)

**Fastest:** paste [prompts/install-claude.md](../prompts/install-claude.md) into Claude Code.

Manifest: [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json). Shared skills and commands live at the [plugin root](../README.md).

## Install skills (recommended)

From your project root:

```bash
npx skills add kernoio/kerno-mcp-plugin
```

Use `-g` for a user-wide install. Refresh after upstream changes: `npx skills update kernoio/kerno-mcp-plugin`.

Marketplace install is **not** available yet — do not use `/plugin marketplace`.

## Full plugin (slash commands)

For slash commands in addition to skills, clone the repo and start Claude with `--plugin-dir`:

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

Or point `--plugin-dir` at any checkout of [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin). Restart Claude after adding or updating the checkout.

## First step after installing

Run **`/install-kerno`**. That skill installs `@kerno/cli`, runs `kerno login`, starts the agent with `kerno mcp -w <path>`, and registers MCP for Claude Code.

## MCP registration

Host-specific steps and scopes: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Claude Code** row).

## Further reading

- [Plugin root README](../README.md)
- [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
