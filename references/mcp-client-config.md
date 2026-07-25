# MCP client configuration (Kerno)

Single reference for connecting an MCP host to Kerno — CLI install, host registration, operator setup, and client limits.

For the full install procedure, use **`/install-kerno`** (`skills/install-kerno/SKILL.md`). Read sections below as needed.

---

## Install (CLI)

Install and start via **`@kerno/cli`**:

```bash
npm install -g @kerno/cli
kerno login
kerno init -w /absolute/path/to/your/repo
```

Read the **full command output** before proposing MCP config. The port is **session-specific** — never copy a port from docs or old config.

### Parse `MCP_URL` from CLI output

The agent listens on **loopback** at a URL ending in `/mcp`. Prefer, in order:

1. A full URL in a printed registration snippet (`http://127.0.0.1:<port>/mcp` or `http://localhost:<port>/mcp`)
2. A line like `MCP server running on port <N>` → `http://127.0.0.1:<N>/mcp`

Also confirm: **Agent started successfully** and the **Workspace** line matches the absolute path you passed to `-w`.

If the port changes after restart, re-parse and update host config.

### Register with your MCP host

Read this section **after** the user names their host. Do not assume a host from the current session.

1. Run `kerno init -w "$WORKSPACE"` and parse `MCP_URL`.
2. Find the host's MCP config location or CLI for the chosen scope (project/repo vs user/machine).
3. Merge the server entry below; do not overwrite unrelated servers.
4. Add transport/type fields only if the host rejects url-only config.
5. Refresh or reconnect the host if tools are not visible.
6. Resolve the MCP server id from the host's tool descriptors before calling tools.

```json
{
  "mcpServers": {
    "kerno": {
      "type": "http",
      "url": "<MCP_URL from CLI output>"
    }
  }
}
```

The CLI may print ready-made snippets for common hosts — prefer those when the user chose that host, after confirming scope.

**Server id:** parent folder name of `kerno_get_applications.json` in the host's MCP descriptor tree.

#### Scope aliases

| User says | Means |
|-----------|-------|
| global, user-level, machine-wide, machine | User/machine scope |
| project, repo, workspace | Project/repo scope |

Register at **exactly one** scope per setup. If Kerno exists at the other scope, tell the user and remove only with explicit approval.

#### Host examples

Substitute **`MCP_URL`** everywhere.

| Host | Project/repo scope | User/machine scope | Refresh if tools missing |
|------|-------------------|--------------------|----------------------------|
| **Cursor** | `<workspace>/.cursor/mcp.json` | `~/.cursor/mcp.json` | Reload window |
| **Claude Code** | `claude mcp add --transport http kerno --scope project <MCP_URL>` | `claude mcp add --transport http kerno --scope local <MCP_URL>` | Restart or reopen in project |
| **Codex / OpenCode / Gemini CLI** | Follow host MCP docs for workspace config | Follow host MCP docs for user config | Per host docs |
| **Other** | Ask user | Ask user | Follow host MCP docs |

Some hosts require extra JSON fields (`transport`, `type`, etc.) — add only what that host's docs specify.

#### Codex (`config.toml`)

Project-scoped MCP lives in `.codex/config.toml` at the repo root. Codex loads it only when the project is trusted in `~/.codex/config.toml`:

```toml
[projects."/absolute/path/to/your/repo"]
trust_level = "trusted"
```

Register Kerno with the parsed **`MCP_URL`** (substitute `<port>` from CLI output):

```toml
[mcp_servers.kerno]
url = "http://127.0.0.1:<port>/mcp"
enabled = true
```

User-scoped: put the same `[mcp_servers.kerno]` block in `~/.codex/config.toml` instead.

**Plugin install:** see [codex/README.md](../codex/README.md) for the marketplace install. The plugin may ship a bundled [`mcp.json.example`](../mcp.json.example) template; still update the URL after `kerno init -w` because the port is session-specific.

