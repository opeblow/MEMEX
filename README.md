# MEMEX

> The Operating System for Artificial Memory.

MEMEX is the world's first cinematic operating system for artificial memory. It provides persistent, evolving, queryable memory infrastructure for AI agents and their human collaborators.

## Architecture

This monorepo contains the full MEMEX stack:

| Layer | Tech | Location |
|---|---|---|
| Frontend | Next.js 15 (App Router) + Three.js + Framer Motion | `apps/web/` |
| API | FastAPI (Python) | `apps/api/` |
| Worker | Arq (Redis-backed task queue) | `apps/worker/` |
| Memory Engine | Cognee (graph + vector + relational) | Imported as SDK |
| Shared Packages | TypeScript types, hooks, UI, config | `packages/*` |

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full design document.

## Quick Start

### Prerequisites

- Node.js 22+
- Python 3.12+
- pnpm
- PostgreSQL 16 (with pgvector)
- Redis 7+

### Setup

```bash
# Install frontend dependencies
pnpm install

# Install API dependencies
cd apps/api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start services (PostgreSQL, Redis)
docker compose -f docker/docker-compose.yml up -d

# Start development servers
# Terminal 1: API
cd apps/api
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
pnpm dev
```

## Environment Variables

See `.env.example` for all required variables.

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET` | Secret for JWT token signing |
| `OPENAI_API_KEY` | OpenAI key for embeddings & LLM |
| `RESEND_API_KEY` | Email sending (Resend) |

## Project Structure

```
apps/
  web/          Next.js frontend
  api/          FastAPI backend
packages/
  ui/           Design system components
  hooks/        Shared React hooks
  lib/          API client & utilities
  types/        TypeScript type definitions
  config/       Shared configuration
```

## Available Scripts

```bash
pnpm dev          # Start frontend
pnpm build        # Production build
pnpm lint         # Lint frontend
pnpm typecheck    # TypeScript check
cd apps/api
python -m ruff check app/   # Lint API
```

## API Endpoints

The API serves 26 endpoints under `/api/v1/memex/`:

- **Auth** — login, register, verify email, reset password, OAuth
- **Profile** — get/update user profile
- **Workspaces** — CRUD workspaces and members
- **Projects** — CRUD projects
- **Memory** — remember, recall, improve, forget
- **Graph** — neighborhood queries, clusters, timeline
- **Analytics** — usage stats, insights

## License

Proprietary — All rights reserved.
