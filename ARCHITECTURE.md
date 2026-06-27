# MEMEX — Architecture Document

**Version:** 1.0.0
**Status:** Approved
**Author:** Architecture Team
**Date:** 2026-06-27

---

> "The Operating System for Artificial Memory."

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision](#2-product-vision)
3. [Product Goals](#3-product-goals)
4. [Technical Goals](#4-technical-goals)
5. [Engineering Principles](#5-engineering-principles)
6. [Monorepo Structure](#6-monorepo-structure)
7. [Backend Architecture](#7-backend-architecture)
8. [Frontend Architecture](#8-frontend-architecture)
9. [Cognee Architecture](#9-cognee-architecture)
10. [Memory Lifecycle](#10-memory-lifecycle)
11. [Database Schema](#11-database-schema)
12. [API Specification](#12-api-specification)
13. [Event Flow](#13-event-flow)
14. [AI Flow](#14-ai-flow)
15. [Animation Architecture](#15-animation-architecture)
16. [Security Model](#16-security-model)
17. [Deployment Plan](#17-deployment-plan)
18. [Scaling Plan](#18-scaling-plan)
19. [Future Features](#19-future-features)
20. [Risks](#20-risks)
21. [Technical Decisions](#21-technical-decisions)
22. [Roadmap](#22-roadmap)
23. [Folder Structure](#23-folder-structure)
24. [Development Standards](#24-development-standards)
25. [Coding Standards](#25-coding-standards)
26. [Naming Conventions](#26-naming-conventions)
27. [Acceptance Criteria](#27-acceptance-criteria)

---

## 1. Executive Summary

MEMEX is the world's first cinematic Operating System for Artificial Memory. It provides the memory infrastructure that every AI agent deserves. Instead of storing flat chat logs, MEMEX stores **experience, reasoning, decisions, relationships, evolution, and intelligence** — making every AI assistant capable of remembering forever.

The product is built on five pillars — **Remember, Recall, Improve, Forget, Visualize** — each powered by **Cognee**, the open-source AI memory platform that combines relational, vector, and graph storage into a unified memory engine.

Cognee is the beating heart of MEMEX. Every memory ingested goes through Cognee's ingestion pipeline. Every search traverses Cognee's graph-vector hybrid retrieval. Every improvement pass enriches Cognee's knowledge graph. Every deletion respects Cognee's ownership model.

MEMEX wraps Cognee's raw power in a cinematic, minimal, living interface — designed to feel like entering an artificial brain. No dashboards. No bootstrap. No admin panels. Instead: a Memory Universe where every memory is a celestial body, relationships form constellations, and knowledge clusters evolve into galaxies.

The target audience includes startup founders, AI engineers, software teams, researchers, product managers, and autonomous AI agents who need persistent, structured, evolving memory.

---

## 2. Product Vision

Memory is the missing layer of the AI stack.

Every AI assistant today starts each conversation from zero. Every agent forgets everything between sessions. Every team rebuilds context. Every insight is lost.

MEMEX changes this permanently.

**The vision:** Any AI — whether a coding assistant, a research agent, a customer support bot, or a personal AI — should have access to a persistent, evolving, queryable memory across its entire lifetime. Memory should not be a list of chat logs. Memory should be a living knowledge graph that grows, connects, strengthens, and prunes itself over time.

MEMEX is to AI memory what GitHub is to code, what Notion is to documents, what Figma is to design. It is the **operating system** — the foundational layer — upon which all memory-aware AI applications are built.

---

## 3. Product Goals

| Goal | Description |
|---|---|
| **Universal Ingestion** | Accept any data format — text, files, code, images, audio, video, URLs, GitHub issues, support tickets, meeting transcripts |
| **Semantic Recall** | Find memories through natural language search, graph traversal, and relationship discovery across months or years of history |
| **Continuous Improvement** | Automatically merge similar concepts, generate relationships, strengthen weak links, summarize repeated patterns |
| **Memory Lifecycle Management** | Archive, expire, delete, compress, and version memories so the knowledge graph stays relevant and doesn't grow unbounded |
| **Cinematic Visualization** | Explore memories as a universe — celestial bodies, orbiting related memories, galactic clusters — with smooth camera navigation |
| **Agent-First API** | Expose every capability through REST APIs and a Python SDK so autonomous AI agents can read and write memory programmatically |
| **Multi-Tenant Isolation** | Every user/team gets isolated memory spaces with proper access control |
| **Production-Grade Performance** | 95+ Lighthouse, 60 FPS, sub-100ms recall for common queries, streaming for long responses |

---

## 4. Technical Goals

| Goal | Target |
|---|---|
| **Recall Latency (p50)** | < 200ms for session recall, < 1s for graph recall |
| **Recall Latency (p95)** | < 2s for complex graph traversal |
| **Ingestion Throughput** | > 100 documents/minute per instance |
| **Concurrent Users** | 1,000 per instance, horizontally scalable |
| **Frontend Performance** | 95+ Lighthouse, 60 FPS rendered animations |
| **Uptime** | 99.9% (production) |
| **Memory Graph Size** | 10M+ nodes per tenant with sub-2s recall |
| **Streaming** | Server-sent events for all LLM-powered endpoints |
| **Cold Start** | < 200ms for API, < 2s for frontend |

---

## 5. Engineering Principles

1. **Cognee-first.** Never bypass Cognee. Every memory operation goes through Cognee's SDK or REST API. Our backend is a thin orchestration layer on top of Cognee.

2. **Graph-native thinking.** Memory is not a list. Memory is a graph. Every piece of data is a node. Every connection is an edge. Every query traverses relationships.

3. **Cinematic by default.** Every UI component must earn its place. If it doesn't feel like science fiction, redesign it. No spinners. No skeletons. Only emergence and dissolution.

4. **Minimal surface area.** Each service does one thing well. The monorepo is organized by domain, not by layer. Frontend talks to backend talks to Cognee. No circular dependencies.

5. **Progressive disclosure.** The simplest path (session recall) is instant and zero-config. The most powerful path (custom graph traversal with feedback-weighted ranking) is available with explicit opt-in.

6. **Memory is a first-class citizen.** Every API response includes provenance, confidence, and source attribution. Users and agents can always ask "why?" and get a traceable answer.

7. **Evolve, don't accumulate.** The Improve pillar is not optional. Memory that never improves is a graveyard. Every remember must be followed by improvement.

8. **Own your data.** All embeddings, graph nodes, and metadata are stored in databases we control. No third-party vector stores. No vendor lock-in.

---

## 6. Monorepo Structure

```
memex/
├── apps/
│   ├── web/                      # Next.js frontend application
│   ├── api/                      # FastAPI backend service
│   ├── worker/                   # Background task runner (Celery/Arq)
│   └── docs/                     # Documentation site (Next.js)
│
├── packages/
│   ├── @memex/shared/            # Shared TypeScript types & utilities
│   ├── @memex/config/            # Shared configuration (env, constants)
│   ├── @memex/hooks/             # Shared React hooks
│   ├── @memex/components/        # Shared React components (design system)
│   ├── @memex/lib/               # Shared libraries (API client, auth, utils)
│   ├── @memex/animation/         # Animation primitives (Framer Motion, GSAP, R3F)
│   ├── @memex/memory-graph/      # 3D Memory Universe (Three.js, React Three Fiber)
│   └── @memex/providers/         # React context providers (auth, theme, memory)
│
├── services/
│   ├── cognee/                   # Cognee Python SDK wrapper & configuration
│   ├── memory/                   # Memory orchestration (remember, recall, improve, forget)
│   ├── graph/                    # Graph traversal & visualization data preparation
│   ├── embedding/                # Embedding generation & management
│   ├── search/                   # Multi-strategy search coordination
│   └── auth/                     # Authentication & authorization
│
├── shared/
│   ├── types/                    # TypeScript type definitions (shared between frontend & backend docs)
│   ├── schemas/                  # Pydantic/Zod schemas
│   ├── constants/                # Shared constants
│   └── utils/                    # Shared utilities
│
├── tools/
│   ├── seed/                     # Development data seeding
│   ├── migrate/                  # Database migrations
│   ├── benchmark/                # Performance benchmarking
│   └── scripts/                  # Utility scripts
│
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.web
│   ├── Dockerfile.worker
│   └── docker-compose.yml
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   └── benchmark.yml
│   └── templates/
│
├── config/
│   ├── eslint.config.js
│   ├── tsconfig.base.json
│   ├── tailwind.config.ts
│   └── vitest.config.ts
│
├── ARCHITECTURE.md               # This document
├── README.md
├── package.json                  # Workspace root
├── turbo.json                    # Turborepo configuration
└── pnpm-workspace.yaml
```

---

## 7. Backend Architecture

### 7.1 Service Topology

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Frontend     │────▶│  API Gateway      │────▶│  Auth Service │
│  (Next.js)    │     │  (FastAPI)        │     │  (FastAPI)    │
└──────────────┘     └──────────────────┘     └──────────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Memory Service   │◀────────┐
                    │  (Orchestrator)   │         │
                    └──────────────────┘         │
                           │                      │
              ┌────────────┼────────────┐         │
              ▼            ▼            ▼         │
       ┌──────────┐ ┌──────────┐ ┌──────────┐    │
       │ Cognee   │ │ Cognee   │ │ Cognee   │    │
       │ Remember │ │ Improve  │ │ Recall   │    │
       └──────────┘ └──────────┘ └──────────┘    │
              │            │            │         │
              ▼            ▼            ▼         │
       ┌────────────────────────────────────┐    │
       │         Cognee Engine              │    │
       │  (Graph + Vector + Relational)     │    │
       └────────────────────────────────────┘    │
              │            │            │         │
              ▼            ▼            ▼         │
       ┌──────────┐ ┌──────────┐ ┌──────────┐    │
       │PostgreSQL│ │  Redis   │ │  Object   │    │
       │(primary) │ │ (cache)  │ │  Store    │    │
       └──────────┘ └──────────┘ └──────────┘    │
                                                   │
              ┌────────────────────────────────────┘
              │
              ▼
       ┌──────────────┐
       │ Worker Queue  │
       │  (Arq/Redis)  │
       └──────────────┘
```

### 7.2 Service Descriptions

#### API Gateway (`apps/api/`)
- **Framework:** FastAPI (Python)
- **Role:** Route requests to appropriate services, handle authentication, rate limiting, request validation
- **Endpoints:** All REST endpoints under `/api/v1/memex/*`
- **Thin layer:** No business logic — only routing, auth, and aggregation

#### Memory Service (`services/memory/`)
- **Framework:** Python (FastAPI internal)
- **Role:** Orchestrates the four memory operations by calling Cognee SDK
- **`remember(data, session_id, dataset)`** → calls `cognee.remember()`
- **`recall(query, session_id, datasets)`** → calls `cognee.recall()`
- **`improve(dataset, session_ids)`** → calls `cognee.improve()`
- **`forget(dataset, data_id, everything)`** → calls `cognee.forget()`
- **Handles:** Multi-step pipelines, error recovery, retries, streaming, session management

#### Graph Service (`services/graph/`)
- **Framework:** Python (FastAPI)
- **Role:** Prepares graph data for visualization, handles graph traversal queries for the frontend
- **Endpoints:** Graph snapshots, neighborhood queries, cluster detection, temporal slices
- **Does NOT replace Cognee's graph** — it reads from the same store and formats for the UI

#### Search Service (`services/search/`)
- **Framework:** Python
- **Role:** Coordinates multi-strategy search across Cognee's retrieval modes
- **Handles:** Auto-routing, query classification, result ranking, source attribution
- **May cache** frequent queries in Redis

#### Auth Service (`services/auth/`)
- **Framework:** FastAPI
- **Role:** User registration, login (Google OAuth, email/password), JWT issuance, session management
- **Stores:** Users in PostgreSQL, sessions in Redis (optional)
- **Integration:** Cognee's user context is passed through for dataset ownership

#### Worker (`apps/worker/`)
- **Framework:** Arq (Redis-backed task queue)
- **Role:** Run background tasks — large ingestion, scheduled improve passes, global context indexing, memory maintenance
- **Tasks:** `ingest_document`, `run_improve`, `build_global_context`, `expire_memories`, `compress_graph`

### 7.3 Communication Patterns

| Pattern | Where | Mechanism |
|---|---|---|
| **Synchronous** | Frontend ↔ API | HTTP/1.1 (REST) |
| **Streaming** | API → Frontend | Server-Sent Events (SSE) |
| **Asynchronous** | API → Worker | Redis (Arq queue) |
| **Synchronous** | API → Cognee | Python SDK (in-process call) |
| **Cached** | API ↔ Redis | Redis (JSON, session cache) |
| **Persistent** | Cognee ↔ PostgreSQL | Async SQLAlchemy |

### 7.4 API Boundaries

- **External (Frontend → API):** REST + SSE. All endpoints under `/api/v1/memex/`. Frontend never talks directly to Cognee.
- **Internal (API → Cognee):** Python SDK calls within the same process. Cognee is imported as a library, not a service. This gives us low-latency access to the full API surface.
- **Internal (API → Worker):** Arq tasks for anything that takes > 5 seconds.
- **Internal (API → Redis):** Direct read/write for session cache and rate limiting.

---

## 8. Frontend Architecture

### 8.1 Component Hierarchy

```
<App>
  <Providers>          // AuthProvider, ThemeProvider, MemoryProvider, QueryProvider
    <Layout>
      <Sidebar>        // Minimal, glass-morphism sidebar with primary navigation
      <MainContent>    // Router outlet — renders the active view
      <CommandPalette> // Global Cmd+K search (Raycast/Perplexity style)
      <MemoryBar>     // Persistent "ambient memory" footer showing active recall context
    </Layout>
  </Providers>
</App>
```

### 8.2 Views/Routes (Pages)

| Route | View | Description |
|---|---|---|
| `/` | **Universe** | 3D Memory Universe — the primary landing experience |
| `/recall` | **Recall** | Semantic search with graph results and conversation interface |
| `/remember` | **Ingest** | Memory ingestion — drag-and-drop files, text input, URL import |
| `/memories/:id` | **Memory Detail** | Deep dive into a single memory node with its relationships |
| `/clusters/:id` | **Cluster View** | Explore a knowledge cluster as a galaxy |
| `/graph` | **Graph View** | 2D graph exploration (React Flow with heavy customization) |
| `/settings` | **Settings** | Account, API keys, theme, preferences |
| `/projects` | **Projects** | Multi-project/workspace management |
| `/login` | **Login** | Google OAuth / email authentication |

### 8.3 State Management

| State Type | Mechanism | Details |
|---|---|---|
| **Server State** | TanStack React Query (v5) | All API data, caching, optimistic updates, background refetching |
| **Auth State** | React Context + JWT | Stored in httpOnly cookie, decoded in context for user info |
| **UI State** | Zustand | Theme, sidebar state, active filters, animation preferences |
| **Memory Session** | React Context | Active `session_id`, conversation history, recall context |
| **Graph Cache** | Zustand + IndexedDB | 3D graph node/edge positions, camera state, cluster data |
| **Animation State** | Framer Motion + GSAP | Scroll progress, element visibility, reduced-motion preference |

### 8.4 Providers (ordered)

```
QueryClientProvider        // TanStack React Query
  AuthProvider             // JWT + OAuth state
    ThemeProvider          // Dark mode (always dark), reduced motion
      MemoryProvider       // Active memory session context
        AnimationProvider  // Shared animation timeline coordination
          RouterProvider   // Next.js App Router
```

### 8.5 Caching Strategy

| Layer | Cache | TTL | Invalidation |
|---|---|---|---|
| **React Query** | In-memory | 5 min (recall), 30 min (static) | On mutation, on focus |
| **Redis** | Server-side | 1 min (recall), 1 hour (metadata) | Webhook from worker |
| **CDN** | Edge | 1 hour (static assets) | On deploy |
| **IndexedDB** | Browser (graph tiles) | Persistent | On version change |

### 8.6 Optimistic Updates

- **Remember:** Immediately show the memory in the UI with a "processing" state before the API confirms
- **Forget:** Immediately remove the memory from the UI before the API confirms (rollback on error)
- **Improve:** Show a progress indicator in the MemoryBar rather than blocking the UI
- **Recall:** Show cached results immediately, update with fresh results once available (stale-while-revalidate)

---

## 9. Cognee Architecture

### 9.1 Where Cognee Lives

Cognee is the **engine layer** of MEMEX. It lives at the infrastructure level, directly above the databases and below the memory orchestration service.

```
MEMEX Service Layer
        │
        ▼
Cognee SDK (import cognee)
        │
        ├───► Relational Store (PostgreSQL)
        ├───► Vector Store (PostgreSQL / pgvector)
        ├───► Graph Store (PostgreSQL / AGE or NetworkX)
        └───► Session Cache (Redis)
```

Cognee is NOT a microservice. It is a **Python library** imported directly by the Memory Service. This avoids network overhead for the hot path (remember/recall). The REST API layer in front of Cognee is thin and stateless.

For this architecture, Cognee is configured as follows:

| Cognee Setting | MEMEX Value | Rationale |
|---|---|---|
| **Relational DB** | PostgreSQL 16 | Production-grade, supports all Cognee relational needs |
| **Vector Store** | PostgreSQL (pgvector) | Single-database simplicity, no extra infra |
| **Graph Store** | PostgreSQL (AGE) | Graph operations within PostgreSQL; alternatively uses NetworkX for in-memory speed |
| **Cache Backend** | Redis | Shared, production-grade session cache |
| **Default Embedding** | OpenAI `text-embedding-3-small` | Best quality/cost ratio; configurable |
| **Default LLM** | OpenAI GPT-4o | For graph extraction, summarization, and completion |
| **Chunk Size** | 1024 tokens | Balanced between granularity and LLM context |
| **Self-Improvement** | Enabled (default) | Every `remember()` triggers `improve()` |

### 9.2 What Goes Into Cognee

Cognee stores three layers of data for every memory:

**Relational Store (PostgreSQL — `cognee_*` tables):**
- Datasets (name, id, owner)
- Documents/files (provenance, metadata, source URL)
- Chunks (text, position, document reference)
- DataItems (ingested items with labels and external metadata)
- Pipeline run status and history
- User/ownership records

**Vector Store (PostgreSQL pgvector — `cognee_*` collections):**
- Chunk embeddings (1024-1536 dimensions)
- DataPoint embeddings
- Summary embeddings
- Triplet embeddings (when enabled)

**Graph Store (PostgreSQL AGE or NetworkX):**
- Entity nodes (people, places, concepts, organizations, etc.)
- Relationship edges (connections between entities with type, weight, direction)
- NodeSets (groups/categories of nodes)
- Feedback weights on nodes and edges
- Global context index (bucket summaries, root summaries)

**Session Cache (Redis — `cognee:session:*`):**
- QA entries (question, context, answer, feedback)
- Trace entries (tool calls, reasoning steps)
- Graph context snapshots
- Session metadata (user, created_at, updated_at)

### 9.3 What Stays in PostgreSQL (Outside Cognee)

MEMEX maintains its own application tables alongside Cognee's internal tables:

| Table | Purpose | Relationship to Cognee |
|---|---|---|
| `memex.users` | MEMEX user profiles, preferences, API keys | References Cognee user IDs |
| `memex.projects` | Multi-project/workspace organization | Cognee datasets map to projects |
| `memex.workspaces` | Team collaboration spaces | Groups datasets under a workspace |
| `memex.sessions` | MEMEX session metadata, UI state | Broader than Cognee session cache |
| `memex.events` | Audit log, analytics events | Independent from Cognee |
| `memex.knowledge_clusters` | Cached cluster metadata for visualization | Aggregated from Cognee graph |
| `memex.saved_searches` | User-saved recall configurations | Reference recall() parameters |
| `memex.annotations` | User notes/annotations on memories | Linked to Cognee data IDs |

### 9.4 What Stays in Redis

| Key Pattern | Purpose | TTL |
|---|---|---|
| `memex:session:{userId}:{sessionId}` | Active conversation context | 24h |
| `memex:recall:cache:{queryHash}` | Cached recall results | 60s |
| `memex:rate:limit:{userId}` | Rate limit counters | 1s-1h |
| `memex:ws:{userId}` | WebSocket connection registry | Session |
| `memex:task:{taskId}` | Long-running task status | 24h |
| `cognee:session:*` | Cognee's session cache | Configurable |

### 9.5 How Embeddings Are Generated

1. **Text arrives** via `cognee.remember()` or `POST /api/v1/memex/remember`
2. **Cognee chunks** the text using the configured chunker (1024 tokens default)
3. **For each chunk**, Cognee generates an embedding using the configured embedding model
4. **Cognee stores** the embedding in the vector store (pgvector)
5. **During recall**, the query is embedded using the same model
6. **Vector similarity search** finds the nearest chunks
7. **Graph traversal** supplements with entity/relationship matches
8. **Results are ranked** using a hybrid score (vector distance + graph relevance + feedback weight)

### 9.6 How Recall Is Performed

The recall pipeline follows Cognee's auto-routing default:

1. **Query arrives** → `POST /api/v1/memex/recall` → Memory Service → `cognee.recall()`
2. **Session check** → If `session_id` is provided, search session cache first
3. **Auto-routing** → Cognee classifies the query:
   - Summary prompts → summary retrieval
   - Relationship questions → graph context extension
   - Time-oriented → temporal retrieval
   - Exact phrases → lexical chunk search
   - Default → graph completion
4. **Graph retrieval** (most common path):
   - Embed query → vector search for candidate chunks
   - Expand candidates to graph neighborhood
   - Traverse edges to find related entities
   - Score and rank by relevance + feedback weight
5. **LLM completion** → Retrieved context + query → GPT-4o generates answer
6. **Source tagging** → Each result tagged with `source: "session"`, `"graph"`, or `"graph_context"`
7. **Session write-back** → QA entry appended to session cache

### 9.7 How `improve()` Works

Called automatically after `remember()` (via `self_improvement=True`) or explicitly:

1. **Feedback application** → If sessions have feedback, update `feedback_weight` on graph nodes/edges
2. **Session persistence** → Session QA content cognified into permanent graph
3. **Graph enrichment** → Default pass adds derived retrieval structures:
   - Triplet extraction and indexing
   - Summary generation
   - Relationship strengthening/weakening
4. **Global context index** (optional) → Build bucket summaries and root summary for dataset
5. **Session sync-back** → Write enriched graph context back to session cache

### 9.8 How `forget()` Works

1. **Delete data item** → Removes from relational store, removes associated graph nodes/edges, removes vector embeddings
2. **Delete dataset** → Removes all relational records, all graph nodes/edges, all vectors for that dataset
3. **Delete everything** → Clears all datasets for current user + prunes session cache
4. **Memory-only** (preserve raw files) → Clears graph + vector + resets pipeline status, keeps raw files
5. **Shared node preservation** → If a node is referenced by another document, it's preserved

---

## 10. Memory Lifecycle

```
                         ┌─────────────────────────────┐
                         │        Source Data           │
                         │  (text, file, code, URL,     │
                         │   image, audio, video, etc.) │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     1. REMEMBER (Ingestion)                        │
│                                                                     │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐   │
│   │ Validate  │──▶│  Chunk   │──▶│ Extract  │──▶│  Generate    │   │
│   │ & Normalize│  │          │   │ Entities │   │  Embeddings  │   │
│   └──────────┘   └──────────┘   └──────────┘   └──────────────┘   │
│                                              │                     │
│                                              ▼                     │
│   ┌──────────┐   ┌──────────┐   ┌──────────────────────────┐      │
│   │ Store    │◀──│ Store    │◀──│ Build Graph Relations    │      │
│   │ Vectors  │   │ Chunks   │   │ (entities + edges)       │      │
│   └──────────┘   └──────────┘   └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   2. IMPROVE (Enrichment)                          │
│                                                                     │
│   ┌──────────────────┐   ┌────────────────┐   ┌───────────────┐    │
│   │ Merge Duplicates │──▶│ Strengthen     │──▶│ Summarize     │    │
│   │ (entity dedup)   │   │ Relationships  │   │ Repeated      │    │
│   └──────────────────┘   └────────────────┘   │ Patterns      │    │
│                                                └───────────────┘    │
│   ┌──────────────────┐   ┌────────────────┐                        │
│   │ Apply Feedback   │──▶│ Build Global   │                        │
│   │ Weights          │   │ Context Index  │                        │
│   └──────────────────┘   └────────────────┘                        │
└─────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   3. RECALL (Retrieval)                            │
│                                                                     │
│   ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐   │
│   │ Query    │──▶│ Auto-Route   │──▶│ Vector   │──▶│ Graph    │   │
│   │ Arrives  │   │ (classify)   │   │ Search   │   │ Traverse │   │
│   └──────────┘   └──────────────┘   └──────────┘   └──────────┘   │
│                                                      │             │
│   ┌──────────┐   ┌──────────────┐   ┌──────────────┐ │             │
│   │ Return   │◀──│ Generate     │◀──│ Rank & Score │◀┘             │
│   │ Answer   │   │ LLM Answer   │   │ + Attribution │              │
│   └──────────┘   └──────────────┘   └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   4. FORGET (Lifecycle End)                        │
│                                                                     │
│   ┌──────────────┐   ┌──────────────┐   ┌────────────────────┐     │
│   │ Time-to-Live │──▶│ Mark for     │──▶│ Delete from        │     │
│   │ Expired      │   │ Deletion     │   │ All 3 Stores      │     │
│   └──────────────┘   └──────────────┘   └────────────────────┘     │
│                                                                     │
│   ┌──────────────┐   ┌──────────────┐                              │
│   │ User-Initiated│──▶│ Archive (soft │                              │
│   │ Deletion     │   │ delete)       │                              │
│   └──────────────┘   └──────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   5. VISUALIZE (Exploration)                       │
│                                                                     │
│   Memory Universe ─── Celestial body = memory node                 │
│   ├── Orbit radius = semantic distance                             │
│   ├── Galaxy clusters = knowledge clusters                         │
│   ├── Brightness = importance/recency                              │
│   ├── Color = content type (code, text, image, etc.)               │
│   └── Trails = access patterns / temporal evolution                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11. Database Schema

### 11.1 MEMEX Application Tables (PostgreSQL — `memex` schema)

```sql
-- =============================================
-- USERS
-- =============================================
CREATE TABLE memex.users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cognizant_user_id UUID,              -- Reference to Cognee's internal user ID
    email           VARCHAR(255) UNIQUE NOT NULL,
    display_name    VARCHAR(255),
    avatar_url      TEXT,
    auth_provider   VARCHAR(50) NOT NULL, -- 'google', 'email'
    auth_provider_id VARCHAR(255),        -- Google sub / email hash
    role            VARCHAR(50) DEFAULT 'user', -- 'user', 'admin'
    preferences     JSONB DEFAULT '{}',   -- Theme, reduced_motion, etc.
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    last_login_at   TIMESTAMPTZ
);

-- =============================================
-- WORKSPACES
-- =============================================
CREATE TABLE memex.workspaces (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE NOT NULL,
    description     TEXT,
    owner_id        UUID NOT NULL REFERENCES memex.users(id),
    settings        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- WORKSPACE MEMBERS
-- =============================================
CREATE TABLE memex.workspace_members (
    workspace_id    UUID NOT NULL REFERENCES memex.workspaces(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    role            VARCHAR(50) DEFAULT 'member', -- 'owner', 'admin', 'member', 'viewer'
    joined_at       TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (workspace_id, user_id)
);

-- =============================================
-- PROJECTS
-- =============================================
CREATE TABLE memex.projects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES memex.workspaces(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) NOT NULL,
    description     TEXT,
    cognee_dataset_id UUID,             -- The Cognee dataset backing this project
    settings        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (workspace_id, slug)
);

-- =============================================
-- SESSIONS
-- =============================================
CREATE TABLE memex.sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES memex.projects(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    cognee_session_id VARCHAR(255),     -- Cognee session ID for this session
    title           VARCHAR(255),
    metadata        JSONB DEFAULT '{}',  -- UI state, filters, etc.
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    ended_at        TIMESTAMPTZ
);

-- =============================================
-- MEMORIES (metadata about ingested memories)
-- =============================================
CREATE TABLE memex.memories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES memex.projects(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    session_id      UUID REFERENCES memex.sessions(id) ON DELETE SET NULL,
    cognee_data_id  UUID,               -- Reference to Cognee's data item ID
    cognee_dataset_id UUID,             -- Reference to Cognee's dataset ID
    title           VARCHAR(500),
    memory_type     VARCHAR(50) NOT NULL, -- 'text', 'file', 'code', 'image', 'audio', 'video', 'url', 'conversation', 'meeting_note', 'github_issue', 'support_ticket', 'research', 'decision'
    source          VARCHAR(100),        -- 'direct_input', 'file_upload', 'url', 'github_sync', 'api'
    source_url      TEXT,               -- Original URL if applicable
    file_path       TEXT,               -- Original file path if applicable
    mime_type       VARCHAR(100),
    content_preview TEXT,               -- First 500 chars for display
    size_bytes      BIGINT,
    token_count     INTEGER,
    chunk_count     INTEGER,
    status          VARCHAR(50) DEFAULT 'processing', -- 'processing', 'indexed', 'failed', 'deleted'
    importance      FLOAT DEFAULT 0.5,  -- 0.0 to 1.0, computed by Improve
    tags            TEXT[],              -- User-assigned tags
    metadata        JSONB DEFAULT '{}',  -- Flexible metadata blob
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- KNOWLEDGE CLUSTERS (cached for visualization)
-- =============================================
CREATE TABLE memex.knowledge_clusters (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES memex.projects(id) ON DELETE CASCADE,
    name            VARCHAR(500),
    description     TEXT,
    centroid_embedding VECTOR(1536),    -- Cluster centroid for positioning
    node_count      INTEGER DEFAULT 0,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- EVENTS (audit log + analytics)
-- =============================================
CREATE TABLE memex.events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID REFERENCES memex.projects(id) ON DELETE SET NULL,
    user_id         UUID REFERENCES memex.users(id) ON DELETE SET NULL,
    session_id      UUID REFERENCES memex.sessions(id) ON DELETE SET NULL,
    event_type      VARCHAR(100) NOT NULL, -- 'memory.created', 'memory.recalled', 'memory.deleted', 'session.started', 'session.ended', etc.
    event_data      JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- SAVED SEARCHES
-- =============================================
CREATE TABLE memex.saved_searches (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    project_id      UUID REFERENCES memex.projects(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    query           TEXT NOT NULL,
    filters         JSONB DEFAULT '{}',
    is_shared       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- ANNOTATIONS (user notes on memories)
-- =============================================
CREATE TABLE memex.annotations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    memory_id       UUID NOT NULL REFERENCES memex.memories(id) ON DELETE CASCADE,
    content         TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- API KEYS (for agent access)
-- =============================================
CREATE TABLE memex.api_keys (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES memex.users(id) ON DELETE CASCADE,
    project_id      UUID REFERENCES memex.projects(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    key_hash        VARCHAR(255) NOT NULL, -- bcrypt hash of the raw key
    key_prefix      VARCHAR(8) NOT NULL,   -- First 8 chars for display: 'memex_abc...'
    permissions     JSONB DEFAULT '{}',    -- Scoped permissions
    expires_at      TIMESTAMPTZ,
    last_used_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    is_active       BOOLEAN DEFAULT TRUE
);

-- =============================================
-- INDEXES
-- =============================================
CREATE INDEX idx_memories_project ON memex.memories(project_id);
CREATE INDEX idx_memories_user ON memex.memories(user_id);
CREATE INDEX idx_memories_type ON memex.memories(memory_type);
CREATE INDEX idx_memories_status ON memex.memories(status);
CREATE INDEX idx_memories_created ON memex.memories(created_at DESC);
CREATE INDEX idx_memories_tags ON memex.memories USING GIN(tags);
CREATE INDEX idx_events_project ON memex.events(project_id);
CREATE INDEX idx_events_user ON memex.events(user_id);
CREATE INDEX idx_events_type ON memex.events(event_type);
CREATE INDEX idx_events_created ON memex.events(created_at DESC);
CREATE INDEX idx_sessions_active ON memex.sessions(project_id, user_id) WHERE is_active = TRUE;
```

### 11.2 Cognee Internal Tables (created/managed by Cognee)

Cognee manages its own tables in a separate schema (default: `cognee`). These include:

- `cognee.datasets` — Dataset metadata
- `cognee.data` — Data items (ingested content references)
- `cognee.chunks` — Text chunks with position information
- `cognee.documents` — Document metadata
- `cognee.graph_nodes` — Graph entity nodes
- `cognee.graph_edges` — Graph relationship edges
- `cognee.embeddings` — Vector embeddings (pgvector)
- `cognee.summaries` — Generated summaries
- `cognee.pipeline_runs` — Ingestion pipeline status
- `cognee.user_permissions` — Access control
- `cognee.node_sets` — Node grouping/categorization

We do NOT modify Cognee's internal schema. We interact only through the SDK.

---

## 12. API Specification

### 12.1 Base URL

```
Production:  https://api.memex.sh/api/v1/memex
Local:       http://localhost:8000/api/v1/memex
```

### 12.2 Authentication

All endpoints require a Bearer JWT token (user auth) or API key (agent auth):

```
Authorization: Bearer <jwt_token>
X-Api-Key: <api_key>
```

### 12.3 Standard Responses

```json
// Success
{
  "status": "ok",
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "processing_time_ms": 123
  }
}

// Error
{
  "status": "error",
  "error": {
    "code": "MEMORY_NOT_FOUND",
    "message": "The requested memory was not found or you lack access.",
    "details": { ... }
  },
  "meta": {
    "request_id": "uuid",
    "processing_time_ms": 45
  }
}
```

### 12.4 Endpoints

#### Memory Operations

```
POST   /remember                    # Ingest new memory
POST   /recall                      # Query memory
POST   /improve                     # Trigger improvement pass
POST   /forget                      # Delete memory/data
```

##### `POST /remember`

Ingest data into permanent or session memory. This is the primary ingestion endpoint.

**Request:**
```
Content-Type: multipart/form-data
```

| Field | Type | Required | Description |
|---|---|---|---|
| `data` | string, file, or URL | Yes* | Text content, file upload, or URL. Accepts same types as Cognee `remember()`. |
| `project_id` | UUID | Yes | Target project |
| `session_id` | string | No | Enable session memory mode |
| `memory_type` | string | No | `text`, `file`, `code`, `conversation`, etc. |
| `title` | string | No | Human-readable title |
| `tags` | string[] | No | Array of tags |
| `metadata` | object | No | Arbitrary key-value metadata |
| `run_in_background` | boolean | No | Default: false. Process asynchronously. |
| `chunk_size` | integer | No | Override chunk size (tokens) |

*One of `data` (text), `data` (file upload), or `data` (URL string) required.

**Response (Background=false):**
```json
{
  "status": "ok",
  "data": {
    "memory_id": "uuid",
    "dataset_id": "uuid",
    "chunk_count": 12,
    "token_count": 3456,
    "processing_time_ms": 4200,
    "status": "indexed"
  }
}
```

**Response (Background=true, immediate):**
```json
{
  "status": "ok",
  "data": {
    "memory_id": "uuid",
    "status": "processing",
    "task_id": "uuid"
  }
}
```

##### `POST /recall`

Query memory with auto-routed retrieval.

**Request:**
```json
{
  "query": "What architectural decisions did we make about the database?",
  "project_id": "uuid",
  "session_id": "chat_42",
  "session_only": false,
  "datasets": ["product_docs"],
  "query_type": null,
  "top_k": 15,
  "only_context": false,
  "stream": true
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Natural language query |
| `project_id` | UUID | Yes | Scope to project |
| `session_id` | string | No | Session-aware retrieval |
| `session_only` | boolean | No | Only search session cache |
| `datasets` | string[] | No | Restrict to specific datasets |
| `query_type` | string | No | Override auto-routing: `graph_completion`, `chunks`, `summaries`, `temporal`, etc. |
| `top_k` | integer | No | Max results (default: 15) |
| `only_context` | boolean | No | Return context without LLM answer |
| `stream` | boolean | No | Enable SSE streaming for answer |

**Response (Non-streaming):**
```json
{
  "status": "ok",
  "data": {
    "answer": "We decided to use PostgreSQL with pgvector for the vector store...",
    "sources": [
      {
        "text": "Decision: Use PostgreSQL as primary database for MEMEX...",
        "source": "graph",
        "memory_id": "uuid",
        "chunk_id": "uuid",
        "relevance_score": 0.92,
        "evidence": "Chunk 3 of document 'Architecture Decisions': 'Use PostgreSQL pgvector...'"
      }
    ],
    "processing_time_ms": 845
  }
}
```

**Response (Streaming - SSE):**
```
event: token
data: {"token": "We", "done": false}

event: token
data: {"token": " decided", "done": false}

...

event: done
data: {"token": "", "done": true, "sources": [...], "processing_time_ms": 1200}
```

##### `POST /improve`

Trigger an improvement/enrichment pass on a project's memory.

**Request:**
```json
{
  "project_id": "uuid",
  "session_ids": ["chat_42"],
  "build_global_context_index": true,
  "run_in_background": false
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "project_id": "uuid",
    "datasets_improved": ["product_docs"],
    "nodes_enriched": 234,
    "edges_added": 89,
    "summaries_generated": 12,
    "global_context_built": true,
    "processing_time_ms": 15200
  }
}
```

##### `POST /forget`

Delete memory data.

**Request:**
```json
{
  "project_id": "uuid",
  "data_id": "uuid",
  "dataset": "product_docs",
  "everything": false,
  "memory_only": false
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "deleted_data_ids": ["uuid"],
    "deleted_graph_nodes": 45,
    "deleted_vectors": 12,
    "datasets_affected": 1
  }
}
```

#### Project & Workspace CRUD

```
GET    /projects                    # List user's projects
POST   /projects                    # Create project
GET    /projects/:id                # Get project details
PATCH  /projects/:id                # Update project
DELETE /projects/:id                # Delete project (and Cognee dataset)
GET    /workspaces                  # List workspaces
POST   /workspaces                  # Create workspace
POST   /workspaces/:id/members      # Add member
DELETE /workspaces/:id/members/:uid # Remove member
```

#### Graph & Visualization

```
POST   /graph/neighborhood          # Get graph neighborhood around a memory
POST   /graph/clusters              # Get knowledge clusters for universe view
POST   /graph/timeline              # Get temporal slice of graph
GET    /graph/snapshot/:project     # Get full graph snapshot (for visualization)
```

##### `POST /graph/neighborhood`

```json
{
  "memory_id": "uuid",
  "depth": 2,
  "max_nodes": 100
}
```

**Response:**
```json
{
  "nodes": [
    {"id": "uuid", "label": "PostgreSQL", "type": "technology", "importance": 0.8, "position": {"x": 0, "y": 0, "z": 0}}
  ],
  "edges": [
    {"source": "uuid1", "target": "uuid2", "label": "uses", "weight": 0.9}
  ]
}
```

#### Analytics

```
GET    /analytics/summary/:project  # Memory summary stats
GET    /analytics/activity          # User activity timeline
GET    /analytics/clusters          # Cluster growth over time
```

#### Auth

```
POST   /auth/register               # Email registration
POST   /auth/login                  # Email login
POST   /auth/google                 # Google OAuth
POST   /auth/refresh                # Refresh JWT
POST   /auth/logout                 # Invalidate session
GET    /auth/me                     # Current user info
POST   /auth/api-keys              # Create API key
GET    /auth/api-keys              # List API keys
DELETE /auth/api-keys/:id           # Revoke API key
```

---

## 13. Event Flow

### 13.1 Memory Ingestion Flow

```
User/Frontend                     API Gateway                Memory Service               Cognee                      PostgreSQL/Redis
     │                                │                          │                          │                            │
     │  POST /remember                │                          │                          │                            │
     │───────────────────────────────▶│                          │                          │                            │
     │                                │  Validate + Auth + Rate  │                          │                            │
     │                                │─────────────────────────▶│                          │                            │
     │                                │                          │  cognee.remember(data)    │                            │
     │                                │                          │─────────────────────────▶│                            │
     │                                │                          │                          │  Store chunks             │
     │                                │                          │                          │──────────────────────────▶│
     │                                │                          │                          │  Generate embeddings      │
     │                                │                          │                          │──────────────────────────▶│
     │                                │                          │                          │  Extract entities + edges │
     │                                │                          │                          │──────────────────────────▶│
     │                                │                          │                          │                            │
     │                                │                          │  ◀─ RememberResult ─────│                            │
     │                                │                          │                          │                            │
     │                                │                          │  cognee.improve() (auto) │                            │
     │                                │                          │─────────────────────────▶│                            │
     │                                │                          │                          │  Enrich graph             │
     │                                │                          │                          │──────────────────────────▶│
     │                                │                          │                          │  Build summaries           │
     │                                │                          │─────────────────────────▶│                            │
     │                                │                          │                          │                            │
     │  ◀── 201 Created ────────────│◀── response ─────────────│                          │                            │
     │                                │                          │                          │                            │
     │  Event: memory.created         │                          │                          │                            │
     │───────────────────────────────▶│  (fire & forget)         │                          │                            │
```

### 13.2 Recall Flow (Streaming)

```
Frontend                     API Gateway                Memory Service               Cognee                      PostgreSQL/Redis
   │                              │                          │                          │                            │
   │  POST /recall (stream=true)  │                          │                          │                            │
   │─────────────────────────────▶│                          │                          │                            │
   │                              │  Validate + Auth         │                          │                            │
   │                              │─────────────────────────▶│                          │                            │
   │                              │                          │                          │                            │
   │                              │                          │  Check session cache     │                            │
   │                              │                          │─────────────────────────────────────────────────────▶│
   │                              │                          │  ◀── (cache miss or hit) ───────────────────────────│
   │                              │                          │                          │                            │
   │                              │                          │  cognee.recall(query)    │                            │
   │                              │                          │─────────────────────────▶│                            │
   │                              │                          │                          │  Vector search            │
   │                              │                          │                          │──────────────────────────▶│
   │                              │                          │                          │  Graph traversal          │
   │                              │                          │                          │──────────────────────────▶│
   │                              │                          │                          │  Rank + score             │
   │                              │                          │  ◀── results ───────────│                            │
   │                              │                          │                          │                            │
   │                              │                          │  LLM completion (stream) │                            │
   │  ◀── SSE: token ────────────│◀── SSE: token ──────────│─────────────────────────▶│                            │
   │  ◀── SSE: token ────────────│◀── SSE: token ──────────│   (to OpenAI)            │                            │
   │  ◀── SSE: done + sources ───│◀── SSE: done ───────────│                          │                            │
   │                              │                          │                          │                            │
   │                              │                          │  Write QA to session     │                            │
   │                              │                          │─────────────────────────────────────────────────────▶│
   │                              │                          │                          │                            │
   │  Event: memory.recalled      │                          │                          │                            │
   │─────────────────────────────▶│  (fire & forget)         │                          │                            │
```

### 13.3 Background Improvement Flow

```
Worker Scheduler              Worker Process              Cognee                      PostgreSQL
     │                              │                          │                            │
     │  Every 10 min (or on demand) │                          │                            │
     │─────────────────────────────▶│                          │                            │
     │                              │  Scan for sessions that  │                            │
     │                              │  need graph bridging     │                            │
     │                              │──────────────────────────────────────────────────────▶│
     │                              │  ◀── sessions ───────────────────────────────────────│
     │                              │                          │                            │
     │                              │  cognee.improve(         │                            │
     │                              │    dataset=...,          │                            │
     │                              │    session_ids=...,      │                            │
     │                              │    build_global_index=True│                            │
     │                              │  )                       │                            │
     │                              │─────────────────────────▶│                            │
     │                              │                          │  Enrich graph              │
     │                              │                          │──────────────────────────▶│
     │                              │                          │  Build summaries           │
     │                              │                          │──────────────────────────▶│
     │                              │                          │  Apply feedback weights   │
     │                              │                          │──────────────────────────▶│
     │                              │                          │  Build global context     │
     │                              │                          │──────────────────────────▶│
     │                              │                          │                            │
     │  Event: improve.completed    │                          │                            │
     │─────────────────────────────▶│  (to event bus)          │                            │
```

---

## 14. AI Flow

### 14.1 Prompt Architecture

All LLM interactions go through Cognee's internal LLM gateway. MEMEX does NOT directly call OpenAI. We configure Cognee with our model choices and let Cognee handle prompt construction for:

| Operation | Model | Cognee Prompt | Notes |
|---|---|---|---|
| **Graph Extraction** | GPT-4o | `graph_extraction` | Extracts entities + relationships from chunks |
| **Summarization** | GPT-4o-mini | `summarization` | Generates summaries of chunks/clusters |
| **Graph Completion** | GPT-4o | `graph_completion` | Answer generation with retrieved graph context |
| **Improvement** | GPT-4o-mini | `improvement` | Dedup, merge, strengthen relationships |
| **Global Context** | GPT-4o-mini | `global_context` | Bucket + root summary generation |
| **Query Auto-Routing** | Rule-based | N/A | Cognee's internal classifier (no LLM cost) |

### 14.2 Context Window Strategy

Cognee manages context internally. Our configuration:

| Parameter | Value | Rationale |
|---|---|---|
| Chunk size | 1024 tokens | Balances granularity with LLM context |
| Top-K chunks | 15 | Retrieved candidates before ranking |
| Max context tokens | 8000 | Leave room for query + system prompt in 128k window |
| Neighborhood depth | 2 | Number of graph edges to traverse from candidates |
| Wide search top-K | 50 | Initial candidate pool before narrowing |

### 14.3 Conversation Lifecycle

```
Session Start
    │
    ├──→ Session created (Redis: cognee:session:{user}:{sessionId})
    │
    ├──→ User asks question
    │       │
    │       ├──→ Recall with session_id
    │       ├──→ Session cache searched first
    │       ├──→ Graph retrieved if needed
    │       ├──→ LLM generates answer with:
    │       │       - Recent N turns (session context)
    │       │       - Graph context (if retrieved)
    │       │       - System prompt (project instructions)
    │       │
    │       └──→ QA entry stored in session (Redis)
    │
    ├──→ User provides feedback (thumbs up/down)
    │       └──→ Feedback stored in session entry
    │
    ├──→ Session ends (user closes, timeout, explicit end)
    │       │
    │       ├──→ Improve() bridges session → graph
    │       ├──→ Feedback weights applied to graph nodes
    │       └──→ Session persisted to permanent graph
    │
    └──→ Session marked inactive
```

### 14.4 Streaming Implementation

- Long-running responses (graph completion answers) use Server-Sent Events
- The API Gateway streams tokens as they're received from Cognee/OpenAI
- Frontend renders tokens progressively with a typewriter animation
- A "stop" button allows users to abort mid-generation (abort SSE connection + cancel Cognee task)

### 14.5 Error Handling & Retries

| Failure | Strategy | Retry |
|---|---|---|
| OpenAPI API timeout | Cognee's internal retry (3 attempts, exponential backoff) | Yes |
| Rate limit (429) | Cognee handles, backoff + retry | Yes (up to 5) |
| Empty recall results | Return "No relevant memories found" + suggest rephrasing | No |
| Ingestion failure (corrupt file) | Catch early, return specific error | No |
| Graph query timeout | Fall back to vector-only search | No |
| Redis connection failure | Degrade to local memory (lession session-aware recall) | Background recovery |

---

## 15. Animation Architecture

### 15.1 Philosophy

Nothing appears — everything *emerges*.
Nothing disappears — everything *dissolves*.
Nothing loads — everything *materializes*.
No spinners. No skeleton loaders. Only living transitions.

### 15.2 Animation Layers

| Layer | Technology | Purpose |
|---|---|---|
| **Page Transitions** | Framer Motion (AnimatePresence) | Route changes, layout shifts, content mounting |
| **Micro-interactions** | Framer Motion + CSS transitions | Hover states, button clicks, hover on graph nodes |
| **Scroll** | Lenis | Smooth, fluid scroll with inertia |
| **Memory Universe** | React Three Fiber + Three.js | 3D celestial body rendering, camera orbits, particle systems |
| **Graph Animation** | GSAP + React Flow | Node/edge spring physics, layout transitions |
| **Typewriter** | CSS + JS | Streaming token rendering during recall |
| **Particles** | Three.js (PointsMaterial) | Ambient background particle field |
| **Lottie** | Lottie-web | Complex vector animations (branding, empty states) |
| **SVG** | Framer Motion + custom | Animated icons, progress rings, morphing shapes |

### 15.3 Transition Types

| Transition | Duration | Easing | Description |
|---|---|---|---|
| Page enter | 400ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Content fades in with slight vertical lift |
| Page exit | 200ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Content dissolves with slight scale |
| Modal/overlay | 300ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Glass backdrop emerges, content slides up |
| Graph node hover | 150ms | `ease-out` | Node glow + scale pulse |
| Memory materialize | 500ms | `cubic-bezier(0.16, 1, 0.3, 1)` | New memory appears as growing light |
| Memory dissolve | 300ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Memory fades outward in expanding ring |
| Recall answer | 50ms/token | `linear` | Typewriter effect with subtle cursor blink |

### 15.4 Color Palette for Animations

| Color | Hex | Usage |
|---|---|---|
| Black | `#000000` | Primary background |
| Graphite | `#1A1A1A` | Surface, cards, panels |
| Glass | `rgba(255,255,255,0.03)` | Frosted glass effects (backdrop-filter: blur) |
| Liquid Chrome | `#B0B0B0` → `#E8E8E8` | Metallic gradients, high-touch elements |
| Amber | `#F59E0B` | Accent (primary) — highlights, active states |
| Cyan | `#06B6D4` | Accent (secondary) — links, info, AI |
| White | `#FFFFFF` | Primary text |
| White (muted) | `rgba(255,255,255,0.6)` | Secondary text |
| White (faint) | `rgba(255,255,255,0.2)` | Borders, dividers |

### 15.5 Animation Performance Targets

- All animations must run at 60 FPS on a MacBook Pro M-series
- CSS animations preferred over JS where possible (GPU composited)
- 3D scenes (R3F) use `@react-three/drei` for performance (instanced meshes, LOD, frustum culling)
- `will-change` used sparingly and removed after animation completes
- Reduced motion mode: all animations disabled, transitions become instant opacity changes
- GSAP animations use `gsap.timeline()` for sequencing and `ScrollTrigger` scoped to specific viewports

---

## 16. Security Model

### 16.1 Authentication

| Method | Implementation | Use Case |
|---|---|---|
| Google OAuth | Google OAuth 2.0 (OpenID Connect) | Consumer users |
| Email/Password | bcrypt + JWT | Users without Google |
| API Keys | `memex_` prefixed, bcrypt hash stored | AI agents, programmatic access |
| JWT | RS256, 15-min access + 7-day refresh | Session authentication |

### 16.2 Authorization

- **User isolation:** Every user has their own Cognee user context. Datasets are owned by users.
- **Workspace-level:** Project access controlled via workspace membership.
- **Role-based:** `owner` > `admin` > `member` > `viewer` permissions on workspaces.
- **API key scoping:** Keys can be scoped to a single project with read-only or read-write permissions.
- **Cognee integration:** Cognee's permission system is configured with `ENABLE_BACKEND_ACCESS_CONTROL=true`.

### 16.3 Rate Limiting

| Endpoint | Limit | Window |
|---|---|---|
| `/remember` | 60 requests | per minute per user |
| `/recall` | 120 requests | per minute per user |
| `/recall` (streaming) | 30 requests | per minute per user |
| `/improve` | 10 requests | per hour per project |
| `/forget` | 30 requests | per minute per user |
| `/auth/*` | 10 requests | per minute per IP |
| General API | 1000 requests | per minute per user |

### 16.4 Data Protection

- **In transit:** TLS 1.3 for all external communication
- **At rest:** PostgreSQL data encrypted at rest (RDS/Aurora encryption)
- **Secrets:** Environment variables via Vercel/Railway secrets management
- **Embeddings:** Stored in pgvector column, accessible only through API
- **API key storage:** bcrypt hashed, never stored in plaintext

### 16.5 Input Validation

- All API inputs validated with Pydantic (backend)
- All file uploads scanned for size limits (100MB max per file)
- HTML/sanitization for any rendered user content
- SQL injection prevented via Cognee's internal ORM (SQLAlchemy)
- Prompt injection: Cognee's system prompts are separate from user input; graph extraction uses strict schemas

---

## 17. Deployment Plan

### 17.1 Architecture

```
                    ┌─────────────┐
                    │   Vercel    │
                    │  (Frontend) │
                    │  Next.js    │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Railway    │  ← or Render
                    │  (Backend)  │
                    │  FastAPI    │
                    │  Worker     │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  PostgreSQL │
                    │  (Railway)  │
                    │  pgvector   │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Redis      │
                    │  (Railway)  │
                    └─────────────┘
```

### 17.2 Environments

| Environment | URL | PostgreSQL | Redis | LLM Model |
|---|---|---|---|---|
| **Preview** | `pr-*.memex.pages.dev` | Ephemeral (Railway) | Ephemeral | GPT-4o-mini |
| **Staging** | `staging.memex.sh` | Shared (Railway) | Shared | GPT-4o-mini |
| **Production** | `memex.sh` | Dedicated (Railway) | Dedicated | GPT-4o |

### 17.3 CI/CD Pipeline

```
Push to main / PR
    │
    ├──→ Lint (ESLint, Ruff)
    ├──→ Type Check (TypeScript, mypy)
    ├──→ Unit Tests (Vitest, pytest)
    ├──→ Integration Tests (Playwright, pytest)
    │
    ├──→ Preview Deploy (Vercel + Railway)
    │       │
    │       ├──→ E2E Tests (Playwright)
    │       └──→ Load Tests (k6 - optional)
    │
    └──→ Production Deploy (manual approval)
            │
            ├──→ Migrate DB (Alembic)
            ├──→ Deploy API (Railway)
            ├──→ Deploy Worker (Railway)
            └──→ Deploy Frontend (Vercel)
```

### 17.4 Infrastructure as Code

- **Railway:** Environment configuration via `railway.json` + environment variables
- **Vercel:** Project configuration via `vercel.json`
- **Docker:** All backend services containerized for local development
- **No Terraform** at this stage (Railway handles infra)

---

## 18. Scaling Plan

### 18.1 100 Users (MVP / Hackathon)

**Strategy: Simplicity**
- Single PostgreSQL instance (Railway Starter, 1GB RAM)
- Single Redis instance (Railway Starter, 256MB)
- Single FastAPI instance (Railway, 512MB, 1 CPU)
- Single Worker instance (Railway, 512MB)
- Cognee configured for single-PostgreSQL mode (graph, vectors, relational all in one DB)
- Vercel Pro for frontend

**Expected Performance:**
- 50K memories, ~500K graph nodes
- Recall: <500ms p95
- Remember: <5s per document

### 18.2 10,000 Users (Growth Phase)

**Strategy: Separation + Caching**
- PostgreSQL read replica for recall queries
- Separate pgvector index for vector search
- Redis cluster (2 nodes) for session cache + rate limiting
- API Gateway scaled to 3 instances (Railway horizontal scaling)
- Worker scaled to 2 instances
- Cognee: separate graph store from relational store (NetworkX in-memory or Neo4j dedicated)

**Expected Performance:**
- 5M memories, ~50M graph nodes
- Recall: <1s p95
- Remember: <10s per document

### 18.3 1,000,000 Users (Scale)

**Strategy: Full Separation**
- PostgreSQL cluster (primary + 2 read replicas, 8GB RAM each)
- Dedicated pgvector with HNSW index
- Neo4j dedicated instance for graph store
- Redis cluster (4 nodes)
- API Gateway: 20+ instances (auto-scaled)
- Worker: 10+ instances
- Cognee: Enterprise configuration with dedicated graph DB + vector DB
- CDN (Vercel Edge) for static assets + cached recall results
- CQRS: Separate read/write paths for memory operations

**Expected Performance:**
- 500M memories, ~5B graph nodes
- Recall: <2s p95
- Remember: <30s per document

### 18.4 Bottleneck Prevention

| Bottleneck | Strategy |
|---|---|
| **Vector search** | HNSW index on pgvector, pre-filtering by dataset |
| **Graph traversal** | Neo4j with focused neighborhood queries, limit depth |
| **LLM latency** | Streaming, smaller model for simple queries, caching |
| **Ingestion throughput** | Background queue, batch processing, parallel chunking |
| **Session cache memory** | Redis with TTL, LRU eviction |
| **Frontend bundle** | Code splitting, tree shaking, route-based lazy loading |
| **3D rendering** | LOD (level of detail), frustum culling, instanced meshes |

---

## 19. Future Features

### Phase 2 (Post-Hackathon)

| Feature | Description |
|---|---|
| **Memory Sharing** | Share specific memories or clusters with other users/workspaces |
| **Agent SDK** | Python/JS SDK for AI agents to read/write MEMEX memory |
| **Browser Extension** | Clip web pages, articles, research into memory with one click |
| **Slack Integration** | Remember Slack conversations, decisions from channels |
| **GitHub Integration** | Auto-sync issues, PRs, decisions into memory graph |
| **VS Code Extension** | Remember coding context, decisions, architecture notes |
| **Mobile App** | React Native app for on-the-go memory capture and recall |

### Phase 3 (Post-Launch)

| Feature | Description |
|---|---|
| **Memory Templates** | Pre-built ingestion schemas for common use cases (standups, retrospectives, research) |
| **Collaborative Graph** | Real-time multi-user memory exploration (think Figma for knowledge graphs) |
| **Memory Time Machine** | Browse/slider through memory state at any point in time |
| **AI Memory Analyst** | An AI that proactively surfaces insights, patterns, and anomalies from your memory |
| **Custom Embedding Models** | Fine-tune embedding models on user's specific domain vocabulary |
| **Self-Hosted Option** | Docker Compose deployment for enterprises with data sovereignty requirements |
| **Enterprise SSO** | SAML, OIDC, SCIM for enterprise teams |

---

## 20. Risks

### Technical Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Cognee API instability during hackathon | Blocked features | Pin Cognee version, have fallback path for demo |
| OpenAI API rate limits | Slow recall/ingestion | Queue + retry, use GPT-4o-mini for non-critical paths |
| PostgreSQL pgvector performance degrades at scale | Slow recall | HNSW index, pre-filtering, limit vector dimensions |
| 3D scene (R3F) performance on low-end hardware | Poor UX | LOD, fallback to 2D React Flow view |
| Redis session cache data loss | Lost session context | Redis AOF persistence, session also stored in PostgreSQL periodically |
| Graph grows unbounded | Slow query, high cost | Memory lifecycle management (TTL for non-important memories) |

### Product Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Users don't understand "memory operating system" | Low adoption | Clear messaging, demo video, one-sentence pitch |
| Too complex for hackathon delivery | Missed deadline | Strict MVP scope, cut 3D universe to 2D if needed |
| Cognee's "cinematic" vision doesn't translate | Judges don't get it | Focus on the five pillars demo, make visual impact secondary |
| LLM cost per user too high | Unsustainable unit economics | Aggressive caching, GPT-4o-mini for improve(), rate limits |

---

## 21. Technical Decisions

### Why Cognee as the Core Engine

Cognee is the only open-source memory platform that natively provides **Remember, Recall, Improve, and Forget** operations over a **graph-vector hybrid** store. Its API surface maps exactly to our product pillars. Building these capabilities from scratch would take months.

Cognee's session memory + permanent graph memory dual-mode perfectly serves our short-term recall and long-term knowledge needs. The `improve()` operation with feedback weighting, session bridging, and global context indexing gives us a built-in mechanism for memory evolution.

### Why FastAPI over Next.js API Routes

Cognee is a Python library. Running it from JavaScript would require a separate Python microservice anyway. FastAPI gives us:
- Direct Python SDK access to Cognee (no HTTP overhead)
- Native async support for streaming
- Pydantic validation
- Auto-generated OpenAPI docs

Next.js API Routes would add a `subprocess` or HTTP hop to call Cognee, increasing latency and complexity.

### Why Single PostgreSQL for MVP

Cognee v1.0 supports running the entire memory stack (relational + vector + graph) on a single PostgreSQL instance. This eliminates the need for Neo4j, Pinecone, and other infrastructure during the hackathon. We can separate stores later when scaling demands it.

### Why React Three Fiber for the Memory Universe

R3F provides declarative, React-native 3D rendering with Three.js. It allows us to create the "celestial body" memory visualization without writing raw Three.js. The `@react-three/drei` and `@react-three/postprocessing` libraries provide camera controls, effects, and performance optimizations out of the box.

However, R3F is the **first thing to cut** if the hackathon timeline is tight. A 2D React Flow graph with GSAP animations can deliver 80% of the visual impact with 20% of the effort.

### Why SSE over WebSockets

Server-Sent Events are simpler to implement (standard HTTP, no upgrade, no bidirectional complexity), are supported by all major frontend frameworks, and work perfectly for our one-directional streaming use case (server → client). WebSockets would add complexity around reconnection, state management, and scaling.

### Why Turborepo + pnpm

Turborepo provides fast monorepo task running, parallel builds, and caching. pnpm's strict dependency management prevents package leakage between apps/packages. Both are battle-tested in large monorepos (Vercel uses Turborepo, pnpm is used by many large JS projects).

---

## 22. Roadmap

### Hackathon (Week 1) — MVP

| Day | Focus | Deliverables |
|---|---|---|
| **Day 1** | Setup + Core Backend | Monorepo scaffold, FastAPI server, Cognee integration, PostgreSQL schema, basic remember/recall endpoints |
| **Day 2** | Auth + Frontend Setup | Google OAuth + email auth, Next.js app shell, minimal layout, auth flow |
| **Day 3** | Core Frontend | Recall interface (search + results), Ingest interface (text input, file upload), session management |
| **Day 4** | Visualization + Improve | Basic Memory Universe (R3F or React Flow), improve() trigger, graph neighborhood view |
| **Day 5** | Polish + Demo | Animations, transitions, streaming recall, edge cases, bug fixes, demo prep |
| **Day 6** | Buffer/Demo Refinement | Performance tuning, accessibility pass, demo script, pitch deck |

### Post-Hackathon (Weeks 2-4)

- Memory sharing and team workspaces
- API key management for agents
- GitHub integration
- Browser extension
- Performance optimization at 10K+ memory scale

### Post-Hackathon (Weeks 5-8)

- Mobile app
- Advanced memory visualization (true 3D universe)
- Custom embedding models
- AI Memory Analyst feature
- Enterprise SSO

---

## 23. Folder Structure

### Frontend (`apps/web/`)

```
apps/web/
├── public/
│   ├── fonts/              # Custom fonts (Inter, JetBrains Mono)
│   ├── textures/           # Glass/noise textures for visual effects
│   └── lottie/             # Lottie animation files
│
├── src/
│   ├── app/                # Next.js App Router pages
│   │   ├── (auth)/         # Auth-optional layout group
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/    # Authenticated layout group
│   │   │   ├── layout.tsx  # Dashboard layout (sidebar, header)
│   │   │   ├── page.tsx    # Universe view (default)
│   │   │   ├── recall/
│   │   │   ├── ingest/
│   │   │   ├── memories/
│   │   │   ├── clusters/
│   │   │   ├── graph/
│   │   │   ├── projects/
│   │   │   └── settings/
│   │   ├── layout.tsx      # Root layout (providers, global styles)
│   │   └── providers.tsx   # All providers composed
│   │
│   ├── components/
│   │   ├── ui/             # Primitives (Button, Input, Card, Dialog, etc.)
│   │   ├── layout/         # Shell components (Sidebar, Header, CommandPalette)
│   │   ├── memory/         # Memory-specific components
│   │   │   ├── MemoryCard.tsx
│   │   │   ├── MemoryDetail.tsx
│   │   │   ├── MemoryList.tsx
│   │   │   └── MemorySource.tsx
│   │   ├── recall/         # Recall-specific components
│   │   │   ├── SearchInput.tsx
│   │   │   ├── RecallResults.tsx
│   │   │   ├── StreamingAnswer.tsx
│   │   │   └── SourceAttribution.tsx
│   │   ├── ingest/         # Ingest-specific components
│   │   │   ├── DropZone.tsx
│   │   │   ├── TextInput.tsx
│   │   │   ├── UrlImport.tsx
│   │   │   └── IngestProgress.tsx
│   │   ├── graph/          # Graph visualization components
│   │   │   ├── Universe3D/ # React Three Fiber scene
│   │   │   ├── Graph2D/    # React Flow graph
│   │   │   └── ClusterView/
│   │   ├── shared/         # Shared UI patterns
│   │   │   ├── Glass.tsx
│   │   │   ├── AmbientParticles.tsx
│   │   │   └── Typewriter.tsx
│   │   └── animations/     # Animation primitives
│   │       ├── Emerge.tsx
│   │       ├── Dissolve.tsx
│   │       └── Materialize.tsx
│   │
│   ├── hooks/
│   │   ├── useRecall.ts
│   │   ├── useRemember.ts
│   │   ├── useImprove.ts
│   │   ├── useForget.ts
│   │   ├── useMemoryGraph.ts
│   │   ├── useUniverseCamera.ts
│   │   ├── useStreamingAnswer.ts
│   │   └── useCommandPalette.ts
│   │
│   ├── lib/
│   │   ├── api/            # API client (fetchers, typed endpoints)
│   │   ├── auth/           # Auth utilities
│   │   ├── utils/          # General utilities
│   │   └── constants.ts
│   │
│   ├── types/              # TypeScript types (mirrors shared/types)
│   ├── styles/             # Global styles, Tailwind config extensions
│   └── config/             # App configuration
│
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

### Backend (`apps/api/`)

```
apps/api/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app, middleware, lifespan
│   ├── config.py              # Environment configuration
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py          # Main router aggregation
│   │   ├── deps.py            # Dependency injection (auth, db, cognee)
│   │   │
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── memory.py      # /remember, /recall, /improve, /forget
│   │   │   ├── projects.py    # /projects CRUD
│   │   │   ├── workspaces.py  # /workspaces CRUD
│   │   │   ├── graph.py       # /graph neighborhood, clusters, timeline
│   │   │   ├── sessions.py    # /sessions CRUD
│   │   │   ├── analytics.py   # /analytics endpoints
│   │   │   └── auth.py        # /auth endpoints
│   │   │
│   │   └── middleware/
│   │       ├── auth.py        # JWT verification middleware
│   │       ├── rate_limit.py  # Rate limiting
│   │       └── logging.py     # Request logging
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── memory.py          # Memory service (orchestrates Cognee)
│   │   ├── cognee_config.py   # Cognee initialization and configuration
│   │   ├── search.py          # Search coordination
│   │   └── analytics.py       # Analytics service
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── workspace.py
│   │   ├── memory.py
│   │   ├── session.py
│   │   ├── event.py
│   │   └── api_key.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── memory.py          # Pydantic request/response schemas
│   │   ├── recall.py
│   │   ├── auth.py
│   │   ├── project.py
│   │   └── graph.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── session.py         # SQLAlchemy session management
│       └── migrations/        # Alembic migrations
│
├── tests/
│   ├── conftest.py
│   ├── test_memory.py
│   ├── test_recall.py
│   ├── test_auth.py
│   └── test_graph.py
│
├── alembic.ini
├── Dockerfile
└── requirements.txt
```

### Worker (`apps/worker/`)

```
apps/worker/
├── app/
│   ├── __init__.py
│   ├── main.py                # Arq worker entrypoint
│   ├── config.py
│   │
│   └── tasks/
│       ├── __init__.py
│       ├── ingest.py           # Background ingestion
│       ├── improve.py          # Scheduled improvement passes
│       ├── expire.py           # TTL-based memory expiration
│       ├── compress.py         # Graph compression/dedup
│       └── global_context.py   # Global context index building
│
└── Dockerfile
```

---

## 24. Development Standards

### 24.1 Git Workflow

- **Branch naming:** `feature/description`, `fix/description`, `chore/description`
- **Commit style:** Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- **PRs:** Require at least 1 approval, all CI checks passing
- **No direct pushes to `main`**

### 24.2 Code Review Standards

- Every PR must include:
  - Description of what and why
  - Screenshots for UI changes
  - Test results
- Review criteria: correctness, performance, security, alignment with architecture

### 24.3 Testing Requirements

| Layer | Tool | Coverage Target |
|---|---|---|
| **Backend (unit)** | pytest + pytest-asyncio | 90%+ |
| **Backend (integration)** | pytest + httpx (AsyncClient) | Critical paths |
| **Frontend (unit)** | Vitest + React Testing Library | 80%+ |
| **Frontend (E2E)** | Playwright | Happy paths |
| **Worker** | pytest | 80%+ |

### 24.4 Documentation Standards

- All API endpoints documented with Pydantic schemas + FastAPI auto-docs
- README in every package explaining its purpose
- Architecture decisions recorded in `ARCHITECTURE.md`
- No inline comments in code (code should be self-documenting)

---

## 25. Coding Standards

### TypeScript/React

- Strict TypeScript mode (`strict: true`)
- No `any` types (use `unknown` and type guards)
- Functional components with hooks (no class components)
- Props typed with `interface ComponentNameProps`
- Named exports (no default exports except for pages)
- Async data fetching via TanStack React Query, never `useEffect`
- Framer Motion variants defined outside component for reusability

### Python/FastAPI

- Type hints required on all function signatures
- Pydantic v2 for all request/response models
- Async SQLAlchemy 2.0 style (no legacy ORM patterns)
- Services are stateless classes with injected dependencies
- No business logic in route handlers
- All external calls wrapped in try/except with proper error propagation

### CSS/Tailwind

- Tailwind utility classes for 95% of styling
- Custom CSS only for complex animations or glass effects
- CSS variables for design tokens (colors, spacing, fonts)
- No inline styles
- All animations respect `prefers-reduced-motion`

---

## 26. Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| **TypeScript files** | kebab-case | `use-recall.ts`, `memory-card.tsx` |
| **Python files** | snake_case | `memory_service.py`, `cognee_config.py` |
| **React components** | PascalCase | `MemoryCard`, `RecallResults`, `StreamingAnswer` |
| **React hooks** | camelCase with `use` prefix | `useRecall`, `useMemoryGraph` |
| **Python classes** | PascalCase | `MemoryService`, `CogneeConfig` |
| **Python functions** | snake_case | `get_neighborhood()`, `format_recall_result()` |
| **API endpoints** | kebab-case | `/api/v1/memex/recall`, `/graph/neighborhood` |
| **Database tables** | snake_case (plural) | `memories`, `knowledge_clusters`, `workspace_members` |
| **Database columns** | snake_case | `created_at`, `memory_type`, `cognee_dataset_id` |
| **Environment variables** | UPPER_SNAKE_CASE | `MEMEX_DATABASE_URL`, `OPENAI_API_KEY` |
| **CSS classes** | kebab-case (Tailwind) | Already handled by Tailwind |

---

## 27. Acceptance Criteria

### Must-Have (Hackathon MVP)

1. **User can register and log in** via Google OAuth or email/password
2. **User can ingest a memory** (text input and file upload) via the Ingest view
3. **User can recall memories** via natural language search in the Recall view
4. **Recall streaming** — answers appear token by token (typewriter effect)
5. **Sources shown** — each recall answer includes source attributions
6. **Memory visualization** — memories shown as interactive nodes in a graph (2D React Flow is acceptable for MVP)
7. **Improvement pass** — user can trigger improve() and see status
8. **Forget** — user can delete a memory and see it dissolve from the UI
9. **Multi-turn conversation** — session memory carries context between turns
10. **Project scoping** — memories are scoped to a project
11. **Cinematic UI** — glass-morphism design, dark theme, smooth transitions, no spinners
12. **API accessible** — all core features available via REST API
13. **Performance** — recall < 2s p95, page loads < 1s, 60 FPS animations

### Should-Have

14. **API keys** — user can create API keys for agent access
15. **Code ingestion** — user can paste/upload code and it's properly indexed
16. **Graph neighborhood view** — click a memory node to see its relationships
17. **Memory timeline** — browse memories by time (temporal retrieval)
18. **Cluster visualization** — knowledge clusters shown as groups in the universe view
19. **Feedback** — thumbs up/down on recall answers, affects future ranking

### Nice-to-Have

20. **3D Memory Universe** — full Three.js celestial body visualization
21. **Global context indexing** — dataset-level summaries for better recall
22. **Batch ingestion** — drag multiple files, ingest in bulk
23. **Reduced motion mode** — all animations disabled
24. **Keyboard shortcuts** — Cmd+K for search, full keyboard navigation

---

## Appendix A: Technology Justification Summary

| Technology | Choice | Why Not Alternative |
|---|---|---|
| **Runtime** | Next.js + FastAPI | Next.js alone can't run Cognee (Python lib) |
| **Memory Engine** | Cognee | LangChain memory is too shallow; building from scratch is infeasible |
| **Graph DB** | PostgreSQL (AGE) | Neo4j adds infra complexity for MVP; AGE gives graph features in existing DB |
| **Vector DB** | pgvector | Pinecone/Weaviate add cost and complexity; pgvector in existing DB is simpler |
| **Session Cache** | Redis | In-memory fast; filesystem is too slow for multi-turn conversations |
| **3D Rendering** | React Three Fiber | raw Three.js is harder to integrate with React; Unity/Unreal are overkill |
| **Monorepo** | Turborepo + pnpm | Nx is heavier; yarn workspaces have slower installs |
| **Styling** | Tailwind | CSS-in-JS (styled-components) has runtime cost; vanilla CSS is slower to develop with |
| **State** | TanStack Query + Zustand | Redux is too verbose; Context-only is insufficient for server state |

---

## Appendix B: Key Configuration Values

```env
# Cognee Configuration
COGNEE_RELATIONAL_DB=postgresql+asyncpg://...
COGNEE_VECTOR_DB=postgresql+asyncpg://...  # pgvector
COGNEE_GRAPH_DB=postgresql+asyncpg://...   # AGE or networkx
COGNEE_CACHE_BACKEND=redis
COGNEE_REDIS_URL=redis://...
COGNEE_DEFAULT_EMBEDDING_MODEL=text-embedding-3-small
COGNEE_DEFAULT_LLM_MODEL=gpt-4o
COGNEE_CHUNK_SIZE=1024
COGNEE_SELF_IMPROVEMENT=true
COGNEE_ENABLE_BACKEND_ACCESS_CONTROL=true

# MEMEX Configuration
MEMEX_DATABASE_URL=postgresql+asyncpg://...
MEMEX_REDIS_URL=redis://...
MEMEX_JWT_SECRET=...
MEMEX_JWT_ALGORITHM=RS256
MEMEX_JWT_ACCESS_EXPIRE_MINUTES=15
MEMEX_JWT_REFRESH_EXPIRE_DAYS=7

# Auth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# OpenAI
OPENAI_API_KEY=...
```

---

## Appendix C: Glossary

| Term | Definition |
|---|---|
| **Memory** | A unit of stored information — a text, file, conversation, decision, etc. |
| **Memory Node** | An entity in the knowledge graph (person, concept, place, etc.) |
| **Memory Edge** | A relationship between two nodes (connects, depends_on, decided, etc.) |
| **Session** | A short-lived conversation context with caching and state |
| **Dataset** | Cognee's scoped collection of memories (maps to a MEMEX project) |
| **Knowledge Cluster** | A group of related memories/nodes (a "galaxy" in the universe view) |
| **Improvement** | The process of enriching, merging, strengthening, and summarizing memory |
| **Graph Completion** | Cognee's default recall mode: vector search → graph traversal → LLM answer |
| **Auto-routing** | Cognee's query classifier that chooses the best retrieval strategy |
| **Universe** | The 3D visualization of all memories as celestial bodies |
| **Source Attribution** | The provenance information showing where a recall answer came from |

---

*End of Architecture Document v1.0.0*
