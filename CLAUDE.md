# CLAUDE.md — kerno-mcp-plugin

This directory ships **three** plugin manifests for the same assets:

- **Claude Code:** `.claude-plugin/plugin.json`
- **Cursor:** `.cursor-plugin/plugin.json`
- **Codex:** `.codex-plugin/plugin.json`

The aicore-agent binary is not included. Human-facing index: [README.md](README.md).

## Source of truth

- **Agent + MCP:** `agent/apps/agent/docs/mcp.md` in the aicore repo.
- **Tool names and descriptions:** `agent/libs/kerno-mcp/.../KernoMcpRegistration.kt`.
- **Unified tool inventory:** `UNIFIED_MCP_TOOL_NAMES` in `McpToolSurface.kt`.
- **Canonical MCP workflow in this plugin:** `references/unified-flow.md`

## Where to start (user onboarding)

1. Install the plugin — [claude/README.md](claude/README.md), [cursor/README.md](cursor/README.md), or [codex/README.md](codex/README.md).
2. Run **`/install-kerno`** — skill `skills/install-kerno/SKILL.md`.
3. User must open their MCP host in the **same workspace** bound by `kerno mcp -w`.

## Conventions

- **Plugin-root paths** — use `skills/…` and `references/…` inside skills, commands, and rules (works in Cursor, Claude Code, and Codex). Claude Code also expands **`${CLAUDE_PLUGIN_ROOT}`** in commands if you need an absolute path there.
- Skills: third-person descriptions in frontmatter (woterclip-style).
- Skills link to **`references/`** for tables, anti-patterns, and tool semantics — do not duplicate reference content in skills.
- Document the unified MCP surface only — one canonical flow in **`references/unified-flow.md`**.
