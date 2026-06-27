from __future__ import annotations


class RankedSource:
    def __init__(
        self,
        text: str,
        source: str,
        memory_id: str,
        chunk_id: str | None = None,
        relevance_score: float = 0.0,
        evidence: str | None = None,
        explanation: str | None = None,
    ):
        self.text = text
        self.source = source
        self.memory_id = memory_id
        self.chunk_id = chunk_id
        self.relevance_score = relevance_score
        self.evidence = evidence
        self.explanation = explanation


class MemoryRanker:
    def __init__(self):
        self.type_weights = {
            "text": 1.0,
            "code": 1.1,
            "conversation": 1.0,
            "meeting_note": 1.05,
            "research": 1.15,
            "decision": 1.2,
            "github_issue": 0.95,
            "support_ticket": 0.9,
            "url": 0.85,
            "file": 0.8,
            "image": 0.7,
            "audio": 0.6,
            "video": 0.6,
        }

    def rank(
        self,
        sources: list[dict],
        query: str,
        importance_boost: bool = True,
    ) -> list[RankedSource]:
        ranked: list[RankedSource] = []

        for src in sources:
            score = src.get("relevance_score", 0.0)
            memory_type = src.get("memory_type", "text")
            type_weight = self.type_weights.get(memory_type, 1.0)

            if importance_boost:
                importance = src.get("importance", 0.5)
                score = score * 0.7 + importance * 0.3
            score = score * type_weight

            explanation = self._build_explanation(src, score, query)
            ranked.append(
                RankedSource(
                    text=src.get("text", ""),
                    source=src.get("source", "graph"),
                    memory_id=src.get("memory_id", ""),
                    chunk_id=src.get("chunk_id"),
                    relevance_score=round(min(score, 1.0), 4),
                    evidence=src.get("evidence"),
                    explanation=explanation,
                )
            )

        ranked.sort(key=lambda r: r.relevance_score, reverse=True)
        return ranked

    def _build_explanation(
        self, src: dict, score: float, query: str
    ) -> str:
        parts: list[str] = []
        source = src.get("source", "unknown")
        memory_type = src.get("memory_type", "text")
        importance = src.get("importance", 0.5)

        if source == "graph":
            parts.append("Matched via graph traversal")
        elif source == "session":
            parts.append("Found in active session context")
        elif source == "vector":
            parts.append("Semantic similarity match")
        else:
            parts.append(f"Retrieved from {source}")

        parts.append(f"Memory type: {memory_type}")
        parts.append(f"Importance weight: {importance:.2f}")
        parts.append(f"Combined relevance: {score:.4f}")

        return " | ".join(parts)


memory_ranker = MemoryRanker()
