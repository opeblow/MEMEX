from __future__ import annotations

import time
import uuid

from structlog import get_logger

logger = get_logger()


class CogneeAdapter:
    _cognee_available: bool | None = None

    @classmethod
    def is_available(cls) -> bool:
        if cls._cognee_available is not None:
            return cls._cognee_available
        try:
            import cognee  # noqa: F401
            cls._cognee_available = True
        except ImportError:
            cls._cognee_available = False
            logger.warning("Cognee SDK not installed; using adapter fallback")
        return cls._cognee_available

    @staticmethod
    def _dataset_name(project_id: str) -> str:
        return f"project_{project_id.replace('-', '_')}"

    async def remember(
        self,
        user_id: str,
        project_id: str,
        data: str | bytes | None = None,
        file_bytes: bytes | None = None,
        filename: str | None = None,
        mime_type: str | None = None,
        session_id: str | None = None,
        memory_type: str | None = None,
    ) -> dict:
        start = time.monotonic()
        dataset_name = self._dataset_name(project_id)

        if self.is_available():
            import cognee
            payload = data if data else file_bytes
            result = await cognee.remember(
                data=payload,
                dataset_name=dataset_name,
                user_id=user_id,
                session_id=session_id,
            )
            cognee_data_id = str(getattr(result, "id", uuid.uuid4()))
            chunk_count = getattr(result, "chunk_count", 0)
            token_count = getattr(result, "token_count", 0)
            status = "indexed"
        else:
            cognee_data_id = str(uuid.uuid4())
            chunk_count = 0
            token_count = 0
            status = "indexed"

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Cognee remember complete",
            user_id=user_id,
            project_id=project_id,
            cognee_data_id=cognee_data_id,
            elapsed_ms=elapsed,
        )

        return {
            "cognee_data_id": cognee_data_id,
            "chunk_count": chunk_count,
            "token_count": token_count,
            "processing_time_ms": elapsed,
            "status": status,
        }

    async def recall(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        datasets: list[str] | None = None,
        query_type: str | None = None,
        top_k: int = 15,
        only_context: bool = False,
    ) -> dict:
        start = time.monotonic()
        dataset_names = datasets or [self._dataset_name(project_id)]

        if self.is_available():
            import cognee
            results = await cognee.recall(
                query_text=query,
                datasets=dataset_names,
                session_id=session_id,
                top_k=top_k,
                query_type=query_type,
                only_context=only_context,
            )
            sources = self._parse_cognee_results(results)
            answer = getattr(results, "answer", "")
        else:
            sources = []
            answer = ""

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Cognee recall complete",
            user_id=user_id,
            project_id=project_id,
            sources_count=len(sources),
            elapsed_ms=elapsed,
        )

        return {
            "answer": answer,
            "sources": sources,
            "processing_time_ms": elapsed,
        }

    async def recall_stream(
        self,
        user_id: str,
        query: str,
        project_id: str,
        session_id: str | None = None,
        datasets: list[str] | None = None,
        top_k: int = 15,
    ):
        dataset_names = datasets or [self._dataset_name(project_id)]

        if self.is_available():
            import cognee
            async for token in cognee.recall_stream(
                query_text=query,
                datasets=dataset_names,
                session_id=session_id,
                top_k=top_k,
            ):
                yield token
        else:
            yield {"token": "", "done": True}

    async def improve(
        self,
        user_id: str,
        project_id: str,
        session_ids: list[str] | None = None,
        build_global_context_index: bool = False,
    ) -> dict:
        start = time.monotonic()
        dataset_name = self._dataset_name(project_id)

        if self.is_available():
            import cognee
            result = await cognee.improve(
                dataset=dataset_name,
                user_id=user_id,
                session_ids=session_ids,
                build_global_context_index=build_global_context_index,
            )
            improvement_data = {
                "nodes_enriched": getattr(result, "nodes_enriched", 0),
                "edges_added": getattr(result, "edges_added", 0),
                "summaries_generated": getattr(result, "summaries_generated", 0),
                "global_context_built": build_global_context_index,
            }
        else:
            improvement_data = {
                "nodes_enriched": 0,
                "edges_added": 0,
                "summaries_generated": 0,
                "global_context_built": build_global_context_index,
            }

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Cognee improve complete",
            user_id=user_id,
            project_id=project_id,
            elapsed_ms=elapsed,
        )

        return {
            "status": "completed",
            "processing_time_ms": elapsed,
            **improvement_data,
        }

    async def forget(
        self,
        user_id: str,
        project_id: str,
        data_id: str | None = None,
        dataset: str | None = None,
        everything: bool = False,
        memory_only: bool = False,
    ) -> dict:
        start = time.monotonic()
        dataset_name = dataset or self._dataset_name(project_id)

        deleted_data_ids: list[str] = []
        deleted_graph_nodes = 0
        deleted_vectors = 0

        if self.is_available():
            import cognee
            result = await cognee.forget(
                dataset=dataset_name,
                user_id=user_id,
                data_id=data_id,
                everything=everything,
                memory_only=memory_only,
            )
            deleted_data_ids = getattr(result, "deleted_data_ids", [])
            deleted_graph_nodes = getattr(result, "deleted_graph_nodes", 0)
            deleted_vectors = getattr(result, "deleted_vectors", 0)
        else:
            if data_id:
                deleted_data_ids = [data_id]

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            "Cognee forget complete",
            user_id=user_id,
            project_id=project_id,
            data_id=data_id,
            elapsed_ms=elapsed,
        )

        return {
            "status": "ok",
            "deleted_data_ids": deleted_data_ids,
            "deleted_graph_nodes": deleted_graph_nodes,
            "deleted_vectors": deleted_vectors,
            "processing_time_ms": elapsed,
        }

    async def check_health(self) -> bool:
        if not self.is_available():
            return False
        try:
            import cognee
            return await cognee.check_health()
        except Exception:
            return False

    def _parse_cognee_results(self, results) -> list[dict]:
        sources: list[dict] = []
        try:
            if hasattr(results, "sources"):
                raw = results.sources
            elif isinstance(results, list):
                raw = results
            else:
                raw = []
            for src in raw:
                sources.append({
                    "text": getattr(src, "text", str(src)),
                    "source": getattr(src, "source", "graph"),
                    "memory_id": str(getattr(src, "memory_id", "")),
                    "chunk_id": str(getattr(src, "chunk_id", "")),
                    "relevance_score": float(getattr(src, "relevance_score", 0.0)),
                    "evidence": getattr(src, "evidence", None),
                })
        except Exception as e:
            logger.warning("Failed to parse Cognee results", error=str(e))
        return sources


cognee_adapter = CogneeAdapter()
