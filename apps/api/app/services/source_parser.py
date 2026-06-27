from __future__ import annotations

import csv
import json
from io import StringIO
from typing import Any


class SourceParserService:
    async def parse(self, source_type: str, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        parser = self._get_parser(source_type)
        if parser is None:
            raise ValueError(f"Unsupported source type: {source_type}")
        return await parser(data, **kwargs)

    def _get_parser(self, source_type: str):
        parsers = {
            "markdown": self._parse_markdown,
            "plain_text": self._parse_plain_text,
            "csv": self._parse_csv,
            "json": self._parse_json,
            "meeting_note": self._parse_meeting_note,
        }
        return parsers.get(source_type)

    async def _parse_markdown(self, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        chunks = []
        sections = text.split("\n## ")
        for i, section in enumerate(sections):
            lines = section.strip().split("\n")
            title = lines[0].lstrip("# ").strip() if lines else f"section_{i}"
            content = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
            if content:
                chunks.append({
                    "title": title,
                    "content": content,
                    "memory_type": "text",
                    "metadata": {"section_index": i, "source_format": "markdown"},
                })
        if not chunks:
            chunks.append({
                "title": kwargs.get("title", "markdown_document"),
                "content": text[:10000],
                "memory_type": "text",
                "metadata": {"source_format": "markdown"},
            })
        return chunks

    async def _parse_plain_text(self, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        return [{
            "title": kwargs.get("title", "text_document"),
            "content": text[:10000],
            "memory_type": "text",
            "metadata": {"source_format": "plain_text"},
        }]

    async def _parse_csv(self, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        reader = csv.DictReader(StringIO(text))
        chunks = []
        for i, row in enumerate(reader):
            content = json.dumps(row, default=str)
            title = row.get("title", row.get("name", f"row_{i}"))
            chunks.append({
                "title": str(title),
                "content": content[:5000],
                "memory_type": "text",
                "metadata": {"row_index": i, "source_format": "csv"},
            })
        return chunks

    async def _parse_json(self, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            parsed = [parsed]
        chunks = []
        for i, item in enumerate(parsed):
            content = json.dumps(item, default=str)
            title = item.get("title", item.get("name", f"item_{i}"))
            chunks.append({
                "title": str(title),
                "content": content[:5000],
                "memory_type": "text",
                "metadata": {"item_index": i, "source_format": "json"},
            })
        return chunks

    async def _parse_meeting_note(self, data: str | bytes, **kwargs) -> list[dict[str, Any]]:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        lines = text.strip().split("\n")
        title = kwargs.get("title", "Meeting Note")
        date = ""
        attendees: list[str] = []
        for line in lines[:10]:
            lower = line.lower()
            if "date:" in lower or "date :" in lower:
                date = line.split(":", 1)[-1].strip()
            if "attendees:" in lower or "attendees :" in lower:
                attendees_str = line.split(":", 1)[-1].strip()
                attendees = [a.strip() for a in attendees_str.split(",") if a.strip()]
        return [{
            "title": title,
            "content": text[:10000],
            "memory_type": "meeting_note",
            "metadata": {
                "date": date,
                "attendees": attendees,
                "source_format": "meeting_note",
            },
        }]

    async def parse_url_content(self, url: str, html_text: str) -> list[dict[str, Any]]:
        import re
        text = re.sub(r"<[^>]+>", " ", html_text)
        text = re.sub(r"\s+", " ", text).strip()
        lines = text.split("\n")
        title = ""
        for line in lines[:5]:
            if line.strip():
                title = line.strip()[:200]
                break
        chunks = []
        chunk_size = 3000
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append({
                    "title": f"{title} (part {i // chunk_size + 1})" if i > 0 else title,
                    "content": chunk,
                    "memory_type": "url",
                    "metadata": {"source_url": url, "source_format": "html"},
                })
        return chunks

    async def parse_pdf(
        self, file_bytes: bytes, filename: str = "document.pdf",
    ) -> list[dict[str, Any]]:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(file_bytes)
            texts = []
            for page in reader.pages:
                text = page.extract_text()
                if text.strip():
                    texts.append(text)
            full_text = "\n\n".join(texts)
            return [{
                "title": filename,
                "content": full_text[:10000],
                "memory_type": "text",
                "metadata": {"source_format": "pdf", "pages": len(reader.pages)},
            }]
        except ImportError:
            text = file_bytes.decode("utf-8", errors="replace")
            return [{
                "title": filename,
                "content": text[:10000],
                "memory_type": "text",
                "metadata": {"source_format": "pdf_fallback"},
            }]

    async def parse_github(self, repo_url: str) -> list[dict[str, Any]]:
        import re
        match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")
        owner, repo = match.group(1), match.group(2).rstrip(".git")
        chunks = [{
            "title": f"Repository: {owner}/{repo}",
            "content": f"GitHub repository {owner}/{repo}",
            "memory_type": "github_issue",
            "metadata": {"source_format": "github_repo", "owner": owner, "repo": repo},
        }]
        import httpx
        async with httpx.AsyncClient() as client:
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
            try:
                resp = await client.get(readme_url, timeout=10)
                if resp.status_code == 200:
                    chunks.append({
                        "title": f"README: {owner}/{repo}",
                        "content": resp.text[:10000],
                        "memory_type": "text",
                        "metadata": {"source_format": "markdown", "owner": owner, "repo": repo},
                    })
            except Exception:
                pass
        return chunks


source_parser_service = SourceParserService()
