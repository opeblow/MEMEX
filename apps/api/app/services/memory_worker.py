from __future__ import annotations

import asyncio

from structlog import get_logger

logger = get_logger()


class MemoryWorker:
    def __init__(self):
        self._tasks: dict[str, asyncio.Task] = {}

    async def enqueue(self, task_type: str, **kwargs) -> str:
        task_id = f"{task_type}_{id(kwargs)}"
        if task_id not in self._tasks or self._tasks[task_id].done():
            task = asyncio.create_task(
                self._run(task_type, task_id, **kwargs),
                name=task_id,
            )
            self._tasks[task_id] = task
            logger.info("Task enqueued", task_type=task_type, task_id=task_id)
        return task_id

    async def _run(self, task_type: str, task_id: str, **kwargs) -> None:
        try:
            logger.info("Task started", task_type=task_type, task_id=task_id)
            if task_type == "index_memory":
                await self._index_memory(**kwargs)
            elif task_type == "improve_memories":
                await self._improve_memories(**kwargs)
            elif task_type == "expire_memories":
                await self._expire_memories(**kwargs)
            elif task_type == "prune_memories":
                await self._prune_memories(**kwargs)
            else:
                logger.warning("Unknown task type", task_type=task_type)
            logger.info("Task completed", task_type=task_type, task_id=task_id)
        except Exception as e:
            logger.error("Task failed", task_type=task_type, task_id=task_id, error=str(e))

    async def _index_memory(self, **kwargs) -> None:
        from app.database.session import async_session_factory
        from app.models.memory import Memory
        memory_id = kwargs.get("memory_id", "")
        async with async_session_factory() as db:
            from sqlalchemy import select
            result = await db.execute(select(Memory).where(Memory.id == memory_id))
            memory = result.scalar_one_or_none()
            if memory:
                from app.services.memory_index import memory_index
                await memory_index.index_memory(db, memory)

    async def _improve_memories(self, **kwargs) -> None:
        from app.services.cognee_adapter import cognee_adapter
        await cognee_adapter.improve(
            user_id=kwargs.get("user_id", ""),
            project_id=kwargs.get("project_id", ""),
            session_ids=kwargs.get("session_ids"),
            build_global_context_index=kwargs.get("build_global_context_index", False),
        )

    async def _expire_memories(self, **kwargs) -> None:
        from app.database.session import async_session_factory
        async with async_session_factory() as db:
            from app.services.memory_lifecycle import memory_lifecycle
            await memory_lifecycle.expire_memories(
                db=db,
                project_id=kwargs.get("project_id", ""),
                older_than_days=kwargs.get("older_than_days", 90),
            )

    async def _prune_memories(self, **kwargs) -> None:
        from app.database.session import async_session_factory
        async with async_session_factory() as db:
            from app.services.memory_lifecycle import memory_lifecycle
            await memory_lifecycle.prune_project(
                db=db,
                project_id=kwargs.get("project_id", ""),
            )


memory_worker = MemoryWorker()
