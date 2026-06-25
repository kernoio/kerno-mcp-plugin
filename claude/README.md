# Claude Code — install

**GitHub:** [kernoio/kerno-mcp-plugin](https://github.com/kernoio/kerno-mcp-plugin) · [Plugin README](../README.md)

**Fastest:** paste [prompts/install-claude.md](../prompts/install-claude.md) into Claude Code.

```bash
git clone https://github.com/kernoio/kerno-mcp-plugin ~/.kerno/mcp-plugin
claude --plugin-dir ~/.kerno/mcp-plugin
```

Or point `--plugin-dir` at any checkout. Restart Claude after adding or updating the checkout. Public marketplace install is **not** available yet — do not use `/plugin marketplace`.

Then run **`/install-kerno`**. MCP registration details: [references/mcp-client-config.md](../references/mcp-client-config.md) (**Claude Code** row). Docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)
