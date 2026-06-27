from __future__ import annotations

import time
from typing import Any

from app.schemas.reasoning import (
    MemoryConfidence,
    MemoryContribution,
    ReasoningRequest,
    ReasoningResponse,
    RelationshipPath,
    TimelinePath,
    TrailStep,
)
from app.services.memory_confidence import memory_confidence_service
from app.services.memory_trail import trail_service


class ReasoningEngine:
    def __init__(self):
        self.pipeline_steps = [
            "intent_detection",
            "memory_retrieval",
            "graph_traversal",
            "relationship_ranking",
            "timeline_analysis",
            "evidence_collection",
            "context_compression",
            "llm_response",
            "source_attribution",
        ]

    async def reason(
        self,
        db: Any,
        user_id: str,
        request: ReasoningRequest,
    ) -> ReasoningResponse:
        from app.services.knowledge import knowledge_service
        from app.services.memory_retriever import memory_retriever

        start = time.time()
        trail_steps: list[TrailStep] = []
        memory_ids_used: set[str] = set()
        start_time = time.time()

        intent_result = await self._detect_intent(request.query)
        trail_steps.append(TrailStep(
            step=1,
            name="intent_detection",
            description=f"Detected intent: {intent_result.get('intent', 'unknown')}",
            data=intent_result,
            duration_ms=(time.time() - start_time) * 1000,
        ))

        step_start = time.time()
        retrieval_results = await memory_retriever.multi_strategy_search(
            db=db,
            user_id=user_id,
            query=request.query,
            project_id=request.project_id,
            top_k=request.top_k,
        )
        for r in retrieval_results:
            mid = r.get("memory_id")
            if mid:
                memory_ids_used.add(mid)
        trail_steps.append(TrailStep(
            step=2,
            name="memory_retrieval",
            description=f"Retrieved {len(retrieval_results)} memories",
            data={"results_count": len(retrieval_results)},
            memory_ids=list(memory_ids_used),
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        graph_results = await self._graph_traversal(
            db=db,
            project_id=request.project_id,
            retrieval_results=retrieval_results,
        )
        expanded_memory_ids = set(memory_ids_used)
        for gr in graph_results:
            mid = gr.get("memory_id")
            if mid:
                expanded_memory_ids.add(mid)
        trail_steps.append(TrailStep(
            step=3,
            name="graph_traversal",
            description=f"Traversed {len(graph_results)} graph connections",
            data={"connections_found": len(graph_results)},
            memory_ids=list(expanded_memory_ids),
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        ranked = await self._rank_relationships(
            retrieval_results=retrieval_results,
            graph_results=graph_results,
        )
        trail_steps.append(TrailStep(
            step=4,
            name="relationship_ranking",
            description=f"Ranked {len(ranked)} relationships by relevance",
            data={"top_score": ranked[0].get("combined_score", 0) if ranked else 0},
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        timeline_data = await self._timeline_analysis(
            db=db,
            project_id=request.project_id,
            memory_ids=list(memory_ids_used),
        )
        trail_steps.append(TrailStep(
            step=5,
            name="timeline_analysis",
            description=f"Analyzed {timeline_data.get('event_count', 0)} timeline events",
            data=timeline_data,
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        evidence = await self._collect_evidence(
            db=db,
            ranked_results=ranked,
        )
        trail_steps.append(TrailStep(
            step=6,
            name="evidence_collection",
            description=f"Collected {len(evidence)} pieces of evidence",
            memory_ids=[e.get("memory_id") for e in evidence if e.get("memory_id")],
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        compressed_context = self._compress_context(ranked, evidence)
        trail_steps.append(TrailStep(
            step=7,
            name="context_compression",
            description="Compressed context for LLM",
            data={"source_count": len(ranked), "evidence_count": len(evidence)},
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        confidence = memory_confidence_service.evaluate(
            source_count=len(ranked),
            source_details=ranked,
            relationship_strength=timeline_data.get("relationship_strength", 0),
            timestamps=[r.get("created_at") for r in ranked if r.get("created_at")],
            entity_types=[r.get("memory_type") for r in ranked if r.get("memory_type")],
            graph_degree=len(graph_results),
        )
        answer_data = await self._generate_answer(
            query=request.query,
            context=compressed_context,
            evidence=evidence,
            confidence=confidence,
            knowledge_service=knowledge_service,
        )
        trail_steps.append(TrailStep(
            step=8,
            name="llm_response",
            description="Generated response via LLM",
            data={"model": answer_data.get("model", "gpt-4o-mini")},
            duration_ms=(time.time() - step_start) * 1000,
        ))

        step_start = time.time()
        contributions = []
        relationship_paths = []
        timeline_paths = []
        for i, r in enumerate(ranked[:5]):
            contributions.append(MemoryContribution(
                memory_id=r.get("memory_id", ""),
                title=r.get("title"),
                relevance=r.get("combined_score", 0),
                evidence=r.get("evidence"),
                explanation=r.get("explanation"),
            ))
            if r.get("entity_path"):
                for path in r["entity_path"]:
                    relationship_paths.append(RelationshipPath(
                        from_entity=path.get("from", ""),
                        to_entity=path.get("to", ""),
                        relationship_type=path.get("type", "related_to"),
                        strength=path.get("strength", 0.5),
                    ))
        for ev in timeline_data.get("events", []):
            timeline_paths.append(TimelinePath(
                event_type=ev.get("event_type", ""),
                memory_id=ev.get("memory_id", ""),
                timestamp=ev.get("timestamp"),
                description=ev.get("description"),
            ))
        explanation = trail_service.build_explanation(
            summary=answer_data.get("explanation_summary", ""),
            memory_contributions=contributions,
            relationship_paths=relationship_paths[:10] if relationship_paths else None,
            timeline_paths=timeline_paths[:10] if timeline_paths else None,
            confidence=confidence,
        )
        trail_steps.append(TrailStep(
            step=9,
            name="source_attribution",
            description=f"Attributed {len(contributions)} sources, confidence: {confidence.label}",
            duration_ms=(time.time() - step_start) * 1000,
        ))

        total_time = int((time.time() - start) * 1000)
        trail = await trail_service.create_trail(
            db=db,
            project_id=request.project_id,
            user_id=user_id,
            question=request.query,
            answer=answer_data.get("answer", ""),
            trail_steps=[s.model_dump() for s in trail_steps],
            memory_ids=list(memory_ids_used),
            confidence_score=confidence.score,
            processing_time_ms=total_time,
            model_used=answer_data.get("model"),
        )

        return ReasoningResponse(
            answer=answer_data.get("answer", ""),
            trail_id=trail.id,
            explanation=explanation if request.include_explanation else None,
            trail=trail_steps if request.include_trail else None,
            processing_time_ms=total_time,
        )

    async def _detect_intent(self, query: str) -> dict[str, Any]:
        query_lower = query.lower()
        temporal_words = {"what changed", "what happened", "before", "after",
                           "when did", "timeline", "history", "recent"}
        analytical_words = {"why", "how", "analyze", "compare", "contrast",
                            "evaluate", "explain", "relationship"}
        factual_words = {"what is", "who is", "where", "when", "which",
                         "find", "search", "tell me about"}
        if any(w in query_lower for w in temporal_words):
            intent = "temporal_query"
        elif any(w in query_lower for w in analytical_words):
            intent = "analytical_query"
        elif any(w in query_lower for w in factual_words):
            intent = "factual_query"
        else:
            intent = "general_query"
        return {"intent": intent, "query": query}

    async def _graph_traversal(
        self,
        db: Any,
        project_id: str,
        retrieval_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        from app.services.cognee_adapter import cognee_adapter

        graph_results = []
        for r in retrieval_results[:5]:
            memory_id = r.get("memory_id")
            if not memory_id:
                continue
            cognee_result = await cognee_adapter.recall(
                user_id="system",
                query=r.get("text", ""),
                project_id=project_id,
                session_id=None,
                datasets=None,
                query_type="graph_completion",
                top_k=3,
                only_context=True,
            )
            sources = cognee_result.get("sources", [])
            for s in sources:
                if isinstance(s, dict):
                    s["relationship_strength"] = r.get("relevance_score", 0.5)
                    graph_results.append(s)
        return graph_results

    async def _rank_relationships(
        self,
        retrieval_results: list[dict[str, Any]],
        graph_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        seen: set[str] = set()
        combined = []
        for r in retrieval_results:
            mid = r.get("memory_id", "")
            if mid in seen:
                continue
            seen.add(mid)
            score = r.get("relevance_score", 0) or 0
            graph_score = 0
            for g in graph_results:
                if g.get("memory_id") == mid:
                    graph_score = g.get("relevance_score", 0) or 0
            combined_score = score * 0.6 + graph_score * 0.4
            r["combined_score"] = combined_score
            r["graph_relevance"] = graph_score
            combined.append(r)
        combined.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
        return combined

    async def _timeline_analysis(
        self,
        db: Any,
        project_id: str,
        memory_ids: list[str],
    ) -> dict[str, Any]:
        from app.services.timeline_intelligence import timeline_intelligence_service
        context = await timeline_intelligence_service.timeline_context(db, project_id, days=30)
        events = []
        for m_id in memory_ids:
            before = await timeline_intelligence_service.what_happened_before(
                db, project_id, m_id, lookback_days=14,
            )
            for b in before:
                events.append({
                    "event_type": "memory_created",
                    "memory_id": b.get("memory_id", ""),
                    "timestamp": b.get("timestamp"),
                    "description": b.get("title", ""),
                })
        context["events"] = events
        context["relationship_strength"] = min(len(events) / 20, 1.0)
        return context

    async def _collect_evidence(
        self,
        db: Any,
        ranked_results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        from app.models.memory import Memory
        evidence = []
        for r in ranked_results[:10]:
            memory_id = r.get("memory_id")
            if not memory_id:
                continue
            memory = await db.get(Memory, memory_id)
            if memory is None:
                continue
            evidence.append({
                "memory_id": memory.id,
                "text": memory.content_preview or "",
                "source": memory.source or "unknown",
                "memory_type": memory.memory_type,
                "importance": memory.importance,
                "tags": memory.tags,
                "timestamp": memory.created_at.isoformat() if memory.created_at else None,
                "relevance_score": r.get("combined_score", 0),
            })
        return evidence

    def _compress_context(
        self,
        ranked_results: list[dict[str, Any]],
        evidence: list[dict[str, Any]],
    ) -> str:
        lines = []
        for r in ranked_results[:10]:
            text = r.get("text", "") or r.get("content_preview", "")
            if text:
                lines.append(f"- {text[:500]}")
        for e in evidence:
            if e.get("text") and e["text"] not in lines:
                lines.append(f"- {e['text'][:500]}")
        return "\n".join(lines[:20])

    async def _generate_answer(
        self,
        query: str,
        context: str,
        evidence: list[dict[str, Any]],
        confidence: MemoryConfidence,
        knowledge_service: Any,
    ) -> dict[str, Any]:
        from app.config import settings
        if not settings.openai_api_key:
            return self._fallback_answer(query, context, evidence, confidence)
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            evidence_lines = []
            for e in evidence[:8]:
                text = e.get('text', '')[:200]
                src = e.get('source', 'unknown')
                rel = e.get('relevance_score', 0)
                etype = e.get('memory_type', 'memory')
                evidence_lines.append(
                    f"[{etype}] {text} (source: {src}, relevance: {rel:.2f})"
                )
            evidence_summary = "\n".join(evidence_lines)
            system_prompt = (
                "You are MEMEX, an artificial reasoning engine. "
                "Answer the user's question based ONLY on the provided memory context. "
                "If the context does not contain enough information, say so. "
                "Cite specific memories and evidence in your answer. "
                "End with a brief explanation of your reasoning confidence."
            )
            user_prompt = (
                f"Question: {query}\n\n"
                f"Memory Context:\n{context}\n\n"
                f"Evidence:\n{evidence_summary}\n\n"
                f"Provide a concise, well-reasoned answer based on these memories."
            )
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )
            answer = response.choices[0].message.content or ""
            explanation_summary = (
                f"Answer generated from {len(evidence)} sources "
                f"with {confidence.label} confidence (score: {confidence.score:.2f}). "
                f"Key factors: {confidence.factors.source_count:.0%} source coverage, "
                f"{confidence.factors.relationship_strength:.0%} relationship strength, "
                f"{confidence.factors.recency_score:.0%} recency."
            )
            return {
                "answer": answer,
                "explanation_summary": explanation_summary,
                "model": "gpt-4o-mini",
            }
        except Exception:
            return self._fallback_answer(query, context, evidence, confidence)

    def _fallback_answer(
        self,
        query: str,
        context: str,
        evidence: list[dict[str, Any]],
        confidence: MemoryConfidence,
    ) -> dict[str, Any]:
        lines = context.strip().split("\n") if context.strip() else []
        if lines:
            answer = (
                f"Based on {len(evidence)} relevant memories:\n\n"
                + "\n".join(f"- {line[2:]}" for line in lines[:5] if line.startswith("- "))
            )
        else:
            answer = "No relevant memories found to answer this question."
        explanation_summary = (
            f"Answer based on {len(evidence)} sources "
            f"with {confidence.label} confidence."
        )
        return {
            "answer": answer,
            "explanation_summary": explanation_summary,
            "model": "fallback",
        }


reasoning_engine = ReasoningEngine()
