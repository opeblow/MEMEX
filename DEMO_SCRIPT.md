# MEMEX — Demo Script (3 Minutes)

## Setup (Pre-Recording)

- Ensure PostgreSQL, Redis, API, and Frontend are running
- Pre-login to the app with a seeded account
- Have a few memories already ingested (text + URL)
- Open browser at http://localhost:3000/recall

---

## Act 1: The Problem (0:00 – 0:30)

> **Narrator:** "Every AI assistant today starts from zero. Every conversation is amnesiac. Every insight is lost."

**Screen:** Cursor hovers over the landing page hero. Neural background animation pulses.

> **Narrator:** "MEMEX is the operating system for artificial memory. Let me show you what that means."

**Action:** Click "Enter" → Navigate to `/recall`

---

## Act 2: Memory Creation — REMEMBER (0:30 – 1:00)

> **Narrator:** "First, let's create a memory."

**Action:** Navigate to `/ingest`

- Type a quick note: *"Met with the team about the new memory compression algorithm. Key insight: we can use hierarchical summarization to reduce storage by 60% without losing semantic fidelity."*
- Click "Remember"

**Screen:** Toast appears: "Memory indexed successfully"

> **Narrator:** "That text was immediately chunked, entities extracted, embeddings generated, and stored in Cognee's graph + vector database."

---

## Act 3: Memory Recall — RECALL (1:00 – 1:30)

> **Narrator:** "Now let me ask a question about something I stored earlier."

**Action:** Back in `/recall`, type: *"What was the insight about memory compression?"*

**Screen:** Streaming response appears with:
- The answer: "Hierarchical summarization can reduce storage by 60% without losing semantic fidelity"
- Source attribution: "Source: graph completion"
- Reasoning trail showing the graph traversal path

> **Narrator:** "Cognee auto-routed this query through vector search and graph traversal. The answer is not just a text match — it understands the relationship between concepts."

---

## Act 4: Memory Improvement — IMPROVE (1:30 – 1:45)

> **Narrator:** "Memory doesn't just sit there. It improves."

**Action:** Navigate to `/memories`

- Show the memory card with the compression note
- Point out the importance badge and related entities

> **Narrator:** "Every memory goes through Cognee's improvement pipeline — deduplication, relationship strengthening, and summarization. Over time, the knowledge graph gets smarter."

---

## Act 5: Memory Forgetting — FORGET (1:45 – 2:00)

> **Narrator:** "And when memory is no longer needed, it can be forgotten."

**Action:** Click archive/delete on a memory

> **Narrator:** "This removes the data from all three stores — relational, vector, and graph — while preserving shared nodes that other memories reference."

---

## Act 6: Knowledge Graph (2:00 – 2:20)

> **Narrator:** "But the real power is the knowledge graph."

**Action:** Navigate to `/graph`

- Show the node/edge visualization
- Point out entity clusters and relationships

> **Narrator:** "Every memory creates nodes and edges in a living knowledge graph. You can see how concepts connect, explore neighborhoods, and discover relationships you didn't know existed."

---

## Act 7: AI Reasoning (2:20 – 2:40)

> **Narrator:** "And this is where it gets interesting."

**Action:** Navigate to `/chat`

- Ask: *"What do I know about compression techniques?"*
- Show the reasoning trail (multi-step) with confidence scores

> **Narrator:** "The AI doesn't just retrieve text — it reasons across the graph. It connects memories, follows relationships, and provides answers with traceable provenance."

---

## Act 8: 3D Memory Universe (2:40 – 2:55)

**Action:** Navigate to `/recall`

- Toggle to 3D Universe view
- Orbit around memory nodes (celestial bodies)
- Point out a knowledge cluster

> **Narrator:** "And this is the Memory Universe — every memory is a celestial body. Orbit radius is semantic distance. Brightness is importance. Color is content type. Clusters are knowledge galaxies."

---

## Close (2:55 – 3:00)

> **Narrator:** "MEMEX + Cognee. The operating system for artificial memory. Persistent. Evolving. Queryable. Forever."

**Screen:** Fade to the MEMEX logo.

---

## Demo Checklist

- [ ] Pre-seeded memories exist
- [ ] PostgreSQL + Redis running
- [ ] API server running on port 8000
- [ ] Frontend running on port 3000
- [ ] OpenAI API key configured (for embeddings + LLM)
- [ ] Screen recording software ready (OBS, CleanShot, etc.)
- [ ] Microphone tested
- [ ] No browser extensions interfering
- [ ] Dark mode (always-on, no toggle needed)
