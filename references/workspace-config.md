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
  - **`target_environment`** — `local` | `remote` (exact values only)
  - **`sut_url`** — required for `local`/`remote` after the SUT is reachable
  - Optional DB env blocks: `postgres`, `mariadb`, `mysql`, `mongodb`, `redis`, `kafka`, `rabbitmq`, `clickhouse`, `azurite`, `zitadel` — each an object of string env vars for scenario runs. These supply **credentials only**; DB-backed scenarios also require a derivable schema — see [Database access requires a derivable schema](#database-access-requires-a-derivable-schema).

## When to call

After **`kerno_get_applications`**.

Start the stack with the repository's dev flow **first** (or point at a **`remote`** SUT hosted somewhere other than this machine, e.g. cloud), then call **`kerno_save_config`** with **`local`** (or **`remote`**), **`sut_url`**, and — for **greybox** — dependency env vars, then **`kerno_environment_setup`**. Omit the DB env blocks for **black box** (HTTP-only); DB-backed scenarios will then be reported **`[BLOCKED]`**.

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

## Database access requires a derivable schema

Setting a DB env block (above) supplies **credentials only**. A scenario that declares **`requiredDependencies: [database]`** additionally needs Kerno to derive the database **schema** from the repo. If it can't, the scenario is **`[BLOCKED]`** and the DB block alone does nothing.

Detection is deterministic (no LLM) and matches by **filename and path convention, not by ORM/tool**. Recognized:

| Schema source | Matches |
|---------------|---------|
| Prisma | any `*.prisma` (e.g. `schema.prisma`) |
| ActiveRecord snapshot | `schema.rb` (anywhere) |
| Raw SQL snapshot | `schema.sql` (outside a `migration`/`migrate` path) |
| SQL migrations / DDL | `*.sql` under a path containing `migration`, `migrate`, `db/`, `sql/`, or `clickhouse/` — covers Flyway, Liquibase SQL, ClickHouse DDL, plain `db/*.sql` |
| Rails migrations | `db/migrate/*.rb` |
| Digit-prefixed migrations | filename **starting with a digit**, ending in `.sql .rb .ts .mts .js .mjs .py .go .php .exs`, under a `migration`/`migrate` path (or `mongo/`, `mongodb/`) — covers Django, goose, Laravel, Ecto, timestamped TypeORM, migrate-mongo |

Skipped dirs: `node_modules`, `.git`, `build`, `dist`, `vendor`, `.gradle`, `target`. Caps: 60 files, depth 12, 40k chars.

**No ORM-specific detection.** knex, Sequelize, and TypeORM match **only** if their migration files happen to satisfy the digit-prefixed-in-a-migration-path rule. Descriptively-named migrations (e.g. knex's `add-x-column.js`) are **not** recognized and block with:

```
requires direct database access but no schema could be derived from source code
```

### When your schema isn't recognized

1. **Point Kerno at it (interactive).** The blocked run surfaces a free-text feedback question (**`awaiting_answer`**). Answer with **`kerno_feedback_answer`** / **`answer_feedback_request`**, giving a **repo-relative path** to your schema/migration file or directory, or **pasting the DDL**. Kerno saves it to a `derived-schema.md` sidecar and reuses it on later runs. Replying **`skip`** hard-blocks the DB scenarios.
2. **Go API-only.** Drive the endpoint through its HTTP surface instead of direct DB access, supplying any credentials via the dependency env blocks above.

Native knex/Sequelize/TypeORM recognition and a static schema-path config option are tracked in aicore, not this plugin.
