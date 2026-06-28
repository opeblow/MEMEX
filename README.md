# MEMEX

> The Operating System for Artificial Memory.

[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Cognee](https://img.shields.io/badge/Cognee-Memory%20Engine-purple)](https://github.com/topoteretes/cognee)
[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)

---

## Vision

Memory is the missing layer of the AI stack.

Every AI assistant today starts each conversation from zero. Every agent forgets everything between sessions. Every team rebuilds context. Every insight is lost.

**MEMEX changes this permanently.**

Any AI — whether a coding assistant, a research agent, a customer support bot, or a personal AI — should have access to a persistent, evolving, queryable memory across its entire lifetime. Memory should not be a list of chat logs. Memory should be a living knowledge graph that grows, connects, strengthens, and prunes itself over time.

MEMEX is to AI memory what GitHub is to code, what Notion is to documents, what Figma is to design. It is the **operating system** — the foundational layer — upon which all memory-aware AI applications are built.

---

## Problem

Every AI system today suffers from the same fundamental flaw: **amnesia**.

| Problem | Impact |
|---|---|
| **Stateless conversations** | Every session starts from zero. No continuity. |
| **Flat chat logs** | No structure, no relationships, no evolution. |
| **No long-term memory** | Insights from last week are gone. |
| **No cross-session learning** | Agents never get smarter. |
| **No shared memory** | Teams repeat work. |
| **No memory visualization** | You can't explore what you can't see. |

The result: AI assistants are useful but forgettable. They can't build on past knowledge, learn from feedback, or connect related ideas across time.

---

## Solution

MEMEX is a **cinematic operating system for artificial memory** — a persistent, evolving, queryable memory infrastructure for AI agents and their human collaborators.

Built on five core pillars:

```
┌─────────────────────────────────────────────────────┐
│                    MEMEX                             │
│                                                      │
│   REMEMBER  →  RECALL  →  IMPROVE  →  FORGET        │
│                                                      │
│                  VISUALIZE                           │
└─────────────────────────────────────────────────────┘
```

### Five Pillars

| Pillar | Description |
|---|---|
| **REMEMBER** | Ingest anything — text, files, code, URLs, conversations — into a structured knowledge graph |
| **RECALL** | Retrieve memories through natural language, semantic search, and graph traversal |
| **IMPROVE** | Memory that evolves — deduplication, relationship strengthening, summarization |
| **FORGET** | Intentional lifecycle management — archive, expire, delete |
| **VISUALIZE** | Explore memory as a 3D universe of celestial bodies and galactic clusters |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  Next.js 15 │  │  Three.js   │  │   Framer Motion      │ │
│  │  App Router │  │  3D Memory  │  │   GSAP Animations    │ │
│  │  React 19   │  │  Universe   │  │   Lenis Scroll       │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘ │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │ REST + SSE                        │
└──────────────────────────┼───────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────┐
│                    API GATEWAY (FastAPI)                     │
│                          │                                   │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Auth  │  Memory  │  Graph  │  Agents  │  Projects     ││
│  └────────┼──────────┼────────┼──────────┼────────────────┘│
│           │          │        │          │                   │
│           ▼          ▼        ▼          ▼                   │
│  ┌──────────────────────────────────────────────────────────┐│
│  │              Memory Orchestration Service                ││
│  │  Remember() │ Recall() │ Improve() │ Forget()           ││
│  └────────────────────────┬─────────────────────────────────┘│
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    COGNEE ENGINE (SDK)                       │
│                           │                                  │
│    ┌──────────────────────────────────────────────────┐     │
│    │   Graph Store    │   Vector Store   │   Relational│     │
│    │   (Knowledge     │   (pgvector)     │   Store     │     │
│    │    Graph)        │                  │   (Metadata) │     │
│    └────────┬─────────┴────────┬────────┴──────┬───────┘     │
│             │                  │               │             │
└─────────────┼──────────────────┼───────────────┼─────────────┘
              │                  │               │
        ┌─────▼──────────────────▼───────────────▼─────┐
        │            PostgreSQL 16 + pgvector           │
        │         (Single DB: Graph + Vector + SQL)     │
        └───────────────────────────────────────────────┘
```

### Memory Lifecycle

```
  SOURCE DATA ──► REMEMBER ──► IMPROVE ──► RECALL ──► FORGET
                     │            │           │           │
                     ▼            ▼           ▼           ▼
              Chunk & Embed   Deduplicate   Semantic    Archive/
              Extract Entities Strengthen   Search      Delete
              Store Graph     Summarize     Graph       Expire
              Store Vectors   Build Context Traversal
```

A complete walkthrough:

1. **REMEMBER** — Data enters through ingestion (text input, file upload, URL import, API). Cognee chunks the content, extracts entities, generates embeddings, and stores everything across relational, vector, and graph stores.

2. **IMPROVE** — Automatically triggered after ingestion. Cognee merges duplicate entities, strengthens relationships between connected concepts, summarizes repeated patterns, and applies feedback weights to prioritize important memories.

3. **RECALL** — A query arrives. Cognee auto-routes it to the appropriate retrieval strategy (vector search, graph traversal, or both). Retrieved context is ranked and scored, then passed to an LLM for answer generation with source attribution.

4. **FORGET** — Memories expire based on TTL, are archived on user request, or are permanently deleted across all three stores. Shared nodes are preserved if referenced by other memories.

5. **VISUALIZE** — The 3D Memory Universe renders every memory as a celestial body. Orbit radius = semantic distance, galaxy clusters = knowledge clusters, brightness = importance, color = content type, trails = access patterns.

---

## Cognee Integration

MEMEX is built on **[Cognee](https://github.com/topoteretes/cognee)**, the open-source AI memory platform that combines relational, vector, and graph storage into a unified memory engine.

| Cognee Feature | How MEMEX Uses It |
|---|---|
| **`cognee.remember()`** | Ingestion pipeline — chunk, extract entities, embed, store |
| **`cognee.recall()`** | Multi-strategy retrieval — vector search + graph traversal |
| **`cognee.improve()`** | Post-ingestion enrichment — dedup, summarize, strengthen |
| **`cognee.forget()`** | Lifecycle management — delete from all stores |
| **Graph store** | Knowledge graph for entity/relationship queries |
| **Vector store** | Semantic search with pgvector |
| **Session cache** | Short-term conversational context in PostgreSQL |
| **Auto-routing** | Query classification to optimal retrieval strategy |
| **Self-improvement** | Automatic improve() after every remember() |

Cognee is imported as a **Python library** (not a microservice), giving MEMEX low-latency access to the full memory API surface without network overhead.

---

## Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| **Next.js 15** (App Router) | React framework with server components |
| **React 19** | UI library |
| **TypeScript 5.6** | Type safety |
| **Three.js** + **React Three Fiber** | 3D Memory Universe visualization |
| **Framer Motion 11** + **GSAP 3** | Animations and transitions |
| **Lenis** | Smooth scrolling |
| **TanStack React Query 5** | Server state management |
| **Zustand 5** | Client state management |
| **Zod** + **React Hook Form** | Form validation |
| **Tailwind CSS 4** | Styling |
| **Radix UI** | Accessible primitives |
| **Lucide React** | Icons |

### Backend

| Technology | Purpose |
|---|---|
| **FastAPI** | Python web framework |
| **Python 3.12+** | Runtime |
| **Cognee** | AI memory engine (graph + vector + relational) |
| **SQLAlchemy** (async) | ORM |
| **Alembic** | Database migrations |
| **PostgreSQL 16** + **pgvector** | Primary database |
| **OpenAI** (GPT-4o + text-embedding-3-small) | LLM and embeddings |
| **structlog** | Structured logging |

### Infrastructure

| Technology | Purpose |
|---|---|
| **Turborepo 2.3** | Monorepo orchestration |
| **pnpm 9** | Package manager |
| **Docker** | Containerization |
| **Biome** | Linting and formatting |
| **Vitest** / **Pytest** | Testing |
| **Playwright** | E2E testing |
| **GitHub Actions** | CI/CD |

---

## Local Setup

### Prerequisites

- Node.js 20+
- Python 3.12+
- pnpm 9+
- Docker Desktop (for PostgreSQL)
- OpenAI API key

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/memex.git
cd memex

# Install frontend dependencies
pnpm install

# Set up Python virtual environment
cd apps/api
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt

# Configure environment
cd ../..
cp .env.example .env
# Edit .env with your credentials (JWT_SECRET, OPENAI_API_KEY, etc.)

# Start infrastructure (PostgreSQL)
docker compose -f docker/docker-compose.yml up -d

# Run database migrations
pnpm db:migrate

# Start development servers
# Terminal 1: API
cd apps/api
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
pnpm dev
```

The frontend will be available at **http://localhost:3000** and the API at **http://localhost:8000**.

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret for JWT signing |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `GOOGLE_CLIENT_ID` | No | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | Google OAuth client secret |
| `RESEND_API_KEY` | No | Email delivery (Resend) |
| `COGNEE_API_KEY` | No | Cognee API key |
| `COGNEE_URL` | No | Cognee service URL |

---

## Deployment

### Docker (Production)

```bash
# Build and start all services
docker compose -f docker/docker-compose.yml up --build -d

# Run migrations
docker exec memex-api alembic upgrade head
```

### Infrastructure Requirements

- PostgreSQL 16 with pgvector extension
- Python 3.12+ runtime
- Node.js 20+ runtime

### Production Checklist

- [ ] Set strong `JWT_SECRET` (64+ char random string)
- [ ] Configure `DATABASE_URL` with production credentials
- [ ] Set `OPENAI_API_KEY` for embeddings and LLM
- [ ] Enable HTTPS (reverse proxy or platform TLS)
- [ ] Set `NODE_ENV=production`
- [ ] Configure CORS `allowed_origins` for your domain
- [ ] Set up database connection pooling
- [ ] Configure logging aggregation
- [ ] Set up monitoring and alerting

---

## Screenshots

<!-- 
Screenshots will be added here after capture.
Recommended captures:

1. Landing Page — Hero section with neural background animation
2. Memory Universe — 3D view with celestial memory bodies
3. Recall Interface — Semantic search with graph results
4. Memory Detail — Deep dive into a single memory node
5. Knowledge Graph — Entity and relationship visualization
6. Timeline View — Temporal event browsing
7. Ingest Interface — File upload and text input
8. AI Chat — Reasoning with memory context
-->

| View | Preview |
|---|---|
| **Landing** | ![Landing](docs/screenshots/landing.png) |
| **Memory Universe** | ![Universe](docs/screenshots/universe.png) |
| **Recall** | ![Recall](docs/screenshots/recall.png) |
| **Knowledge Graph** | ![Graph](docs/screenshots/graph.png) |
| **Memory Detail** | ![Detail](docs/screenshots/detail.png) |

### Animation Previews

| Component | Description |
|---|---|
| **Loader** | Cinematic logo reveal with particle burst |
| **Neural Background** | Real-time neural network simulation |
| **Memory Universe** | Orbiting celestial bodies with gravity |
| **Page Transitions** | Smooth route transitions with Framer Motion |
| **Timeline** | Animated time-series event flow |

---

## Future Roadmap

### Phase 2 (Post-Hackathon)

| Feature | Description |
|---|---|
| **Memory Sharing** | Share specific memories or clusters with teams |
| **Agent SDK** | Python/JS SDK for AI agents |
| **Browser Extension** | One-click memory capture from any web page |
| **Slack Integration** | Auto-remember Slack conversations |
| **GitHub Integration** | Sync issues, PRs, and decisions |
| **VS Code Extension** | Remember coding context and decisions |

### Phase 3 (Post-Launch)

| Feature | Description |
|---|---|
| **Memory Templates** | Pre-built schemas for common use cases |
| **Collaborative Graph** | Real-time multi-user memory exploration |
| **Memory Time Machine** | Browse memory state at any point in time |
| **AI Memory Analyst** | Proactive insight surfacing |
| **Enterprise SSO** | SAML, OIDC, SCIM |
| **Custom Embeddings** | Fine-tuned on domain vocabulary |

---

## Project Structure

```
memex/
├── apps/
│   ├── web/              # Next.js frontend
│   │   ├── src/app/      # App Router pages
│   │   └── src/components/ # React components
│   └── api/              # FastAPI backend
│       ├── app/api/      # API routes
│       ├── app/core/     # Business logic
│       ├── app/models/   # SQLAlchemy models
│       └── app/services/ # Service layer
├── packages/
│   ├── ui/               # Design system
│   ├── types/            # TypeScript types
│   ├── hooks/            # React hooks
│   ├── animations/       # Animation primitives
│   └── config/           # Shared configuration
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.web
│   └── docker-compose.yml
├── ARCHITECTURE.md       # Full architecture document
└── README.md             # This file
```

---

## API Overview

The API serves **26+ endpoints** under `/api/v1/memex/`:

| Category | Endpoints |
|---|---|
| **Auth** | Login, register, verify email, reset password, OAuth, refresh |
| **Memory** | Remember, recall (SSE stream), improve, forget |
| **Graph** | Snapshots, neighborhood queries, clusters, timeline |
| **Agents** | CRUD agents, workflows, tasks, decisions, handoffs |
| **Projects** | CRUD projects and workspaces |
| **Analytics** | Usage stats, memory insights |
| **Import** | File upload, URL import, GitHub sync, SSE progress |

---

## License

Proprietary — All rights reserved.

---

Built with [Cognee](https://github.com/topoteretes/cognee) — the open-source AI memory engine.
