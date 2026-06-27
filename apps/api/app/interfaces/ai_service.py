from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class CompletionInput:
    prompt: str
    system_prompt: str | None = None
    memory_context: list[str] | None = None
    max_tokens: int = 4096
    temperature: float = 0.7
    stream: bool = False


@dataclass
class CompletionOutput:
    text: str
    model: str = ""
    usage: dict | None = None


class AIServiceInterface(ABC):
    @abstractmethod
    async def complete(self, input_data: CompletionInput) -> CompletionOutput:
        ...

    @abstractmethod
    async def complete_stream(
        self, input_data: CompletionInput
    ) -> AsyncIterator[str]:
        ...
        yield ""

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        ...

    @abstractmethod
    async def summarize(self, text: str, max_length: int = 200) -> str:
        ...
