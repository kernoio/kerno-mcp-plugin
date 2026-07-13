---
name: install-kerno
description: >-
  Installs and connects Kerno for a project — CLI, login, local agent bound to
  the workspace, host MCP registration, verification, and next-step handoff.
  Use when the user runs /install-kerno, says "set up Kerno", "install Kerno",
  "configure Kerno MCP", "connect Kerno", or first-time Kerno onboarding.
version: 0.2.1
---

# Install Kerno

Kerno is a local backend-validation engine: **`@kerno/cli`** supervises an agent and exposes MCP over HTTP on **loopback**. The port is **not fixed** — read it from CLI output every time.

**This skill covers bootstrap only.** After MCP is live, read each tool's schema before calling it — do not replay workflow steps from memory.

**Reference:** `references/mcp-client-config.md` — **Install (CLI)** for `MCP_URL` parsing, host registration, scope aliases, Codex `config.toml`, troubleshooting.

Official docs: [Setup Kerno MCP](https://kerno.gitbook.io/docs/getting-started/quickstart)

## Before you start

**Prerequisites** (stop and tell the user if any are missing):

- Node.js ≥ 18 and `npm` on PATH
- Docker running
- Target project is a **git repository**
- A Kerno account (https://kerno.io)
- An MCP-capable assistant host (IDE, CLI agent, etc.)

**Workspace:** Set `WORKSPACE` once — the absolute path passed to `kerno init -w`. Use the **current project root** unless the user specifies another path. Pass the same path as `workspace_path` on every MCP call.

> **Port ≠ workspace ready.** Always run `kerno init -w "$WORKSPACE"` before MCP registration — never skip because some port is already listening.

> **Single-workspace rebind.** The agent binds to one workspace at a time, and `kerno init` runs headless automatically in agent shells. To point Kerno at a *different* workspace, either run `kerno stop` then `kerno init -w "$WORKSPACE"` (graceful — cancels the old workspace's in-flight work first), or `kerno init -w "$WORKSPACE" --force-switch` (stops and switches without a prompt). A plain `kerno init -w` at a new workspace exits with guidance instead of switching. See **`mcp-client-config.md`** § Single-workspace rebind.

**Parallel preflight:** `kerno --version`, `docker info`, confirm `$WORKSPACE` is a git repo, scan existing MCP configs for duplicate Kerno entries.

## Checklist

Work in order. Pause at **(user)** checkpoints. Report progress briefly (✓ / ✗ / pending).

- [ ] **Install CLI** — `npm install -g @kerno/cli` then `kerno --version`
- [ ] **Login** — `kerno login` **(user)** on fresh machines
- [ ] **Start agent + discover MCP URL** — `kerno init -w "$WORKSPACE"`; parse **`MCP_URL`** per **`mcp-client-config.md`**
- [ ] **Workspace gate** — agent started; workspace line matches `$WORKSPACE`; **`MCP_URL`** known
- [ ] **Ask host** **(user)** — which assistant or IDE; never infer from the current session
- [ ] **Ask MCP scope** **(user)** — project/repo vs user/machine; never assume
- [ ] **Register MCP** — merge parsed **`MCP_URL`** per **`mcp-client-config.md`**; only after workspace gate + host + scope chosen
- [ ] **Resolve server id** — from host tool descriptors before calling tools
- [ ] **Refresh host** **(user)** — only if Kerno tools are not visible yet
- [ ] **Verify (Tier C)** — `kerno_get_applications(workspace_path: "$WORKSPACE")` via MCP
- [ ] **Hand off** — workspace reminder + next actions **(user)**

**Completion:** Tier C — `kerno_get_applications` succeeds once the host sees Kerno tools.

**Must not during bootstrap:** hardcode an MCP URL without reading CLI output; run multiple `kerno init` invocations in parallel; register MCP before the workspace gate passes.

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
kerno init -w "$WORKSPACE"
```

First run may download the agent runtime. Read the **full command output**, then parse **`MCP_URL`** and confirm the workspace gate — follow **`mcp-client-config.md`** § Parse `MCP_URL` from CLI output.

## Phase 4 — Register MCP

1. Confirm workspace gate and **`MCP_URL`**
2. **Ask host** **(user)** — wait for an explicit answer
3. **Ask scope** **(user)** — project/repo vs user/machine
4. Register per **`mcp-client-config.md`** § Register with your MCP host (merge; do not overwrite unrelated servers)
5. Resolve MCP server id from host descriptors
6. If tools not visible → user refreshes the host **(user)**

**Codex:** install the plugin first via [codex/README.md](codex/README.md) if skills are missing. Project trust and `[mcp_servers.kerno]` — **`mcp-client-config.md`** § Codex.

## Phase 5 — Verify

Call **`kerno_get_applications`** with `workspace_path: "$WORKSPACE"`. Save `workspace_id` and supported apps.

If healthcheck fails with a schema error but applications work, treat MCP as connected.

## After install — tell the user

Once Tier C passes, say plainly that Kerno is connected. Include:

1. **Use your assistant in this workspace** — Kerno is bound to `$WORKSPACE`. Open your MCP host **inside that folder** (same absolute path).

2. **Apps found** — summarize supported apps; mention unsupported if any.

3. **Next steps** — ask what they want to do:

   > What would you like to do next?
   > - **Set up your environment** — `/kerno-env` or **`kerno-environment-setup`** skill
   > - **Search endpoints** — `kerno_list_endpoints` with required **`scope`**
   > - **Run endpoint tests** — `/kerno-endpoint-test` or **`kerno-endpoint-test`** skill
   > - **Stop here** — MCP is connected; nothing else for now

4. If multiple supported apps, ask which app to work with. If one app, confirm it. If zero, explain what Kerno found and stop.

**Hand off:** Load the chosen skill from `skills/` — do not continue from this skill.

## Agent-safe checks

Do not rely on `kerno status` in agent shells (Ink TUI fails). Use **`kerno --version`**, **`docker info`**, **`kerno init -w "$WORKSPACE"`**, and **`kerno_get_applications`**.
