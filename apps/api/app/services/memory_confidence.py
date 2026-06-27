from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any

from app.schemas.reasoning import ConfidenceFactors, MemoryConfidence


class MemoryConfidenceService:
    def evaluate(
        self,
        source_count: int,
        source_details: list[dict[str, Any]] | None = None,
        relationship_strength: float | None = None,
        timestamps: list[datetime] | None = None,
        entity_types: list[str] | None = None,
        graph_degree: int = 0,
    ) -> MemoryConfidence:
        factors = ConfidenceFactors(
            source_count=min(source_count / 10, 1.0),
            relationship_strength=relationship_strength or 0,
            recency_score=self._recency_score(timestamps or []),
            agreement_score=self._agreement_score(source_details or []),
            entity_consistency=self._entity_consistency(entity_types or []),
            graph_connectivity=min(graph_degree / 20, 1.0),
        )
        weights = {
            "source_count": 0.20,
            "relationship_strength": 0.20,
            "recency_score": 0.15,
            "agreement_score": 0.20,
            "entity_consistency": 0.10,
            "graph_connectivity": 0.15,
        }
        score = (
            factors.source_count * weights["source_count"]
            + factors.relationship_strength * weights["relationship_strength"]
            + factors.recency_score * weights["recency_score"]
            + factors.agreement_score * weights["agreement_score"]
            + factors.entity_consistency * weights["entity_consistency"]
            + factors.graph_connectivity * weights["graph_connectivity"]
        )
        label = self._label(score)
        return MemoryConfidence(score=round(score, 3), factors=factors, label=label)

    def _recency_score(self, timestamps: list[datetime]) -> float:
        if not timestamps:
            return 0
        now = datetime.now(UTC)
        scores = []
        for ts in timestamps:
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=UTC)
            days_ago = (now - ts).total_seconds() / 86400
            scores.append(math.exp(-days_ago / 30))
        return sum(scores) / len(scores) if scores else 0

    def _agreement_score(self, sources: list[dict[str, Any]]) -> float:
        if len(sources) < 2:
            return 0.5
        texts = [s.get("text", "") for s in sources if s.get("text")]
        if len(texts) < 2:
            return 0.5
        overlap_ratios = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                words_i = set(texts[i].lower().split())
                words_j = set(texts[j].lower().split())
                if not words_i or not words_j:
                    continue
                overlap = len(words_i & words_j)
                ratio = overlap / min(len(words_i), len(words_j))
                overlap_ratios.append(ratio)
        return sum(overlap_ratios) / len(overlap_ratios) if overlap_ratios else 0.5

    def _entity_consistency(self, types: list[str]) -> float:
        if not types:
            return 0.5
        type_counts: dict[str, int] = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1
        max_type = max(type_counts.values())
        return max_type / len(types) if types else 0.5

    def _label(self, score: float) -> str:
        if score >= 0.9:
            return "very high"
        if score >= 0.7:
            return "high"
        if score >= 0.5:
            return "moderate"
        if score >= 0.3:
            return "low"
        return "very low"


memory_confidence_service = MemoryConfidenceService()
