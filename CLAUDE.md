# CLAUDE.md — kerno-claude-plugin

This directory ships **two** plugin manifests for the same assets:

- **Claude Code:** `.claude-plugin/plugin.json`
- **Cursor:** `.cursor-plugin/plugin.json`

The aicore-agent binary is not included.

## Source of truth

- **Agent + MCP:** `agent/apps/agent/docs/mcp.md` in the aicore repo.
- **Tool names and descriptions:** `agent/libs/kerno-mcp/.../KernoMcpRegistration.kt`.

## Layout

| Path | Role |
|------|------|
| `.claude-plugin/plugin.json` | Claude Code manifest |
| `.cursor-plugin/plugin.json` | Cursor manifest |
| `commands/*.md` | Slash commands (both ecosystems where supported) |
| `skills/*/SKILL.md` | Procedural skills |
| `references/*.md` | Long-form client config, ordering, and tool-specific notes (e.g. `capture-baseline.md`) |
| `rules/*.mdc` | Cursor-discovered rules |
| `mcp.json` | MCP server template at plugin root (Cursor) |
| `cursor/README.md` | Cursor install notes |

## Conventions

- **${CLAUDE_PLUGIN_ROOT}** — use for paths to plugin files inside skills/commands (Claude Code).
- Skills: third-person descriptions in frontmatter (woterclip-style).
