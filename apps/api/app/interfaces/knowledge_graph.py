from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GraphNode:
    id: str
    label: str
    type: str
    importance: float = 0.5
    metadata: dict | None = None


@dataclass
class GraphEdge:
    source: str
    target: str
    label: str = ""
    weight: float = 1.0
    metadata: dict | None = None


@dataclass
class GraphSnapshot:
    nodes: list[GraphNode] = list()
    edges: list[GraphEdge] = list()


class KnowledgeGraphInterface(ABC):
    @abstractmethod
    async def get_snapshot(self, project_id: str) -> GraphSnapshot:
        ...

    @abstractmethod
    async def get_neighborhood(
        self, memory_id: str, depth: int = 2, max_nodes: int = 100
    ) -> GraphSnapshot:
        ...

    @abstractmethod
    async def search_nodes(
        self, project_id: str, query: str, limit: int = 20
    ) -> list[GraphNode]:
        ...

    @abstractmethod
    async def add_node(self, node: GraphNode) -> str:
        ...

    @abstractmethod
    async def add_edge(self, edge: GraphEdge) -> None:
        ...
