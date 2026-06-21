from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, AsyncIterator

import httpx
from httpx_sse import aconnect_sse


@dataclass
class LightRAGClient:
    base_url: str
    api_key: str | None = None
    timeout: float = 120.0

    def _headers(self) -> dict[str, str]:
        headers = {"accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url.rstrip("/"), headers=self._headers(), timeout=self.timeout)

    async def health(self) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.get("/health")
            r.raise_for_status()
            return r.json()

    async def query(self, query: str, *, include_references: bool = True, include_chunk_content: bool = False, stream: bool = False) -> dict[str, Any]:
        payload = {
            "query": query,
            "include_references": include_references,
            "include_chunk_content": include_chunk_content,
            "stream": stream,
        }
        async with self._client() as client:
            r = await client.post("/query", json=payload)
            r.raise_for_status()
            return r.json()

    async def query_stream(self, query: str, *, include_references: bool = True, include_chunk_content: bool = False) -> AsyncIterator[str]:
        payload = {
            "query": query,
            "include_references": include_references,
            "include_chunk_content": include_chunk_content,
            "stream": True,
        }
        async with self._client() as client:
            async with aconnect_sse(client, "POST", "/query/stream", json=payload) as event_source:
                async for event in event_source.aiter_sse():
                    data = event.data
                    if not data:
                        continue
                    try:
                        parsed = json.loads(data)
                    except json.JSONDecodeError:
                        yield data
                        continue
                    if isinstance(parsed, dict) and "response" in parsed:
                        yield str(parsed["response"])
                    elif isinstance(parsed, dict) and "token" in parsed:
                        yield str(parsed["token"])
                    else:
                        yield data

    async def insert_text(self, text: str, *, file_source: str, title: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {"text": text, "file_source": file_source, "title": title, "metadata": metadata or {}}
        async with self._client() as client:
            r = await client.post("/documents/text", json=payload)
            r.raise_for_status()
            return r.json()

    async def insert_texts(self, texts: list[dict[str, Any]]) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.post("/documents/texts", json={"texts": texts})
            r.raise_for_status()
            return r.json()

    async def scan(self) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.post("/documents/scan")
            r.raise_for_status()
            return r.json()

    async def status_counts(self) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.get("/documents/status_counts")
            r.raise_for_status()
            return r.json()

    async def pipeline_status(self) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.get("/documents/pipeline_status")
            r.raise_for_status()
            return r.json()

    async def track_status(self, track_id: str) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.get(f"/documents/track_status/{track_id}")
            r.raise_for_status()
            return r.json()

    async def documents(self, *, page: int = 1, page_size: int = 20, status: str | None = None) -> dict[str, Any]:
        payload = {"page": page, "page_size": page_size}
        if status:
            payload["status"] = status
        async with self._client() as client:
            r = await client.post("/documents/paginated", json=payload)
            r.raise_for_status()
            return r.json()

    async def delete_document(self, doc_id: str) -> dict[str, Any]:
        async with self._client() as client:
            r = await client.delete("/documents/delete_document", params={"doc_id": doc_id})
            r.raise_for_status()
            return r.json()
