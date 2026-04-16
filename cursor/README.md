# Cursor — legacy templates

**Prefer the Cursor plugin layout at this package root:** `.cursor-plugin/plugin.json`, `rules/`, `mcp.json`, `skills/`, `commands/` (see [README.md](../README.md)).

## Cursor plugin (recommended)

1. Symlink or copy this folder into Cursor’s local plugins directory:

   ```bash
   ln -s /path/to/aicore/kerno-claude-plugin ~/.cursor/plugins/local/kerno-mcp
   ```

2. Restart Cursor or run **Developer: Reload Window**.

3. Components are discovered from default directories (`rules/`, `skills/`, `commands/`, root `mcp.json`). See [Cursor plugin docs](https://cursor.com) for manifest fields and optional custom paths.

## Files in this folder

| File | Purpose |
|------|---------|
| [mcp.json.example](mcp.json.example) | Same shape as root [mcp.json](../mcp.json); kept for docs that linked here earlier |

Canonical rule content lives in [rules/kerno-mcp.mdc](../rules/kerno-mcp.mdc).
