---
name: install-kerno
description: >-
  Installs and connects Kerno for a project — CLI, login, local agent bound to
  the workspace, host MCP registration, verification, and next-step handoff.
  Use when the user runs /install-kerno, says "set up Kerno", "install Kerno",
  "configure Kerno MCP", "connect Kerno", or first-time Kerno onboarding.
version: 0.1.0
---

# Install Kerno

Kerno is a local backend-validation engine: **`@kerno/cli`** supervises an agent and exposes MCP over HTTP on **loopback**. The port is **not fixed** — read it from CLI output every time.

**This skill covers bootstrap only.** After MCP is live, read each tool's schema before calling it — do not replay workflow steps from memory.

**Reference:** `${CLAUDE_PLUGIN_ROOT}/references/mcp-client-config.md` — **Install (CLI)** section for host registration, scope aliases, troubleshooting.

Official docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)

## Before you start

**Prerequisites** (stop and tell the user if any are missing):

- Node.js ≥ 18 and `npm` on PATH
- Docker running
- Target project is a **git repository**
- A Kerno account (https://kerno.io)
- An MCP-capable assistant host (IDE, CLI agent, etc.)

**Workspace:** Set `WORKSPACE` once — the absolute path passed to `kerno mcp -w`. Use the **current project root** unless the user specifies another path. Pass the same path as `workspace_path` on every MCP call.

**MCP URL:** Set `MCP_URL` from CLI output after starting the agent — never assume a default port. Docs often mention 8086; the CLI may bind another port for this session.

> **Port ≠ workspace ready.** A listener on an old port may be stale or bound to another session. Always run `kerno mcp -w "$WORKSPACE"` before MCP registration — never skip because some port is already listening.

**Parallel preflight:** `kerno --version`, `docker info`, confirm `$WORKSPACE` is a git repo, scan existing MCP configs for duplicate Kerno entries.

## Checklist

Work in order. Pause at **(user)** checkpoints. Report progress briefly (✓ / ✗ / pending).

- [ ] **Install CLI** — `npm install -g @kerno/cli` then `kerno --version`
- [ ] **Login** — `kerno login` **(user)** on fresh machines
- [ ] **Start agent + discover MCP URL** — `kerno mcp -w "$WORKSPACE"`; parse output for `MCP_URL`
- [ ] **Workspace gate** — agent started successfully; output shows MCP port/URL for this workspace
- [ ] **Ask host** **(user)** — which assistant or IDE; never infer from the current session
- [ ] **Ask MCP scope** **(user)** — project/repo vs user/machine; never assume
- [ ] **Register MCP** — use parsed `MCP_URL`; only after workspace gate + host + scope chosen
- [ ] **Resolve server id** — find actual MCP server name from host descriptors before calling tools
- [ ] **Refresh host** **(user)** — only if Kerno tools are not visible yet
- [ ] **Verify (Tier C)** — `kerno_get_applications(workspace_path: "$WORKSPACE")` via MCP
- [ ] **Hand off** — workspace reminder + next actions **(user)**

**Completion:** Tier C — `kerno_get_applications` succeeds once the host sees Kerno tools.

**Must not during bootstrap:** hardcode an MCP URL without reading CLI output; run `kerno start` and `kerno mcp` in parallel; register MCP before the workspace gate passes.

## Phase 1 — CLI

```bash
npm install -g @kerno/cli
kerno --version
```

If global install is not possible: `npx -y -p @kerno/cli kerno …`

## Phase 2 — Login

```bash
kerno login
```

Blocks on browser OAuth — **pause** and wait for the user to confirm login finished.

## Phase 3 — Start agent and discover MCP URL

**Always run** (even if an agent appears to be running already):

```bash
kerno mcp -w "$WORKSPACE"
```

First run may download the agent runtime (can take a minute). Read the **full command output** before proposing any MCP config to the user.

### Parse output → set `MCP_URL`

Extract the MCP endpoint from the CLI output. Prefer, in order:

1. A full URL in a printed registration snippet (e.g. `http://127.0.0.1:<port>/mcp` or `http://localhost:<port>/mcp`)
2. A line like `MCP server running on port <N>` → build `http://127.0.0.1:<N>/mcp`

Also confirm from the same output:

- **Agent started successfully** (or equivalent success marker)
- **Workspace** line matches `$WORKSPACE` (absolute path)

If output is missing port/URL, re-run `kerno mcp -w "$WORKSPACE"` once. Do not guess a port.

Optional check: `lsof -i :<port>` shows a listener on the parsed port.

**Workspace gate:** command succeeds, workspace matches, and `MCP_URL` is known.

If MCP calls fail later, re-run `kerno mcp -w "$WORKSPACE"`, re-parse `MCP_URL`, update host config if the port changed, then retry — do not re-register blindly with a stale URL.

## Phase 4 — Register MCP

1. Confirm workspace gate and **`MCP_URL`** from Phase 3
2. **Ask host** **(user)** — which MCP-capable assistant they use; wait for an explicit answer
3. **Ask scope** **(user)** — project/repo (config in repo) vs user/machine (global); see reference for aliases
4. Merge into existing MCP config; do not overwrite unrelated servers
5. Register with the **parsed `MCP_URL`** — shape (minimal):

```json
{
  "mcpServers": {
    "kerno": {
      "url": "<MCP_URL from CLI output>"
    }
  }
}
```

The CLI may print host-specific registration snippets in its output — use them as hints for the chosen host, but still confirm host and scope with the user. Add transport/type fields only when required — see reference.

6. Resolve MCP server id from host tool descriptors (e.g. `kerno_get_applications.json` parent folder)
7. If tools not visible → user refreshes or reconnects the host per its MCP docs **(user)**

**Codex:** merge `[mcp_servers.kerno]` with `url = "<MCP_URL>"` into `.codex/config.toml` (project) or `~/.codex/config.toml` (user). If using project scope, confirm `trust_level = "trusted"` for `$WORKSPACE` in `~/.codex/config.toml`. Install skills first with `npx skills add kernoio/kerno-mcp-plugin` (see [codex/README.md](../codex/README.md)) if skills are missing — do not use plugin marketplaces. Restart Codex or start a new thread after config changes.

## Phase 5 — Verify

Call **`kerno_get_applications`** with `workspace_path: "$WORKSPACE"`. Save `workspace_id` and supported apps.

If healthcheck fails with a schema error but applications work, treat MCP as connected.

## After install — tell the user

Once Tier C passes, say plainly that Kerno is connected. Include:

1. **Use your assistant in this workspace** — Kerno is bound to `$WORKSPACE`. Open your MCP host **inside that folder** (same absolute path). Tools only work when the assistant session matches the bound workspace.

2. **Apps found** — summarize supported apps; mention unsupported if any.

3. **Next steps** — ask what they want to do:

   > What would you like to do next?
   > - **Set up your environment** — generate a compose plan and start the local stack (async jobs; can take many minutes)
   > - **Search endpoints** — list HTTP routes for an app (lightweight)
   > - **Plan an endpoint test** — explore routes and validation/scenario workflow
   > - **Stop here** — MCP is connected; nothing else for now

4. If multiple supported apps, ask which app to work with. If one app, confirm it. If zero, explain what Kerno found and stop.

**Hand off:** After the user picks an app and intent, read MCP tool schemas only — e.g. `kerno_list_endpoints` with required **`scope`** for explore; for environment setup load **`${CLAUDE_PLUGIN_ROOT}/skills/kerno-environment-setup/SKILL.md`** (compose plan approval gate + start environment). Do not continue from this skill.

## Agent-safe checks

Do not rely on `kerno status` in agent shells (Ink TUI fails). Use:

| Check | Command | Pass |
|-------|---------|------|
| CLI | `kerno --version` | version printed |
| Docker | `docker info` | server version |
| Agent + URL | `kerno mcp -w "$WORKSPACE"` | success + `MCP_URL` parsed |
| MCP live | `kerno_get_applications` | apps returned |
