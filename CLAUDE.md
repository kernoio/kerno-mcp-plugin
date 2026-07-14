# CLAUDE.md — kerno-mcp-plugin

This directory ships **three** plugin manifests for the same assets:

- **Claude Code:** `.claude-plugin/plugin.json`
- **Cursor:** `.cursor-plugin/plugin.json`
- **Codex:** `.codex-plugin/plugin.json`

The Kerno agent binary is not included. Human-facing index: [README.md](README.md).

## Source of truth

- **Agent + MCP:** `agent/apps/agent/docs/mcp.md` in the Kerno backend repo.
- **Tool names and descriptions:** `agent/libs/kerno-mcp/.../KernoMcpRegistration.kt`.
- **Unified tool inventory:** `UNIFIED_MCP_TOOL_NAMES` in `McpToolSurface.kt`.
- **Canonical MCP workflow in this plugin:** `references/unified-flow.md`

## Where to start (user onboarding)

1. Install the plugin — [claude/README.md](claude/README.md), [cursor/README.md](cursor/README.md), or [codex/README.md](codex/README.md).
2. Run **`/install-kerno`** — skill `skills/install-kerno/SKILL.md`.
3. User must open their MCP host in the **same workspace** bound by `kerno init -w`.

## Conventions

- **Plugin-root paths** — use `skills/…` and `references/…` inside skills, commands, and rules (works in Cursor, Claude Code, and Codex). Claude Code also expands **`${CLAUDE_PLUGIN_ROOT}`** in commands if you need an absolute path there.
- Skills: third-person descriptions in frontmatter (woterclip-style).
- Skills link to **`references/`** for tables, anti-patterns, and tool semantics — do not duplicate reference content in skills.
- Document the unified MCP surface only — one canonical flow in **`references/unified-flow.md`**.

## Releasing (so marketplace installs see updates)

All three installs (Claude, Cursor, Codex) pull from this repo on `master`, but a tool only surfaces "update available" when the plugin `version` changes. Bump it every release, in lockstep across all three manifests:

1. `python3 scripts/bump-version.py <new-version>` (e.g. `0.2.0`) — updates `version` in `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/` plugin.json.
2. Commit the bump.
3. `claude plugin tag --push` — validates plugin.json vs the marketplace entry, tags `kerno--v<version>`, and pushes the tag.
4. Draft a GitHub Release for that tag (this is the notification channel: repo watchers get pinged; the editors themselves don't nag).

Users update via `claude plugin update kerno` / `codex plugin marketplace upgrade` / Cursor's marketplace Refresh.
