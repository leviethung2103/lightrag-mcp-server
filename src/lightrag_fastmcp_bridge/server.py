from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import LightRAGClient


def build_client() -> LightRAGClient:
    base_url = os.environ.get("LIGHTRAG_BASE_URL", "http://localhost:9621")
    api_key = os.environ.get("LIGHTRAG_API_KEY")
    return LightRAGClient(base_url=base_url, api_key=api_key)


def get_mcp_host() -> str:
    return os.environ.get("MCP_HOST", "0.0.0.0")


def get_mcp_port() -> int:
    return int(os.environ.get("MCP_PORT", "3000"))


mcp = FastMCP("lightrag-fastmcp", host=get_mcp_host(), port=get_mcp_port())


@mcp.tool()
async def health() -> dict[str, Any]:
    """Check whether the LightRAG server is alive."""
    return await build_client().health()


@mcp.tool()
async def query(
    question: str,
    mode: str = "naive",
    include_references: bool = True,
    include_chunk_content: bool = False,
    only_need_context: bool = False,
    only_need_prompt: bool = False,
    response_type: str = "Multiple Paragraphs",
    top_k: int = 10,
    enable_rerank: bool = False,
    hl_keywords: list[str] | None = None,
    ll_keywords: list[str] | None = None,
) -> dict[str, Any]:
    """Run a LightRAG query and return the final response payload.

    Args:
        question: The query text to search for
        mode: Query mode - "naive" (semantic vector search), "local", "global", "hybrid", or "mix" (default: "naive")
        include_references: Include source references in response (default: True)
        include_chunk_content: Include chunk content in response (default: False)
        only_need_context: Return only context without LLM response (default: False)
        only_need_prompt: Return only generated prompt without response (default: False)
        response_type: Response format type (default: "Multiple Paragraphs")
        top_k: Number of top results to return (default: 10)
        enable_rerank: Enable reranking of results (default: False)
        hl_keywords: High-level keywords for prioritization (optional)
        ll_keywords: Low-level keywords for search refinement (optional)
    """
    return await build_client().query(
        question,
        mode=mode,
        include_references=include_references,
        include_chunk_content=include_chunk_content,
        only_need_context=only_need_context,
        only_need_prompt=only_need_prompt,
        response_type=response_type,
        top_k=top_k,
        enable_rerank=enable_rerank,
        hl_keywords=hl_keywords,
        ll_keywords=ll_keywords,
    )



@mcp.tool()
async def insert_text(text: str, file_source: str, title: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Insert raw text into LightRAG."""
    return await build_client().insert_text(text, file_source=file_source, title=title, metadata=metadata)


@mcp.tool()
async def insert_texts(texts: list[dict[str, Any]]) -> dict[str, Any]:
    """Insert multiple text payloads into LightRAG."""
    return await build_client().insert_texts(texts)


@mcp.tool()
async def scan_documents() -> dict[str, Any]:
    """Trigger a document scan."""
    return await build_client().scan()


@mcp.tool()
async def document_status_counts() -> dict[str, Any]:
    """Get counts of documents by status."""
    return await build_client().status_counts()


@mcp.tool()
async def pipeline_state() -> dict[str, Any]:
    """Get the current ingestion pipeline state."""
    return await build_client().pipeline_status()


@mcp.tool()
async def get_track_status(track_id: str) -> dict[str, Any]:
    """Get ingestion status for a track id."""
    return await build_client().track_status(track_id)


@mcp.tool()
async def list_documents(page: int = 1, page_size: int = 20, status: str | None = None) -> dict[str, Any]:
    """List paginated documents."""
    return await build_client().documents(page=page, page_size=page_size, status=status)


@mcp.tool()
async def delete_document(doc_id: str) -> dict[str, Any]:
    """Delete a document by doc id."""
    return await build_client().delete_document(doc_id)


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http").lower()

    if transport == "stdio":
        mcp.run("stdio")
        return
    if transport == "sse":
        mcp.run("sse")
        return
    mcp.run("streamable-http")


if __name__ == "__main__":
    main()
