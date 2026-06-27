from __future__ import annotations

import asyncio
from typing import Any

from app.models.source_import import ImportJob


class BackgroundImportService:
    _tasks: dict[str, asyncio.Task] = {}

    async def start_import(
        self,
        db_factory: Any,
        job: ImportJob,
        data: str | bytes | None = None,
    ):
        from app.services.import_pipeline import import_pipeline_service

        async def _run():
            try:
                async with db_factory() as db:
                    await import_pipeline_service.run_import(db, job, data)
            except Exception:
                pass
            finally:
                self._tasks.pop(job.id, None)

        task = asyncio.create_task(_run())
        self._tasks[job.id] = task
        return job

    async def cancel_import(self, job_id: str) -> bool:
        task = self._tasks.get(job_id)
        if task:
            task.cancel()
            self._tasks.pop(job_id, None)
            return True
        return False


background_import_service = BackgroundImportService()
