from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, AsyncIterator

import httpx


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

    async def query(self, query: str, *, mode: str = "naive", include_references: bool = True, include_chunk_content: bool = False, only_need_context: bool = False, only_need_prompt: bool = False, response_type: str = "Multiple Paragraphs", top_k: int = 10, enable_rerank: bool = False, hl_keywords: list[str] | None = None, ll_keywords: list[str] | None = None) -> dict[str, Any]:
        payload = {
            "query": query,
            "mode": mode,
            "include_references": include_references,
            "include_chunk_content": include_chunk_content,
            "stream": stream,
            "only_need_context": only_need_context,
            "only_need_prompt": only_need_prompt,
            "response_type": response_type,
            "top_k": top_k,
            "enable_rerank": enable_rerank,
        }
        if hl_keywords:
            payload["hl_keywords"] = hl_keywords
        if ll_keywords:
            payload["ll_keywords"] = ll_keywords

        async with self._client() as client:
            r = await client.post("/query", json=payload)
            r.raise_for_status()
            return r.json()


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
