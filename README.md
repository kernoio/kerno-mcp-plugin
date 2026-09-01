# Kerno MCP plugin — deprecated

> **This plugin is deprecated and no longer maintained.** Kerno no longer ships as an editor plugin.

Kerno now sets up entirely through its CLI and MCP server, with no plugin to install. The `@kerno/cli` prints the MCP registration snippet when you run `kerno init`, and the Kerno MCP server carries its own tool descriptions and guides, so your coding agent gets the full workflow without any plugin-side skills or slash commands.

## Set up Kerno

Follow the quickstart: **https://kerno.gitbook.io/docs/getting-started/quickstart**

In short:

```bash
npm install -g @kerno/cli
kerno login
kerno init -w /absolute/path/to/your/repo
```

Then register the MCP server with your coding tool using the snippet `kerno init` prints, and verify with `kerno_get_applications`.

## Already installed the plugin?

You can remove it — it is no longer needed and receives no updates:

- **Claude Code:** `/plugin uninstall kerno@kerno`
- **Cursor:** Settings → Plugins → remove **kerno**
- **Codex:** remove **kerno** from `/plugins`

Uninstall guide: https://kerno.gitbook.io/docs/getting-started/uninstall-kerno

---

This repository is archived for reference. Its history holds the former plugin skills, commands, and references; none of it is published to a marketplace any more.
