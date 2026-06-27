from __future__ import annotations

from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    importance: float = 0.5
    position: dict = {"x": 0, "y": 0, "z": 0}


class GraphEdge(BaseModel):
    source: str
    target: str
    label: str = ""
    weight: float = 1.0


class GraphSnapshot(BaseModel):
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []


class NeighborhoodRequest(BaseModel):
    memory_id: str
    depth: int = 2
    max_nodes: int = 100
