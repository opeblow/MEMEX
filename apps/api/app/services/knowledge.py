from __future__ import annotations

from structlog import get_logger

from app.config import settings

logger = get_logger()


class KnowledgeService:
    async def extract_entities(self, text: str) -> list[dict]:
        if not settings.openai_api_key:
            return []
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Extract entities and relationships from the text. "
                            "Return JSON array: [{name, type, description}]."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            import json
            data = json.loads(content)
            return data.get("entities", data.get("nodes", []))
        except Exception as e:
            logger.error("Entity extraction failed", error=str(e))
            return []

    async def generate_tags(self, text: str, max_tags: int = 8) -> list[str]:
        if not settings.openai_api_key:
            return []
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"Generate up to {max_tags} relevant tags for this content. "
                            "Return JSON: {\"tags\": [\"tag1\", \"tag2\"]}"
                        ),
                    },
                    {"role": "user", "content": text[:2000]},
                ],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or '{"tags": []}'
            import json
            return json.loads(content).get("tags", [])
        except Exception as e:
            logger.error("Tag generation failed", error=str(e))
            return []

    async def summarize(self, text: str, max_length: int = 200) -> str:
        if not settings.openai_api_key:
            return text[:max_length]
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"Summarize the following content in"
                            f" {max_length} characters or less."
                        ),
                    },
                    {"role": "user", "content": text[:4000]},
                ],
            )
            return response.choices[0].message.content or text[:max_length]
        except Exception as e:
            logger.error("Summarization failed", error=str(e))
            return text[:max_length]

    async def merge_duplicates(
        self, existing_tags: list[str], new_tags: list[str]
    ) -> list[str]:
        combined = list(set(existing_tags + new_tags))
        if not settings.openai_api_key:
            return combined
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Merge duplicate or highly similar tags. "
                            "Return JSON: {\"tags\": [\"deduplicated\", \"tags\"]}"
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Tags: {', '.join(combined)}",
                    },
                ],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or '{"tags": []}'
            import json
            return json.loads(content).get("tags", combined)
        except Exception as e:
            logger.error("Tag merge failed", error=str(e))
            return combined


knowledge_service = KnowledgeService()
