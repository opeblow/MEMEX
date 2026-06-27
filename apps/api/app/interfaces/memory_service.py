from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RememberInput:
    user_id: str
    project_id: str
    data: str | None = None
    session_id: str | None = None
    memory_type: str | None = None
    title: str | None = None
    tags: list[str] | None = None
    run_in_background: bool = False


@dataclass
class RememberOutput:
    memory_id: str
    dataset_id: str
    chunk_count: int = 0
    token_count: int = 0
    processing_time_ms: int = 0
    status: str = "processing"


class MemoryServiceInterface(ABC):
    @abstractmethod
    async def remember(self, input_data: RememberInput) -> RememberOutput:
        ...

    @abstractmethod
    async def improve(
        self,
        user_id: str,
        project_id: str,
        session_ids: list[str] | None = None,
        build_global_context_index: bool = False,
        run_in_background: bool = False,
    ) -> dict:
        ...

    @abstractmethod
    async def forget(
        self,
        user_id: str,
        project_id: str,
        data_id: str | None = None,
        dataset: str | None = None,
        everything: bool = False,
        memory_only: bool = False,
    ) -> dict:
        ...
