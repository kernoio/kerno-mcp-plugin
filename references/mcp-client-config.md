# MCP client configuration (Kerno)

## URL

- **Streamable HTTP:** `POST http://127.0.0.1:<PORT>/mcp` when MCP shares the main agent port.
- **Dedicated MCP port:** If `MCP_PORT` is set and differs from `PORT`, use `http://127.0.0.1:<MCP_PORT>/mcp` for MCP only.

Replace host if the agent runs remotely.

## Server identity

The MCP server advertises the name **`kerno-aicore-agent`**. Clients may show tools with a prefix; map them to the `kerno_*` tool names in the agent.

## Sentry Insights (MCP Resources table)

Sentry’s **MCP Resources** UI groups by **resource URI** (`mcp.server` spans with **`mcp.resource.uri`**). That is **not** the same dimension as MCP **tool** names. Kerno registers **tools** only (no MCP **resources** in the current agent). See **[sentry-insights-mcp.md](sentry-insights-mcp.md)** for the distinction and the canonical **`kerno_*`** list.

## Environment (operator)

Typical variables (see `AgentConfig` in the main repo):

- `ENABLE_MCP=true`
- `WORKSPACE` — absolute path to workspace root
- `PORT` — main HTTP port (default 8086)
- `MCP_PORT` — optional dedicated MCP port

## JSON example (illustrative)

Clients vary; use your product’s MCP config format. The plugin root includes [`mcp.json`](../mcp.json) with the same shape:

```json
{
  "mcpServers": {
    "kerno": {
      "url": "http://127.0.0.1:8086/mcp"
    }
  }
}
```

Some clients use `type: "http"` or SSE variants—match the transport your client supports for **Streamable HTTP** to `POST /mcp`.

## Smoke

Send JSON-RPC `initialize` with:

- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`

## Timeouts and long jobs

**Per-tool-call limit is usually on the MCP host (client),** not the agent. Many hosts end a single tool HTTP round-trip around **~60 seconds**, regardless of how long the server would otherwise wait. **`kerno_job`** cannot rely on one blocking call lasting through a **15+ minute** `kerno_start_environment`; jobs often run **many minutes** and may **exceed 15 minutes**.

**`MCP_TIMEOUT`** in Claude Code applies to **MCP server startup**, not how long an individual tool call may run.

**Practical pattern:** use **`kerno_job`** with **`wait=false`** and check again **every few minutes**, or read **`log_path`**. **Do not** invoke **`kerno_job`** in a **tight loop**—each call costs tokens.

Server-side SDK or Ktor timeouts **do not** override the host’s per-tool-call behavior for MCP tools.