**Plugin MCP policy** (optional, after install): `~/.codex/config.toml` may include `[plugins."kerno@kerno".mcp_servers.kerno]` — see [Codex plugin MCP docs](https://developers.openai.com/codex/plugins/build).

#### Install troubleshooting

| Symptom | Action |
|---------|--------|
| MCP fails but something is listening | Re-run `kerno init -w "$WORKSPACE"`, re-parse `MCP_URL`, update config if port changed |
| Tools not visible after register | Confirm config uses current `MCP_URL`, refresh host |
| `workspace not found` | Same absolute path in `kerno init -w` and every MCP call |
| Two Kerno entries | Duplicate at project + user scope — ask which to keep |
| Wrong workspace bound / agent won't rebind | `kerno stop`, then re-run `kerno init -w "$WORKSPACE"` alone (escalate to `kerno doctor --clean` if orphan/inconsistent state persists) |
| Stale URL in config | Re-parse from fresh CLI output |

#### CLI maintenance

| Action | Command |
|--------|---------|
| Stop | `kerno stop` |
| Re-bind + refresh URL | `kerno init -w "$WORKSPACE"` |
| Logs (user terminal) | `kerno logs` |
| Sign out | `kerno logout` |

#### Single-workspace rebind

The agent binds to **one workspace at a time** — binding a new workspace tears down the previously bound agent. In an agent shell (no TTY), `kerno init` runs **headless automatically**.

To point Kerno at a different workspace non-interactively:

- **Graceful (preferred when the old workspace has work running):** `kerno stop`, then `kerno init -w "$WORKSPACE"`. `kerno stop` cancels the old workspace's in-flight tests and stops its app services before shutting the agent down.
- **One-shot:** `kerno init -w "$WORKSPACE" --force-switch` — stops the other-workspace agent and switches without a prompt. This only kills the old agent process; it does **not** gracefully cancel its in-flight work.

Without `--force-switch`, a headless `kerno init` targeting a different workspace exits with a clear message to `kerno stop` first or re-run with `--force-switch` — it does not hang or crash.

**Session drops on rebind.** Any agent stop, restart, or workspace switch invalidates the host's current MCP session, independent of whether the port changes. Symptom: tool calls return `Unknown session` (or the host shows the server disconnected) right after a rebind. Fix: re-parse `MCP_URL` from the new `kerno init` output, update host config if the port changed, and reconnect/refresh the host. Expect this whenever you switch workspaces mid-session — it is not an error state.

---

## Connection (advanced / self-hosted)

For running the **Kerno agent** directly (dev or custom deploy), not via `@kerno/cli`:

- **Streamable HTTP:** `POST http://127.0.0.1:<PORT>/mcp` when MCP shares the main agent port.
- **Dedicated MCP port:** If `MCP_PORT` differs from `PORT`, use `http://127.0.0.1:<MCP_PORT>/mcp`.
- **Docs default:** often port 8086 — treat as documentation only when using the CLI path above.

Replace host if the agent runs remotely.

## Server identity

The MCP server advertises the name **`kerno-aicore-agent`**. Clients may show tools with a prefix; map them to the `kerno_*` tool names in the agent.

## Tools vs MCP resources (observability)

Some telemetry or MCP UIs may group traffic by **resource URI** or server identity on spans. That is **not** the same dimension as MCP **tool** names. Use the server’s `tools/list` and the **`kerno_*`** names for the canonical tool surface.

The Kerno agent registers **both** tools and MCP **resources**. Current resources:

- **`kerno://guide/<topic>`** — the same content as the **`kerno_guide`** tool (`endpoint_test_intent`, `rules_template`, `env_visibility`, `scenario_philosophy`)
- **`kerno://scenarios/{path}`**
- **`kerno://preconditions/{path}`

## Environment (operator)

Typical variables when running the agent directly (see `AgentConfig` in the main repo):

- `ENABLE_MCP=true`
- `WORKSPACE` — absolute path to workspace root
- `PORT` — main HTTP port (default 8086)
- `MCP_PORT` — optional dedicated MCP port

## Smoke

Send JSON-RPC `initialize` with:

- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`

## Timeouts and long jobs

**Per-tool-call limit is usually on the MCP host (client),** not the agent. Many hosts end a single tool HTTP round-trip around **~60 seconds**, regardless of how long the server would otherwise wait. **`kerno_job`** cannot rely on one blocking call lasting through a **15+ minute** endpoint-test job; jobs often run **many minutes** and may **exceed 15 minutes**.

**`MCP_TIMEOUT`** in some hosts applies to **MCP server startup**, not how long an individual tool call may run.

**Practical pattern:** use **`kerno_job`** with **`wait=false`** and check again **every few minutes**, or read **`log_path`**. **Do not** invoke **`kerno_job`** in a **tight loop**—each call costs tokens.

Server-side SDK or Ktor timeouts **do not** override the host’s per-tool-call behavior for MCP tools.
