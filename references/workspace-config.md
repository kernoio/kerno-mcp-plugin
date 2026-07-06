# Workspace config (`.kerno/config.yaml`)

Unified MCP persists per-application settings through **`kerno_save_config`**. Config is merged from committed defaults and gitignored local overrides.

## Files

| File | Role |
|------|------|
| `.kerno/default.config.yaml` | Committed template per application |
| `.kerno/config.yaml` | Gitignored local overrides (what **`kerno_save_config`** writes) |

Only **`input-url`** and **`target-environment`** are persisted; effective URLs and reachability are resolved at runtime.

## save_config parameters

Call **`kerno_save_config`** with:

- **`workspace_path`** — absolute path matching agent `WORKSPACE`
- **`applications`** — array of per-app entries:
  - **`app`** — module id or name from **`kerno_get_applications`**
  - **`target_environment`** — `local` | `remote` | `orchestrate` (exact values only)
  - **`sut_url`** — required for `local`/`remote` after the SUT is reachable; omit for `orchestrate`
  - Optional DB env blocks: `postgres`, `mariadb`, `mysql`, `mongodb`, `redis`, `kafka`, `rabbitmq`, `clickhouse`, `azurite`, `zitadel` — each an object of string env vars for scenario runs

## When to call

After **`kerno_get_applications`**.

**Local path** (repo has easy startup): start the stack with the repository's dev flow **first**, then call **`kerno_save_config`** with **`local`**, **`sut_url`**, and dependency env vars, then **`kerno_environment_setup`**.

**Orchestrate path:** call **`kerno_save_config`** with **`target_environment: orchestrate`** (omit **`sut_url`**) when the user explicitly asks Kerno to orchestrate the environment, **or** when the repository has no easy full-stack startup. Then **`kerno_environment_setup`**.

See [target-environment.md](target-environment.md) for the full decision tree.

## Probe behavior

**`kerno_save_config`** probes reachability from inside the **ts-sandbox** network before persisting:

1. Probes the original URL from the agent host
2. Probes gateway candidates from inside ts-sandbox
3. Persists the first sandbox-reachable **`effectiveUrl`**

Failure messages distinguish host vs sandbox reachability.

## Localhost → host gateway

Users often supply `http://localhost:8080`. That works on the **host** but not inside **ts-sandbox** (`localhost` there is the container).

Kerno rewrites localhost URLs to gateway addresses before probing and scenario execution:

| Input | In ts-sandbox |
|-------|---------------|
| `localhost`, `127.0.0.1`, `::1` | Rewritten to gateway candidates |
| `host.docker.internal` | Docker route to host (Desktop / recent Linux) |
| `172.17.0.1` | Default Linux bridge gateway |

Set **`KERNO_HOST_GATEWAY`** when your Docker setup uses a different bridge address (rootless Docker, custom networks, CI).

The saved **`effectiveUrl`** becomes **`SUT_BASE_URL`** for scenario execution; the original **`inputUrl`** is kept for display.

## Optional override at setup

**`kerno_environment_setup`** accepts optional **`sut_url`** to persist before probing for local/remote targets.

See [target-environment.md](target-environment.md) for when to pick each **`target_environment`**.
