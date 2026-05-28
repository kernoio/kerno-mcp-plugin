# CLAUDE.md — kerno-claude-plugin

This directory ships **three** plugin manifests for the same assets:

- **Claude Code:** `.claude-plugin/plugin.json`
- **Cursor:** `.cursor-plugin/plugin.json`
- **Codex:** `.codex-plugin/plugin.json`

The aicore-agent binary is not included.

## Source of truth

- **Agent + MCP:** `agent/apps/agent/docs/mcp.md` in the aicore repo.
- **Tool names and descriptions:** `agent/libs/kerno-mcp/.../KernoMcpRegistration.kt`.

## Where to start (user onboarding)

1. Install the plugin (see root README).
2. Run **`/install-kerno`** — skill `skills/install-kerno/SKILL.md`.
3. User must open their MCP host in the **same workspace** bound by `kerno mcp -w`.

## Layout

| Path | Role |
|------|------|
| `.claude-plugin/plugin.json` | Claude Code manifest |
| `.cursor-plugin/plugin.json` | Cursor manifest |
| `commands/*.md` | Slash commands (both ecosystems where supported) |
| `skills/install-kerno/SKILL.md` | First-time CLI + MCP install |
| `skills/*/SKILL.md` | Procedural skills |
| `references/mcp-client-config.md` | CLI install, host registration, operator config, client timeouts |
| `references/*.md` | Tool ordering and tool-specific notes (e.g. `capture-baseline.md`) |
| `rules/*.mdc` | Cursor-discovered rules |
| `mcp.json` | MCP server template at plugin root (Cursor) |
| `cursor/README.md` | Cursor install notes |

## Conventions

- **${CLAUDE_PLUGIN_ROOT}** — use for paths to plugin files inside skills/commands (Claude Code).
- Skills: third-person descriptions in frontmatter (woterclip-style).
