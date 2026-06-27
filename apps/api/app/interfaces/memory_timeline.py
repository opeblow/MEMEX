from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimelineEvent:
    id: str
    project_id: str
    event_type: str
    timestamp: datetime
    data: dict | None = None


@dataclass
class TimelineQuery:
    project_id: str
    from_date: datetime | None = None
    to_date: datetime | None = None
    event_types: list[str] | None = None
    limit: int = 50
    offset: int = 0


class MemoryTimelineInterface(ABC):
    @abstractmethod
    async def get_events(self, query: TimelineQuery) -> list[TimelineEvent]:
        ...

    @abstractmethod
    async def record_event(
        self, project_id: str, event_type: str, data: dict | None = None
    ) -> str:
        ...

    @abstractmethod
    async def get_timeline_summary(
        self, project_id: str
    ) -> dict:
        ...
