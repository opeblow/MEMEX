from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class RecallInput:
    user_id: str
    query: str
    project_id: str
    session_id: str | None = None
    datasets: list[str] | None = None
    query_type: str | None = None
    top_k: int = 15
    only_context: bool = False
    stream: bool = False


@dataclass
class RecallSource:
    text: str
    source: str
    memory_id: str
    chunk_id: str | None = None
    relevance_score: float = 0.0
    evidence: str | None = None


@dataclass
class RecallOutput:
    answer: str = ""
    sources: list[RecallSource] = list()
    processing_time_ms: int = 0


class CogneeServiceInterface(ABC):
    @abstractmethod
    async def recall(self, input_data: RecallInput) -> RecallOutput:
        ...

    @abstractmethod
    async def recall_stream(
        self, input_data: RecallInput
    ) -> AsyncIterator[dict]:
        ...
        yield {}

    @abstractmethod
    async def check_health(self) -> bool:
        ...
