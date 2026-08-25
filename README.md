# SecondCycle API

Backend for SecondCycle — a Romanian consignment platform that buys used
bikes, repairs them, and sells them with papers and a 12-month warranty.
SecondCycle is legally the **seller** (Romanian consignment, Cod civil
art. 2054), not a marketplace.

FastAPI · async SQLAlchemy 2.0 · Postgres (Neon) · Alembic · Cloudflare R2 ·
Resend · deployed on Fly.io. Managed with `uv`.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- A Postgres database (Neon in production; Docker locally — see below)

## Setup

```bash
uv sync
cp .env.example .env   # then fill in the values
```

### The Neon pooled-vs-direct URL rule (important)

Neon's **pooled** connection string runs PgBouncer in transaction mode, which
is incompatible with asyncpg's prepared-statement cache. Therefore:

- `DATABASE_URL` — the **pooled** URL. Used by the app. The engine sets
  `statement_cache_size=0` to make asyncpg safe under PgBouncer.
- `DATABASE_URL_DIRECT` — the **direct (unpooled)** URL. Used **only** by
  Alembic migrations (`migrations/env.py`). Never run migrations through the
  pooler.

Both use the asyncpg driver:
`postgresql+asyncpg://USER:PASSWORD@HOST/DB?sslmode=require`.

## Running

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Health check: `GET /v1/health`. Interactive docs: `/v1/docs`.

## Migrations

```bash
# create a revision after changing models
uv run alembic revision --autogenerate -m "message"

# apply
uv run alembic upgrade head

# roll back one
uv run alembic downgrade -1
```

Alembic reads `DATABASE_URL_DIRECT` from the environment.

## Quality gates

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

## Project layout

```
app/
  config.py          # pydantic-settings, all env vars
  db.py              # async engine (pooled, statement_cache_size=0) + session
  main.py            # app factory: CORS, security headers, request-id, routers
  core/              # ids (uuid7), logging, middleware, rate limiting
  models/            # SQLAlchemy models
  schemas/           # Pydantic request/response models
  routers/           # thin HTTP routers
  services/          # business logic
  emails/            # email templates
migrations/          # Alembic
tests/               # pytest + httpx + testcontainers Postgres
```

## Not in scope (MVP)

No payment execution / Stripe, no invoicing / e-Factura, no websockets/SSE,
no workshop logins, no admin UI, no multi-language, no PDF generation.
