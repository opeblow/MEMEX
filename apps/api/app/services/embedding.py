from __future__ import annotations

from structlog import get_logger

from app.config import settings

logger = get_logger()


class EmbeddingService:
    _client_available: bool | None = None

    @classmethod
    def is_available(cls) -> bool:
        if cls._client_available is not None:
            return cls._client_available
        if not settings.openai_api_key:
            cls._client_available = False
            logger.warning("OPENAI_API_KEY not configured; embedding disabled")
            return False
        cls._client_available = True
        return True

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not self.is_available():
            return [[0.0]] * len(texts)

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error("Embedding failed", error=str(e))
            return [[0.0]] * len(texts)

    async def embed_text(self, text: str) -> list[float]:
        results = await self.embed_texts([text])
        return results[0] if results else []


embedding_service = EmbeddingService()
